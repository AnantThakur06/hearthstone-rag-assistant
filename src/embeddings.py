from sentence_transformers import SentenceTransformer, util
from chunking import chunk_text
from ingestion import read_txt, read_pdf, read_docx

model = SentenceTransformer("all-MiniLM-L6-v2")


if __name__ == "__main__":
    faq_text = read_txt("data/hearthstone_faq.txt")
    pieces = chunk_text(faq_text, "hearthstone_faq.txt")
    policy_text = read_pdf("data/returns_and_shipping_policy.pdf")
    policy_pieces = chunk_text(policy_text, "returns_and_shipping_policy.pdf")
    guide_text = read_docx("data/brewing_guide.docx")
    guide_pieces = chunk_text(guide_text, "brewing_guide.docx")
    all_chunks = pieces + policy_pieces + guide_pieces

    texts = []
    for chunk in all_chunks:
        texts.append(chunk["text"])

    print(f"Total texts: {len(texts)}")

    embeddings = model.encode(texts)
    print(embeddings.shape)

    question = "How long do I have to return coffee?"
    question_embedding = model.encode(question)

    scores = util.cos_sim(question_embedding, embeddings)
    best_index = scores.argmax().item()

    best_chunk = all_chunks[best_index]

    print("--- QUESTION ---")
    print(question)
    print("--- BEST CHUNK ---")
    print(best_chunk["text"])
    print("--- SOURCE ---")
    print(best_chunk["source"])