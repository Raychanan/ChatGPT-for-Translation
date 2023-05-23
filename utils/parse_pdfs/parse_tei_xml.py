import os
import regex
import requests
from lxml import etree

def save_xml_to_file(pdf_path, xml_source):
    base_path = os.path.splitext(pdf_path)[0] # strip the extension from the file path
    xml_file_path = f"{base_path}.tei.xml" # append the custom extension

    with open(xml_file_path, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_source)

    print(f"XML source saved to {xml_file_path}")

def parse_pdf_from_server(pdf_path):
    url = 'https://kermitt2-grobid.hf.space/api/processFulltextDocument'

    with open(pdf_path, 'rb') as file:
        files = {'input': file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        xml_source = response.text
        # save_xml_to_file(pdf_path, xml_source)
        return xml_source
    else:
        print(f"Error: {response.status_code}")
        return None
    
def extract_paper_info(pdf_path):
    xml_source = parse_pdf_from_server(pdf_path)
    if xml_source is None:
        return

    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(xml_source.encode('utf-8'), parser=parser)  # use fromstring here

    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    titles = root.xpath("//tei:titleStmt/tei:title", namespaces=ns)
    abstract = root.xpath("//tei:profileDesc/tei:abstract/tei:div/tei:p", namespaces=ns)
    divs = root.xpath("//tei:body/tei:div", namespaces=ns)

    output_file_path = f"{os.path.splitext(pdf_path)[0]}_extracted.txt"
    with open(output_file_path, 'w') as output_file:
        output_file.write("Title(s):\n")
        for title in titles:
            output_file.write(f"{title.text}\n")

        output_file.write("\nAbstract:\n")
        for abs_part in abstract:
            output_file.write(f"{etree.tostring(abs_part, method='text', encoding='unicode')}\n")

        for div in divs:
            heading = div.xpath("tei:head", namespaces=ns)
            heading_number = div.xpath("tei:head/@n", namespaces=ns)
            paragraphs = div.xpath("tei:p", namespaces=ns)

            if heading:
                if heading_number:
                    output_file.write(f"{heading_number[0]} {heading[0].text}\n")
                else:
                    heading_text = heading[0].text
                    if len(heading_text) >= 2: # ignore one-letter capital style paragraph
                        output_file.write(f"{heading_text}\n")
            if paragraphs:
                for para in paragraphs:
                    # Set the text content of the ref elements with type="foot" to an empty string
                    for ref in para.xpath(".//tei:ref[@type='foot']", namespaces=ns):
                        ref.text = ""
                    
                    text = etree.tostring(para, method='text', encoding='unicode')

                    # Remove footnotes in plain text format with a regex
                    text = regex.sub(r'(?<=\.|")\s\d+(?=\s[A-Z])', '', text)

                    output_file.write(f"{text}\n")

    print(f"Extraction completed, results saved in {output_file_path}")


pdf_path = "/Users/raychan/Downloads/GitHub/ChatGPT-for-Translation/tests/chapter6.pdf"
# print(parse_pdf_from_server(pdf_path))
extract_paper_info(pdf_path)
