import argparse
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import concurrent.futures
from tqdm import tqdm
import openai
import requests
import trafilatura
from tqdm import tqdm
from utils.bilingual_txt_to_docx import create_bilingual_docx
from utils.parse_pdfs.extract_pdfs import process_pdfs

ALLOWED_FILE_TYPES = [
    ".txt",
    ".md",
    ".rtf",
    ".html",
    ".pdf",
]
AZURE_API_VERSION = "2023-03-15-preview"


def translate(key, target_language, not_to_translate_people_names, text,use_chatglm=False, use_azure=False, api_base="", deployment_name=""):
    last_request_time = 0
    request_interval = 1  # seconds
    max_backoff_time = 60  # seconds

    api_base = api_base or os.environ.get("OPENAI_API_BASE")

    if use_chatglm:
        openai.api_base = api_base


    # Set up OpenAI API version
    if use_azure:
        openai.api_type = "azure"
        openai.api_version = AZURE_API_VERSION
        openai.api_base = api_base

    # Set up OpenAI API key
    openai.api_key = key
    if not text:
        return ""
    # lang
    while True:
        try:
            # Check if enough time has passed since the last request
            elapsed_time = time.monotonic() - last_request_time
            if elapsed_time < request_interval:
                time.sleep(request_interval - elapsed_time)
            last_request_time = time.monotonic()
            # change prompt based on not_to_translate_people_names
            if not_to_translate_people_names:
                messages=[{
                    'role': 'system',
                    'content': 'You are a translator assistant.'
                }, {
                    "role":
                    "user",
                    "content":
                    f"Translate the following text into {target_language} in a way that is faithful to the original text. But do not translate people and authors' names and surnames. Do not remove numbers. Return only the translation and nothing else:\n{text}",
                }]
            else:
                messages=[{
                    'role': 'system',
                    'content': 'You are a translator assistant.'
                }, {
                    "role":
                    "user",
                    "content":
                    f"Translate the following text into {target_language} in a way that is faithful to the original text. Retain the original format. Return only the translation and nothing else:\n{text}",
                }]
            if use_azure:
                completion = openai.ChatCompletion.create(
                    # No need to specify model since deployment contain that information.
                    messages=messages,
                    deployment_id=deployment_name
                )
            else:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                )
            t_text = (completion["choices"][0].get("message").get(
                "content").encode("utf8").decode())
            break
        except Exception as e:
            print(str(e))
            # Exponential backoff if rate limit is hit
            request_interval *= 2
            if request_interval > max_backoff_time:
                request_interval = max_backoff_time
            print(f"Rate limit hit. Sleeping for {request_interval} seconds.")
            time.sleep(request_interval)
            continue

    return t_text


def remove_empty_paragraphs(text):
    # Split the text into paragraphs
    if isinstance(text, str):
        text = text.split('\n')

    # Filter out empty paragraphs
    non_empty_paragraphs = filter(lambda p: p.strip() != '', text)

    # Join the non-empty paragraphs back into a string
    return '\n'.join(non_empty_paragraphs)




