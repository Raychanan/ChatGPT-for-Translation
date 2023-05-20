# ChatGPT for Translation | ChatGPT用于翻译
Use ChatGPT to translate text faithfully to the original. This tool accepts a text file (`.pdf`, `.txt`, `.md`, `.html`, or `.rtf`) or a folder containing text. It will generate both a **direct translation** and a **bilingual** text file. Special optimizations have been made for academic paper PDF parsing and translation.

使用ChatGPT将文本以忠于原文的方式完成翻译。该工具接受一个文本文件（`.pdf`, `.txt`, `.md`, `.html`或`.rtf`）或者一个包含文本的文件夹。它将生成一个**直接翻译**和一个**双语**文本文件。尤其对于学术论文 PDF 解析和翻译做了特别的优化。

Use this on Google Colab (recommended). See [here](https://colab.research.google.com/drive/1_715zHeS3VaZaB9ISyo29Zp-KOTsyP8D#scrollTo=hU-8gsBXAyf0)

Google Colab上使用这个工具(推荐)。见[这里](https://colab.research.google.com/drive/1_715zHeS3VaZaB9ISyo29Zp-KOTsyP8D#scrollTo=hU-8gsBXAyf0)

## Simple Example | 简单例子

```
# Install
git clone https://github.com/Raychanan/ChatGPT-for-Translation.git
cd ./ChatGPT-for-Translation/
pip install -r requirements.txt --quiet

# Run
python ChatGPT-translate.py --input_path=input.txt --openai_key=password
```

This command will translate the text in input.txt into simplified Chinese using ChatGPT. You can also specify any language you want. For example, `--target_language="Japanese"`. See this txt as an [example](input_translated.txt).

这个命令将使用ChatGPT把`input.txt`中的文本翻译成简体中文。你也可以指定任何你想要的语言。例如，`--target_language="Japanese"`。翻译后的txt文件例子见[这里](input_translated.txt)

## Translate All Files Within the Folder | 翻译文件夹内所有文本文件

`python ChatGPT-translate.py --input_path=./folder/ --openai_key=password`

## Other Examples | 其它例子

Azure:
```
python ChatGPT-translate.py --input_path=input.pdf --use_azure --azure_endpoint=endpoint_uri --azure_deployment_name=deployment_name --openai_key=your_AOAI_key
```

GPT-4:
```
python ChatGPT-translate.py --input_path=input.txt --model=gpt-4 --openai_key=password
```


## Prerequisites | 要求
You need a OpenAI API key (https://beta.openai.com/signup/)

你需要一个OpenAI的API密钥（https://beta.openai.com/signup/）


## Arguments | 可用参数
```
--num_threads: The number of threads to use for translation (default: 10).
--only_process_this_file_extension. For example, set only_process_this_file_extension="txt".
--not_to_translate_references. By default, not to translate references.
```

## Acknowledge 
PDF parser is based on [scipdf](https://github.com/titipata/scipdf_parser) project on Github. Some adjustments were done to allow users to parse PDFs without having to initialzing a server locally.
