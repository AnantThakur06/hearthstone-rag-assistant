from ingestion import read_txt, read_pdf, read_docx


def chunk_text(text, source, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        piece = text[start:end]
        chunks.append({"text": piece, "source": source})
        start = start + chunk_size - overlap

    return chunks


if __name__ == "__main__":
    faq_text = read_txt("data/hearthstone_faq.txt")
    pieces = chunk_text(faq_text, "hearthstone_faq.txt")
    print(f"FAQ produced {len(pieces)} chunks")
    print("--- first chunk ---")
    print(pieces[0]["source"])