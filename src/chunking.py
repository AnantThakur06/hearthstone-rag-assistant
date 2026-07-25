from ingestion import read_txt, read_pdf, read_docx



def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []          # empty bucket for the pieces
    start = 0            # where the current piece begins

    while start < len(text):
        end = start + chunk_size
        piece = text[start:end]
        chunks.append(piece)
        start = start + chunk_size - overlap

    return chunks


if __name__ == "__main__":
    faq_text = read_txt("data/hearthstone_faq.txt")
    pieces = chunk_text(faq_text)
    print(f"FAQ produced {len(pieces)} chunks")
    print("--- first chunk ---")
    print(pieces[0])