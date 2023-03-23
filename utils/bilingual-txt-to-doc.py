from docx import Document
from docx.shared import Pt, Length
from langdetect import detect



def is_chinese(text):
    detected_lang = detect(text)
    return detected_lang == 'zh-cn' or detected_lang == 'zh-tw'


def convert_bilingual_txt_to_doc(txt_file, doc_file):
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    paragraphs = content.split('\n')
    document = Document()




    for p in paragraphs:
        paragraph = document.add_paragraph(p)
        if is_chinese(p):
            style = document.styles['Normal']
            font = style.font
            font.name = 'Arial'
            font.size = Pt(12)
            print('chinese: ')
            paragraph.style = document.styles['Normal']
        else:
            style = document.styles['Normal']
            font = style.font
            font.name = 'Arial'
            font.size = Pt(9)i
            print('not chinese: ')
            paragraph.style = document.styles['Normal']
    
    document.save(doc_file)

# Example usage
convert_bilingual_txt_to_doc('../input_bilingual.txt', '../input_bilingual.docx')
