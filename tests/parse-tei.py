import os
import regex
from lxml import etree


def extract_paper_info(file_path):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_path, parser=parser)
    root = tree.getroot()

    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    titles = root.xpath("//tei:titleStmt/tei:title", namespaces=ns)
    abstract = root.xpath("//tei:profileDesc/tei:abstract/tei:div/tei:p", namespaces=ns)
    divs = root.xpath("//tei:body/tei:div", namespaces=ns)

    output_file_path = f"{os.path.splitext(file_path)[0]}_extracted.txt"
    with open(output_file_path, 'w') as output_file:
        output_file.write("Title(s):\n")
        for title in titles:
            output_file.write(f"{title.text}")

        output_file.write("\nAbstract:\n")
        for abs in abstract:
            output_file.write(f"{etree.tostring(abs, method='text', encoding='unicode')}\n")

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

extract_paper_info("chapter3.pdf.tei.xml")
