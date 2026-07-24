from pypdf import PdfReader
from docx import Document


def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text = text + page.extract_text() + "\n"
    return text


def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text = text + paragraph.text  + "\n"
        
    return text


if __name__ == "__main__":
    faq_text = read_txt("data/hearthstone_faq.txt")
    policy_text = read_pdf("data/returns_and_shipping_policy.pdf")
    guide_text = read_docx("data/brewing_guide.docx")

    print(f"FAQ: {len(faq_text)} characters")
    print(f"Policy: {len(policy_text)} characters")
    print(f"Guide: {len(guide_text)} characters")
  