from sentence_transformers import SentenceTransformer, util
from chunking import chunk_text
from ingestion import read_txt, read_pdf, read_docx
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

    # question = "What water temperature should I use for brewing?"
    # question = "Do you ship to India?"
    # question = "What is the capital of France?"
    question = "How long do I have to return coffee?"
    question_embedding = model.encode(question)

    scores = util.cos_sim(question_embedding, embeddings)
    best_index = scores.argmax().item()
    best_score = scores[0][best_index].item()
    print(f"Score: {best_score:.2f}")
    best_chunk = all_chunks[best_index]

    if best_score < 0.35:
        print("Sorry, I could not find that in the Hearthstone documents.")
    else:
        print("--- QUESTION ---")
        print(question)
        print("--- SOURCE ---")
        print(best_chunk["source"])

        prompt = f"""Answer the question using only the context below.
If the context does not contain the answer, say you do not know.

Context:
{best_chunk["text"]}

Question: {question}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        print("--- ANSWER ---")
        print(response.choices[0].message.content)