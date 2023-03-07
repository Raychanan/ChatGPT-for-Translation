# ChatGPT for Translation | ChatGPT用于翻译
This is a simple tool that uses ChatGPT to translate text into a specified target language **in a faithful and accurate manner**. The tool takes a text file (`.txt` or `.md`)as input, and outputs a **translated** text file or a **bilingual** text file with the original and translated text side by side. This tool automatically sets multi-threading (to speed up your translation process) and automatically considers the frequency limit set by ChatGPT for users.

使用ChatGPT将文本以**忠于原味的方式**翻译成指定的目标语言。该工具接受一个文本文件（`.txt`, `.md`或`.rtf`）作为输入，并生成一个**直接翻译**后的文本文件或一个**双语的**(并列显示原始文本和翻译文本)文本文件。这个工具默认自动设置了多线程(加速你的翻译过程)、自动考虑了ChatGPT给用户设置的频率限制。

Use this tool on Google Colab (recommended): https://colab.research.google.com/drive/1_715zHeS3VaZaB9ISyo29Zp-KOTsyP8D?usp=sharing

在 Google Colab 上使用此工具（推荐）：https://colab.research.google.com/drive/1_715zHeS3VaZaB9ISyo29Zp-KOTsyP8D?usp=sharing

## Simple Example | 简单例子

```
git clone https://github.com/Raychanan/ChatGPT-for-Translation.git
cd ./ChatGPT-for-Translation/
pip install -r requirements.txt --quiet
python ChatGPT-translate.py --input_path=input.txt --openai_key=password --target_lang="Chinese"`
```

This command will translate the text in input.txt into Simplified Chinese using ChatGPT. You can also specify any language you want. For example, `--target_lang="Japanese"`. See this txt as an [example](input_translated.txt).

这个命令将使用ChatGPT把`input.txt`中的文本翻译成简体中文。你也可以指定任何你想要的语言。例如，`--target_lang="Japanese"`。翻译后的txt文件例子见[这里](input_translated.txt)

## Translate Folder Files | 翻译文件夹内所有的文本文件

`python ChatGPT-translate.py --input_path=./folder/ --openai_key=password --target_lang="Chinese"`


## Bilingual Translation Example | 双语翻译例子

`python ChatGPT-translate.py --input_path=input.txt --openai_key=password --target_lang="Japanese"`


This command will translate the text in input.txt into Simplified Chinese using ChatGPT, using 20 threads (10 by default) for translation. The output will be a bilingual text file with the original and translated text side by side. See this txt as an [example](input_bilingual.txt)

这个命令将使用ChatGPT把input.txt中的文本翻译成简体中文，使用20个线程（默认为5个）进行翻译。输出结果将是一个双语文本文件，其中并列着原始文本和翻译文本。双语翻译后的txt文件例子见[这里](input_bilingual.txt)。


## Speed up Translation | 加速翻译过程

`python ChatGPT-translate.py --input_path=input.txt --openai_key=password --bilingual --num_threads 20 --target_lang="Traditional Chinese"`


## Prerequisites | 要求
You need a OpenAI API key (https://beta.openai.com/signup/)

你需要一个OpenAI的API密钥（https://beta.openai.com/signup/）


## Arguments | 可用参数
```
--input_path= Path to the input text file to be translated (required).
--openai_key: Your OpenAI API key (required).
--no_limit: Set this flag to disable the limit on the number of threads used for translation.
--num_threads: The number of threads to use for translation (default: 10).
--bilingual: Set this flag to output a bilingual text file with the original and translated text side by side.
--target_lang: The target language to translate to (default: Simplified Chinese).
```
