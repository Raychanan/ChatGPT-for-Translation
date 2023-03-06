from tqdm import tqdm
import argparse
import time
from os import environ as env
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import openai


ALLOWED_FILE_TYPES = [".txt", ".md", ]

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
                        f"Translate the following text into {self.target_lang} in a way that is faithful to the original text (but do not translate people's names). Return only translations and nothing else:\n {text}",
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file",
        dest="input_file",
        type=str,
        help="input file to translate",
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
        default=10,
        help="number of threads to use for translation",
    )
    parser.add_argument(
        "--bilingual",
        dest="bilingual",
        action="store_true",
        default=False,
        help=
        "output bilingual txt file with original and translated text side by side",
    )
    parser.add_argument(
        "--target_lang",
        dest="target_lang",
        type=str,
        default="Simplified Chinese",
        help="target language to translate to",
    )

    options = parser.parse_args()
    OPENAI_API_KEY = options.openai_key or env.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise Exception("Please provide your OpenAI API key")
    if not options.input_file.endswith(".txt"):
        raise Exception("please use a txt file")
    with open(options.input_file, "r") as f:
        text = f.read()
        translator = ChatGPT(OPENAI_API_KEY, options.target_lang)
        paragraphs = [p.strip() for p in text.split("\n") if p.strip() != ""]

    with ThreadPoolExecutor(max_workers=options.num_threads) as executor:
        translated_paragraphs = list(
            tqdm(executor.map(translator.translate, paragraphs),
                total=len(paragraphs),
                desc="Translating paragraphs",
                unit="paragraph"))
        translated_paragraphs = [p.strip() for p in translated_paragraphs]

    translated_text = "\n".join(translated_paragraphs)

    if options.bilingual:
        bilingual_text = "\n".join(f"{paragraph}\n{translation}"
                                   for paragraph, translation in zip(
                                       paragraphs, translated_paragraphs))
        output_file = f"{Path(options.input_file).parent}/{Path(options.input_file).stem}_bilingual.txt"
        with open(output_file, "w") as f:
            f.write(bilingual_text)
            print(f"Bilingual text saved to {f.name}.")
    else:
        output_file = f"{Path(options.input_file).parent}/{Path(options.input_file).stem}_translated.txt"
        with open(output_file, "w") as f:
            f.write(translated_text)
            print(f"Translated text saved to {f.name}.")