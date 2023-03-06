# ChatGPT for Translation
This is a simple tool that uses ChatGPT to translate text into a specified target language. The program takes a text file (`.txt` or `.md`)as input, and outputs a **translated** text file or a **bilingual** text file with the original and translated text side by side.



## Example

`python ChatGPT-translate.py --input_file input.txt --openai_key=your_key --target_lang="Simplified Chinese"`

This command will translate the text in input.txt into Simplified Chinese using ChatGPT. You can also specify any language you want. For example, `--target_lang="Japanese"`.


`python ChatGPT-translate.py --input_file input.txt --openai_key=your_key --bilingual --num_threads 5 --target_lang="Simplified Chinese"`

This command will translate the text in input.txt into Simplified Chinese using ChatGPT, using 5 threads for translation. The output will be a bilingual text file with the original and translated text side by side.

## Prerequisites
Python
OpenAI API key (https://beta.openai.com/signup/)

## Installation
Clone the repository: git clone https://github.com/Raychanan/ChatGPT-Translation.git

Install the required packages: pip install -r requirements.txt

Set up your OpenAI API key by adding it to the --openai_key argument or setting it as an environment variable (export OPENAI_API_KEY=<your_key>)
Usage

## Usage
`python translate.py [--input_file INPUT_FILE] [--openai_key OPENAI_KEY] [--no_limit] [--num_threads NUM_THREADS] [--bilingual] [--target_lang TARGET_LANG]`

Arguments
```
--input_file: Path to the input text file to be translated (required).
--openai_key: Your OpenAI API key (required).
--no_limit: Set this flag to disable the limit on the number of threads used for translation.
--num_threads: The number of threads to use for translation (default: 10).
--bilingual: Set this flag to output a bilingual text file with the original and translated text side by side.
--target_lang: The target language to translate to (default: Simplified Chinese).
```
