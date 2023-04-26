# ChatGLM for Translation | ChatGLM用于翻译
This is a simple tool that uses ChatGPT to translate text into a specified target language **in a faithful way to the original**. The tool takes a text file (`.pdf`, `.txt`, `.md`,  `.html` and `.rtf`) or a folder of text files as input, and outputs a **translated** text file or a **bilingual** text file with the original and translated text side by side. Special optimization has been done especially for academic paper PDF parsing and translation.

使用ChatGPT将文本以**忠于原文的方式**翻译成指定的目标语言。该工具接受一个文本文件（`.pdf`, `.txt`, `.md`, `.html`或`.rtf`）或者一个包含文本的文件夹，并生成一个**直接翻译**后的文本或一个**双语的**(并列显示原始文本和翻译文本)文本。尤其对于学术论文 PDF 解析和翻译做了特别的优化。

使用[chatglm-openai-api](https://github.com/ninehills/chatglm-openai-api)部署本地ChatGLM API

```
export OPENAI_API_BASE="http://localhost:8000/v1"
```

Use this on Google Colab (recommended). See [here](https://colab.research.google.com/drive/1_715zHeS3VaZaB9ISyo29Zp-KOTsyP8D#scrollTo=hU-8gsBXAyf0)

Google Colab上使用这个工具(推荐)。见[这里](https://colab.research.google.com/drive/1_715zHeS3VaZaB9ISyo29Zp-KOTsyP8D#scrollTo=hU-8gsBXAyf0)

Note: Use absolute paths instead of relative paths to process PDFs.

注意：处理 PDF 的时候使用绝对路径而不是相对路径。

## Simple Example | 简单例子

```
git clone https://github.com/Raychanan/ChatGPT-for-Translation.git
cd ./ChatGPT-for-Translation/
pip install -r requirements.txt --quiet

# for windows
spacy download en



python ChatGPT-translate.py --input_path=input.txt --openai_key=password

# chatglm
python .\ChatGPT-translate.py --input_path=input.txt --use_chatglm --endpoint=http://localhost:8000/v1 --opeanai_key="token1"

```

This command will translate the text in input.txt into simplified Chinese using ChatGPT. You can also specify any language you want. For example, `--target_language="Japanese"`. See this txt as an [example](input_translated.txt).

这个命令将使用ChatGPT把`input.txt`中的文本翻译成简体中文。你也可以指定任何你想要的语言。例如，`--target_language="Japanese"`。翻译后的txt文件例子见[这里](input_translated.txt)


```
# Azure's OpenAI service, use this:
python ChatGPT-translate.py --input_path=input.txt --use_azure --azure_endpoint=endpoint_uri --azure_deployment_name=deployment_name --openai_key=your_AOAI_key
```


## Translate Folder Files | 翻译文件夹内所有的文本文件

`python ChatGPT-translate.py --input_path=./folder/ --openai_key=password`


## Bilingual Translation Example | 双语翻译例子

`python ChatGPT-translate.py --bilingual --input_path=input.txt --openai_key=password`

## Prerequisites | 要求
You need a OpenAI API key (https://beta.openai.com/signup/)

你需要一个OpenAI的API密钥（https://beta.openai.com/signup/）
或部署了[chatglm-openai-api](https://github.com/ninehills/chatglm-openai-api)


## Arguments | 可用参数
```
--num_threads: The number of threads to use for translation (default: 5).
--only_process_this_file_extension For example, set only_process_this_file_extension="txt"
--not_to_translate_people_names Whether or not to translate names in the text. This can be useful if you are translating academic texts. By default, names will be translated.
--not_to_translate_references By default, not to translate references.
--keep_first_two_paragraphs Keep the first three paragraphs of the original text. By default, false.
```

## Acknowledge 
PDF parser is based on [scipdf](https://github.com/titipata/scipdf_parser) project on Github. Some adjustments were done to allow users to parse PDFs without having to initialzing a server locally.
