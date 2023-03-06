# ChatGPT for Translation | ChatGPT用于翻译
This is a simple tool that uses ChatGPT to translate text into a specified target language. The program takes a text file (`.txt` or `.md`)as input, and outputs a **translated** text file or a **bilingual** text file with the original and translated text side by side.

使用ChatGPT将文本翻译成指定的目标语言。该程序接受一个文本文件（`.txt`或`.md`）作为输入，并输出一个**翻译的**文本文件或一个**双语的**文本文件，并列显示原始文本和翻译文本。


Use this tool on Google Colab (recommended): https://colab.research.google.com/drive/1_715zHeS3VaZaB9ISyo29Zp-KOTsyP8D?usp=sharing

在 Google Colab 上使用此工具（推荐）：https://colab.research.google.com/drive/1_715zHeS3VaZaB9ISyo29Zp-KOTsyP8D?usp=sharing

## Simple Example | 简单例子

```
git clone https://github.com/Raychanan/ChatGPT-for-Translation.git
cd ./ChatGPT-for-Translation/
pip install -r requirements.txt --quiet
python ChatGPT-translate.py --input_file input.txt --openai_key=your_key --target_lang="Chinese"`
```

This command will translate the text in input.txt into Simplified Chinese using ChatGPT. You can also specify any language you want. For example, `--target_lang="Japanese"`.

这个命令将使用ChatGPT把`input.txt`中的文本翻译成简体中文。你也可以指定任何你想要的语言。例如，`--target_lang="Japanese"`。

## Bilingual Translation Example | 双语翻译例子


`python ChatGPT-translate.py --input_file input.txt --openai_key=your_key --bilingual --num_threads 20 --target_lang="Chinese"`

This command will translate the text in input.txt into Simplified Chinese using ChatGPT, using 20 threads (10 by default) for translation. The output will be a bilingual text file with the original and translated text side by side.

这个命令将使用ChatGPT把input.txt中的文本翻译成简体中文，使用20个线程（默认为10个）进行翻译。输出结果将是一个双语文本文件，其中并列着原始文本和翻译文本。


## Prerequisites | 要求
You need a OpenAI API key (https://beta.openai.com/signup/)

你需要一个OpenAI的API密钥（https://beta.openai.com/signup/）

## Usage 使用方法
`python translate.py [--input_file INPUT_FILE] [--openai_key OPENAI_KEY] [--no_limit] [--bilingual] [--target_lang=TARGET_LANG] [--num_threads NUM_THREADS]`

## Arguments | 可用参数
```
--input_file: Path to the input text file to be translated (required).
--openai_key: Your OpenAI API key (required).
--no_limit: Set this flag to disable the limit on the number of threads used for translation.
--num_threads: The number of threads to use for translation (default: 10).
--bilingual: Set this flag to output a bilingual text file with the original and translated text side by side.
--target_lang: The target language to translate to (default: Simplified Chinese).
```
