# ChatGPT用于翻译
使用ChatGPT将文本翻译成指定的目标语言。该程序接受一个文本文件（`.txt`或`.md`）作为输入，并输出一个**翻译的**文本文件或一个**双语的**文本文件，并列显示原始文本和翻译文本。

在Google Colab上使用这个工具（推荐）：https://colab.research.google.com/drive/1_715zHeS3VaZaB9ISyo29Zp-KOTsyP8D?usp=sharing

## 例子

```
git clone https://github.com/Raychanan/ChatGPT-for-Translation.git
cd ./ChatGPT-for-Translation/
pip install -r requirements.txt --quiet
python ChatGPT-translate.py --input_file input.txt --openai_key=your_key --target_lang="Chinese"。
```

这个命令将使用ChatGPT把`input.txt`中的文本翻译成简体中文。你也可以指定任何你想要的语言。例如，`--target_lang="Japanese"`。


`python ChatGPT-translate.py --input_file input.txt --openai_key=your_key --bilingual --num_threads 20 --target_lang="简体中文"`。

这个命令将使用ChatGPT把input.txt中的文本翻译成简体中文，使用20个线程（默认为10个）进行翻译。输出结果将是一个双语文本文件，其中并列着原始文本和翻译文本。

## 要求
你需要一个OpenAI的API密钥（https://beta.openai.com/signup/）。

## 使用方法
`python translate.py [--input_file INPUT_FILE] [--openai_key OPENAI_KEY] [--no_limit] [--bilingual] [--target_lang=TARGET_LANG] [--num_threads NUM_THREADS]`。

## 额外可用参数

```
--input_file: 要翻译的输入文本文件的路径（需要）。
--openai_key: 你的OpenAI API密钥（需要）。
--no_limit: 设置这个标志可以禁用翻译所用的线程数限制。
--num_threads: 用于翻译的线程数（默认：10）。
--bilingual: 设置这个标志，以输出一个双语文本文件，并排显示原始文本和翻译文本。
--target_lang: 要翻译的目标语言（默认：简体中文）。
```