def translate_text_file(text_filepath_or_url, options):
    OPENAI_API_KEY = options.openai_key or os.environ.get("OPENAI_API_KEY")

    paragraphs = read_and_preprocess_data(text_filepath_or_url, options)

    # keep first three paragraphs
    first_three_paragraphs = paragraphs[:2]

    # if users require to ignore References, we then take out all paragraphs after the one starting with "References"
    if options.not_to_translate_references:
        ignore_strings = [
            "Acknowledgment", "Notes", "NOTES", "disclosure statement",
            "References", "Funding", "declaration of conflicting interest",
            "acknowledgment", "supplementary material", "Acknowledgements"
        ]
        ignore_indices = []
        for i, p in enumerate(paragraphs):
            for ignore_str in ignore_strings:
                if (p.startswith(ignore_str) or p.lower().startswith(
                        ignore_str.lower())) and len(p) < 30:
                    ignore_indices.append(i)
                    break
        if ignore_indices:
            print("References will not be translated.")
            ref_paragraphs = paragraphs[min(ignore_indices):]
            paragraphs = paragraphs[:min(ignore_indices)]
        else:
            print(paragraphs[-3:])
            raise Exception("No References found.")

    with ThreadPoolExecutor(max_workers=options.num_threads) as executor:
        translated_paragraphs = list(
            tqdm(executor.map(
                lambda text:
                translate(OPENAI_API_KEY, options.target_language, options.
                          not_to_translate_people_names, text,options.use_chatglm, options.use_azure, options.endpoint, options.azure_deployment_name), paragraphs),
                 total=len(paragraphs),
                 desc="Translating paragraphs",
                 unit="paragraph"))
        translated_paragraphs = [p.strip() for p in translated_paragraphs]

    translated_text = "\n".join(translated_paragraphs)

    if options.bilingual:
        bilingual_text = "\n".join(f"{paragraph}\n{translation}"
                                   for paragraph, translation in zip(
                                       paragraphs, translated_paragraphs))
        # add first three paragraphs if required
        if options.keep_first_two_paragraphs:
            bilingual_text = "\n".join(
                first_three_paragraphs) + "\n" + bilingual_text
        # append References
        if options.not_to_translate_references:
            bilingual_text += "\n".join(ref_paragraphs)
        bilingual_text = remove_empty_paragraphs(bilingual_text)
        output_file = f"{Path(text_filepath_or_url).parent}/{Path(text_filepath_or_url).stem}_bilingual.txt"
        with open(output_file, "w") as f:
            f.write(bilingual_text)
            print(f"Bilingual text saved to {f.name}.")

    else:
        # remove extra newlines
        translated_text = re.sub(r"\n{2,}", "\n", translated_text)
        # add first three paragraphs if required
        if options.keep_first_two_paragraphs:
            translated_text = "\n".join(
                first_three_paragraphs) + "\n" + translated_text
        # append References
        if options.not_to_translate_references:
            translated_text += "\n" + "\n".join(ref_paragraphs)
        translated_text = remove_empty_paragraphs(translated_text)
        output_file = f"{Path(text_filepath_or_url).parent}/{Path(text_filepath_or_url).stem}_translated.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(translated_text)
            print(f"Translated text saved to {f.name}.")
    create_bilingual_docx(output_file)


def download_html(url):
    response = requests.get(url)
    return response.text




def read_and_preprocess_data(text_filepath_or_url, options):
    if text_filepath_or_url.startswith('http'):
        # replace "https:/www" with "https://www"
        text_filepath_or_url = text_filepath_or_url.replace(":/", "://")
        # download and extract text from URL
        print("Downloading and extracting text from URL...")
        downloaded = trafilatura.fetch_url(text_filepath_or_url)
        print("Downloaded text:")
        print(downloaded)
        text = trafilatura.extract(downloaded)
    elif text_filepath_or_url.endswith('.pdf'):
        # extract text from PDF file
        print("Extracting text from PDF file...")
        process_pdfs(text_filepath_or_url)
        # use newly created txt file
        text_filepath_or_url = f"{Path(text_filepath_or_url).parent}/{Path(text_filepath_or_url).stem}_extracted.txt"
        with open(text_filepath_or_url, "r", encoding='utf-8') as f:
            text = f.read()
    else:
        with open(text_filepath_or_url, "r", encoding='utf-8') as f:
            text = f.read()
            if text_filepath_or_url.endswith('.html'):
                # extract text from HTML file
                print("Extracting text from HTML file...")
                text = trafilatura.extract(text)
                # write to a txt file ended with "_extracted"
                with open(
                        f"{Path(text_filepath_or_url).parent}/{Path(text_filepath_or_url).stem}_extracted.txt",
                        "w") as f:
                    f.write(text)
                    print(f"Extracted text saved to {f.name}.")
    paragraphs = [p.strip() for p in text.split("\n") if p.strip() != ""]

    # Remove paragraphs after "References" or other keywords in ignore_strings
    if options.remove_references:
        ignore_strings = [
            "Acknowledgment", "Acknowledgments", "Notes", "NOTES",
            "disclosure statement", "References", "Funding",
            "declaration of conflicting interest", "acknowledgment",
            "supplementary material", "Acknowledgements"
        ]
        for i, p in enumerate(paragraphs):
            for ignore_str in ignore_strings:
                if (p.startswith(ignore_str) or p.lower().startswith(
                        ignore_str.lower())) and len(p) < 30:
                    paragraphs = paragraphs[:i]
                    break
            else:
                continue
            break

    return paragraphs


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser()

    arguments = [
        ("--input_path", {"type": str, "help": "input file or folder to translate"}),
        ("--openai_key", {"type": str, "default": "", "help": "OpenAI API key"}),
        ("--num_threads", {"type": int, "default": 10, "help": "number of threads to use for translation"}),
        ("--bilingual", {"action": "store_true", "default": False, "help": "output bilingual txt file with original and translated text side by side"}),
        ("--target_language", {"type": str, "default": "Simplified Chinese", "help": "target language to translate to"}),
        ("--not_to_translate_people_names", {"action": "store_true", "default": False, "help": "whether or not to translate names in the text"}),
        ("--not_to_translate_references", {"action": "store_true", "default": False, "help": "not to translate references"}),
        ("--keep_first_two_paragraphs", {"action": "store_true", "default": False, "help": "keep the first three paragraphs of the original text"}),
        ("--only_process_this_file_extension", {"type": str, "default": "", "help": "only process files with this extension"}),
        ("--remove_references", {"action": "store_true", "default": False, "help": "remove all paragraphs after 'References' or any other similar keywords found in ignore_strings"}),
        ("--use_azure", {"action": "store_true", "default": False,"help": "Use Azure OpenAI service instead of OpenAI platform."}),
        ("--use_chatglm",
         {"action": "store_true", "default": False, "help": "Use ChatGLM  service instead of OpenAI platform."}),
        ("--endpoint",
         {"type": str, "default": "", "help": "Endpoint URL of Azure OpenAI service"}),
        ("--azure_deployment_name",
         {"type": str, "default": "", "help": "Deployment of Azure OpenAI service. Only require when use AOAI."}),
    ]

    for argument, kwargs in arguments:
        parser.add_argument(argument, **kwargs)

    options = parser.parse_args()
    OPENAI_API_KEY = options.openai_key or os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY and not options.use_chatglm:
        raise Exception("Please provide your OpenAI API key")

    
    if options.use_azure:
        assert options.endpoint is not None and options.endpoint != '', "--endpoint is required when use Azure"
        assert options.azure_deployment_name is not None and options.azure_deployment_name, "--azure_deployment_name is required when use Azure"
    return options



