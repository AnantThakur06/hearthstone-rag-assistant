from src.ingestion import read_txt, read_pdf, read_docx


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
    policy_text = read_pdf("data/returns_and_shipping_policy.pdf")
    policy_pieces = chunk_text(policy_text, "returns_and_shipping_policy.pdf")
    guide_text = read_docx("data/brewing_guide.docx")   
    guide_pieces = chunk_text(guide_text, "brewing_guide.docx")
    all_chunks = pieces + policy_pieces + guide_pieces
    print(f"Total chunks: {len(all_chunks)}")
    print(all_chunks[0]["source"])
    print(all_chunks[-1]["source"])
    # print(f"FAQ produced {len(pieces)} chunks")
    # print("--- first chunk ---")
    # print(pieces[0]["source"])