from sentence_transformers import SentenceTransformer, util
from src.chunking import chunk_text
from src.ingestion import read_txt, read_pdf, read_docx
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_data():
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

    embeddings = model.encode(texts)

    return all_chunks, embeddings


def answer_question(question, all_chunks, embeddings):
    question_embedding = model.encode(question)

    scores = util.cos_sim(question_embedding, embeddings)
    best_index = scores.argmax().item()
    best_score = scores[0][best_index].item()
    best_chunk = all_chunks[best_index]

    if best_score < 0.35:
        return "Sorry, I could not find that in the Hearthstone documents.", None, best_score

    prompt = f"""Answer the question using only the context below.
If the context does not contain the answer, say you do not know.

Context:
{best_chunk["text"]}

Question: {question}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    return answer, best_chunk["source"], best_score


if __name__ == "__main__":
    all_chunks, embeddings = load_data()
    question = "How long do I have to return coffee?"
    answer, source, score = answer_question(question, all_chunks, embeddings)
    print(f"Score: {score:.2f}")
    print(f"Source: {source}")
    print(answer)