def check_file_path(file_path: Path, options=None):
    """
    Ensure file extension is in ALLOWED_FILE_TYPES or is a URL.
    If file ends with _translated.txt or _bilingual.txt, skip it.
    If there is any txt file ending with _translated.txt or _bilingual.txt, skip it.
    """
    if not file_path.suffix.lower() in ALLOWED_FILE_TYPES and not str(
            file_path).startswith('http'):
        print(f"File extension {file_path.suffix} is not allowed.")
        raise Exception("Please use a txt file or URL")

    if file_path.stem.endswith("_translated") or file_path.stem.endswith(
            "extracted_translated"):
        print(
            f"You already have a translated file for {file_path}, skipping...")
        return False
    elif file_path.stem.endswith("_bilingual") or file_path.stem.endswith(
            "extracted_bilingual"):
        print(
            f"You already have a bilingual file for {file_path}, skipping...")
        return False

    if (file_path.with_name(f"{file_path.stem}_translated.txt").exists() or
            file_path.with_name(f"{file_path.stem}_extracted_translated.txt").
            exists()) and not getattr(options, 'bilingual', False):
        print(
            f"You already have a translated file for {file_path}, skipping...")
        return False
    elif (file_path.with_name(f"{file_path.stem}_bilingual.txt").exists()
          or file_path.with_name(f"{file_path.stem}_extracted_bilingual.txt").
          exists()) and getattr(options, 'bilingual', False):
        print(
            f"You already have a bilingual file for {file_path}, skipping...")
        return False

    return True


def process_file(file_path, options):
    """Translate a single text file"""
    if not check_file_path(file_path, options):
        return
    print(f"Translating {file_path}...")
    translate_text_file(str(file_path), options)


def process_folder(folder_path, options):
    """Translate all text files in a folder"""
    # if only_process_this_file_extension is set, only process files with this extension
    if options.only_process_this_file_extension:
        files_to_process = list(
            folder_path.rglob(f"*.{options.only_process_this_file_extension}"))
        print(
            f"Only processing files with extension {options.only_process_this_file_extension}"
        )
        print(f"Found {len(files_to_process)} files to process")
    else:
        files_to_process = list(folder_path.rglob("*"))
    total_files = len(files_to_process)
    for index, file_path in enumerate(files_to_process):
        if file_path.is_file() and file_path.suffix.lower(
        ) in ALLOWED_FILE_TYPES:
            process_file(file_path, options)
        print(
            f"Processed file {index + 1} of {total_files}. Only {total_files - index - 1} files left to process."
        )


def main():
    """Main function"""
    options = parse_arguments()
    input_path = Path(options.input_path)
    if input_path.is_dir():
        # input path is a folder, scan and process all allowed file types
        process_folder(input_path, options)
    elif input_path.is_file:
        process_file(input_path, options)


if __name__ == "__main__":
    main()
