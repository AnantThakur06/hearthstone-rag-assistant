from pypdf import PdfReader

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        print(f"--- PAGE ---")
        print(page_text[:80])
        text = text + page_text
    return text

read_pdf("data/returns_and_shipping_policy.pdf")