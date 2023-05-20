import re
from tqdm import tqdm
from bs4 import BeautifulSoup
from . import scipdf
import requests
import grobid_tei_xml
import concurrent.futures
import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from pprint import pprint
import warnings
from bs4 import GuessedAtParserWarning
warnings.filterwarnings('ignore', category=GuessedAtParserWarning)
import re
import nltk
nltk.download('punkt')


def parse_pdf_from_server(pdf_path):

    url = 'https://kermitt2-grobid.hf.space/api/processFulltextDocument'

    with open(pdf_path, 'rb') as file:
        files = {'input': file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        parsed_article = response.text
        return parsed_article
    else:
        print(f"Error: {response.status_code}")
        return None


def tidy_parsed_article_to_dict_using_sci_pdf(parsed_article):
    article_dict = scipdf.convert_article_soup_to_dict(
        BeautifulSoup(parsed_article, "lxml"), as_list=False)
    return article_dict


def tidy_parsed_article_to_dict_using_grobid_tei_xml(parsed_article):
    doc = grobid_tei_xml.parse_document_xml(parsed_article)
    return doc.to_dict()


def extract_pdf_content_as_dict(pdf_path, parser):
    parsed_article = parse_pdf_from_server(pdf_path)
    if parser == 'scipdf':
        article_dict = tidy_parsed_article_to_dict_using_sci_pdf(
            parsed_article)
    elif parser == 'grobid_tei_xml':
        article_dict = tidy_parsed_article_to_dict_using_grobid_tei_xml(
            parsed_article)
    return article_dict


def convert_pdf_dict_into_string(pdf_dict):
    """Extracts the contents of a PDF dict into a list of paragraphs."""
    contents = []
    title = pdf_dict["title"]
    authors = pdf_dict["authors"]
    pub_date = pdf_dict["pub_date"]
    abstract = pdf_dict["abstract"]
    contents.extend([title, authors, pub_date, abstract])

    for section in pdf_dict['sections']:
        contents.append(section['heading'])
        contents.append(section['text'])

    contents.append("References")
    for ref in pdf_dict['references']:
        title = ref['title']
        journal = ref['journal']
        year = ref['year']
        authors = ref['authors']
        ref_complete = f"{authors}; {year}; {title};{journal}"
        contents.append(ref_complete)

    # remove empty lines
    contents = [x for x in contents if x]
    return "\n".join(contents)




def split_fist_joined_text(text):
    '''
    sometimes the first paragraph in the body content would be joined with the abstract.
    This function corrects such cases.
    '''

    # Find the index of "Abstract"
    abstract_index = text.lower().find("abstract")

    if abstract_index != -1:
        abstract_end = abstract_index + len("abstract")
        first_paragraph = text[:abstract_end]
        remaining_text = text[abstract_end:].strip()

        paragraphs = remaining_text.split("\n", 1)

        if len(paragraphs) > 1:
            first_body_paragraph, second_body_paragraph = paragraphs
            first_body_paragraph = first_body_paragraph.strip()
            second_body_paragraph = second_body_paragraph.strip()

            # Case 1: Find the index of the first period followed by a character instead of a space
            match = re.search('\.\w', first_body_paragraph)

            if match:
                split_index = match.start() + 1
                truncated_part = first_body_paragraph[split_index:].strip()
                first_body_paragraph = first_body_paragraph[:split_index]
                second_body_paragraph = f"{truncated_part} {second_body_paragraph}"
                return f"{first_paragraph}\n{first_body_paragraph}\n{second_body_paragraph}"

            # Case 2: Second paragraph starts with a lowercase letter
            if second_body_paragraph and second_body_paragraph[0].islower():
                sentences = nltk.sent_tokenize(first_body_paragraph)
                if len(sentences) > 1:
                    last_sentence = sentences[-1]
                    first_body_paragraph = first_body_paragraph[:-len(last_sentence)].rstrip()
                    second_body_paragraph = f"{last_sentence} {second_body_paragraph}"

                return f"{first_paragraph}\n{first_body_paragraph}\n{second_body_paragraph}"

    # Return the original text
    return text



def write_extracted_pdf_to_file(string, file_path):
    new_file_path = Path(file_path).with_name(
        Path(file_path).stem + "_extracted.txt")
    # replace two and more newlines with one newline
    string = re.sub(r'\n{2,}', '\n', string)
    if not new_file_path.exists():
        with open(new_file_path, "w") as f:
            f.write(string)
    else:
        print(f"Skipping {file_path} as the extracted file already exists.")


def process_pdf_file(pdf_filepath, parser):
    article_dict = extract_pdf_content_as_dict(pdf_filepath, parser=parser)
    article_string = convert_pdf_dict_into_string(article_dict)
    cleaned_article_string = split_fist_joined_text(article_string)
    write_extracted_pdf_to_file(cleaned_article_string, pdf_filepath)


def process_pdfs(input_path, parser='scipdf'):
    input_path = Path(input_path)
    print(f"Processing {input_path} using {parser} parser.")
    if input_path.is_file() and input_path.suffix == '.pdf':
        pdf_filepaths = [input_path]
    elif input_path.is_dir():
        pdf_filepaths = list(input_path.glob('*.pdf'))
    else:
        raise ValueError(
            "Invalid input path. Must be a PDF file or a directory containing PDF files.")

    # Filter out PDFs that have already been extracted
    pdf_filepaths = [pdf_filepath for pdf_filepath in pdf_filepaths if not Path(
        pdf_filepath).with_name(Path(pdf_filepath).stem + "_extracted.txt").exists()]

    # Collect PDFs that do not have corresponding extracted txt files
    not_extracted_pdfs = []

    with tqdm(total=len(pdf_filepaths), position=0, leave=True) as pbar:
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(
                process_pdf_file, pdf_filepath, parser): pdf_filepath for pdf_filepath in pdf_filepaths}
            for future in concurrent.futures.as_completed(futures):
                pdf_filepath = futures[future]
                pbar.update(1)
                try:
                    future.result()
                except Exception as e:
                    print(f"Failed to extract {pdf_filepath}: {e}")
                    not_extracted_pdfs.append(pdf_filepath)

    # Print PDFs without corresponding extracted txt files
    if not_extracted_pdfs:
        print("\nHere are PDFs without extracted txt files. You want to make sure 1. these files are OCRed 2. They are not corrupted:")
        for pdf in not_extracted_pdfs:
            print(pdf.stem)

