import os

from lxml import etree


def extract_paper_info(file_path):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_path, parser=parser)
    root = tree.getroot()

    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    titles = root.xpath("//tei:titleStmt/tei:title", namespaces=ns)
    abstract = root.xpath("//tei:profileDesc/tei:abstract/tei:div/tei:p", namespaces=ns)
    divs = root.xpath("//tei:body/tei:div", namespaces=ns)

    # Open the output file
    output_file_path = f"{os.path.splitext(file_path)[0]}_extracted.txt"
    with open(output_file_path, 'w') as output_file:
        output_file.write("Title(s):\n")
        for title in titles:
            output_file.write(f"{title.text}\n")

        output_file.write("\nAbstract:\n")
        for abs in abstract:
            output_file.write(f"{etree.tostring(abs, method='text', encoding='unicode')}\n")

        for div in divs:
            # Modified XPath expression to match any <head> element
            heading = div.xpath("tei:head", namespaces=ns)
            paragraphs = div.xpath("tei:p", namespaces=ns)

            if heading:
                output_file.write(f"{heading[0].text}\n")
            if  paragraphs:
                for para in paragraphs:
                    text = etree.tostring(para, method='text', encoding='unicode')
                    output_file.write(f"{text}\n")

    print(f"Extraction completed, results saved in {output_file_path}")

extract_paper_info("ps-sample.pdf.tei.xml")