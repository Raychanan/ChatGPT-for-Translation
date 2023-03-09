import os
import re
from tqdm import tqdm
import argparse
import time
from os import environ as env
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import openai


ALLOWED_FILE_TYPES = [".txt", ".md", ".rtf"]

class ChatGPT:

    def __init__(self, key, target_lang):
        self.key = key
        self.target_lang = target_lang
        self.last_request_time = 0
        self.request_interval = 1  # seconds
        self.max_backoff_time = 60  # seconds

    def translate(self, text):
        # Set up OpenAI API key
        openai.api_key = self.key
        # lang
        while True:
            try:
                # Check if enough time has passed since the last request
                elapsed_time = time.monotonic() - self.last_request_time
                if elapsed_time < self.request_interval:
                    time.sleep(self.request_interval - elapsed_time)
                self.last_request_time = time.monotonic()

                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{
                        'role':
                        'system',
                        'content':
                        'You are a translator assistant.'
                    }, {
                        "role":
                        "user",
                        "content":
                        f"Translate the following text into {self.target_lang} in a way that is faithful to the original text. Do not translate people and authors' names. Return only the translation and nothing else:\n {text}",
                    }],
                )
                t_text = (completion["choices"][0].get("message").get(
                    "content").encode("utf8").decode())
                break
            except Exception as e:
                print(str(e))
                # Exponential backoff if rate limit is hit
                self.request_interval *= 2
                if self.request_interval > self.max_backoff_time:
                    self.request_interval = self.max_backoff_time
                print(
                    f"Rate limit hit. Sleeping for {self.request_interval} seconds."
                )
                time.sleep(self.request_interval)
                continue

        return t_text
    
def translate_text_file(text_filepath, options):
    OPENAI_API_KEY = options.openai_key or os.environ.get("OPENAI_API_KEY")

    with open(text_filepath, "r") as f:
        text = f.read()
        paragraphs = [p.strip() for p in text.split("\n") if p.strip() != ""]

    if options.bilingual:
        with ThreadPoolExecutor(max_workers=options.num_threads) as executor:
            translator = ChatGPT(OPENAI_API_KEY, options.target_lang)
            translated_paragraphs = list(
                tqdm(executor.map(translator.translate, paragraphs),
                    total=len(paragraphs),
                    desc="Translating paragraphs",
                    unit="paragraph"))
            translated_paragraphs = [p.strip() for p in translated_paragraphs]

        translated_text = "\n".join(translated_paragraphs)
        bilingual_text = "\n".join(f"{paragraph}\n{translation}"
                                   for paragraph, translation in zip(
                                       paragraphs, translated_paragraphs))
        output_file = f"{Path(text_filepath).parent}/{Path(text_filepath).stem}_bilingual.txt"
        with open(output_file, "w") as f:
            f.write(bilingual_text)
            print(f"Bilingual text saved to {f.name}.")
    else:
        # if len(paragraphs) % 2 == 1:
        #     # Add a placeholder string to make the number of paragraphs even
        #     paragraphs.append("")

        # # for every two paragraphs, join them together 
        # # and translate them as a single paragraph pair
        # pairs = [f"{paragraphs[i]}\n{paragraphs[i+1]}"
        #         for i in range(0, len(paragraphs), 2)]

        pairs = paragraphs

        with ThreadPoolExecutor(max_workers=options.num_threads) as executor:
            translator = ChatGPT(OPENAI_API_KEY, options.target_lang)
            # Translate each pair of paragraphs
            translated_pairs = list(
                tqdm(executor.map(translator.translate, pairs),
                    total=len(pairs),
                    desc="Translating paragraph pairs",
                    unit="paragraph pair"))
            translated_paragraphs = [p.strip() for p in translated_pairs]

        translated_text = "\n".join(translated_paragraphs).strip()
        # remove extra newlines
        translated_text = re.sub(r"\n{2,}", "\n", translated_text)
        output_file = f"{Path(text_filepath).parent}/{Path(text_filepath).stem}_translated.txt"
        with open(output_file, "w") as f:
            f.write(translated_text)
            print(f"Translated text saved to {f.name}.")




def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_path",
        dest="input_path",
        type=str,
        help="input file or folder to translate",
    )
    parser.add_argument(
        "--openai_key",
        dest="openai_key",
        type=str,
        default="",
        help="OpenAI API key",
    )
    parser.add_argument(
        "--num_threads",
        dest="num_threads",
        type=int,
        default=5,
        help="number of threads to use for translation",
    )
    parser.add_argument(
        "--bilingual",
        dest="bilingual",
        action="store_true",
        default=False,
        help="output bilingual txt file with original and translated text side by side",
    )
    parser.add_argument(
        "--target_lang",
        dest="target_lang",
        type=str,
        default="Simplified Chinese",
        help="target language to translate to",
    )
    options = parser.parse_args()
    OPENAI_API_KEY = options.openai_key or os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise Exception("Please provide your OpenAI API key")
    return options


def process_file(file_path, options):
    """Translate a single text file"""
    if not file_path.suffix.lower() in ALLOWED_FILE_TYPES:
        raise Exception("Please use a txt file")
    # if file ends with _translated.txt or _bilingual.txt, skip it
    if file_path.stem.endswith("_translated"):
        print(f"You already have a translated file for {file_path}, skipping...")
        return
    elif file_path.stem.endswith("_bilingual"):
        print(f"You already have a bilingual file for {file_path}, skipping...")
        return
    print(f"Translating {file_path}...")
    # if there is any txt file ending with _translated.txt or _bilingual.txt, skip it
    if (file_path.with_name(f"{file_path.stem}_translated{file_path.suffix}").exists()
            and not options.bilingual):
        print(f"You already have a translated file for {file_path}, skipping...")
        return
    elif (file_path.with_name(f"{file_path.stem}_bilingual{file_path.suffix}").exists()
            and options.bilingual):
        print(f"You already have a bilingual file for {file_path}, skipping...")
        return
    translate_text_file(str(file_path), options)


def process_folder(folder_path, options):
    """Translate all text files in a folder"""
    for file_path in folder_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in ALLOWED_FILE_TYPES:
            process_file(file_path, options)


def main():
    """Main function"""
    options = parse_arguments()
    input_path = Path(options.input_path)
    if not input_path.exists():
        raise Exception("Input path does not exist")
    if input_path.is_dir():
        # input path is a folder, scan and process all allowed file types
        process_folder(input_path, options)
    elif input_path.is_file():
        process_file(input_path, options)


if __name__ == "__main__":
    main()
