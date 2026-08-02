import streamlit as st
from src.embeddings import load_data, answer_question

st.title("Hearthstone Coffee Assistant")
st.caption("Try asking:")
st.caption("• How long do I have to return coffee?")
st.caption("• What water temperature should I use?")
st.caption("• Do you ship to India?")

all_chunks, embeddings = load_data()

question = st.text_input("Ask a question about our coffee:")

if question:
    answer, source, score = answer_question(question, all_chunks, embeddings)
    st.write(answer)
    if source:
        st.caption(f"Source: {source}")

st.divider()
st.subheader("Source documents")

with open("data/returns_and_shipping_policy.pdf", "rb") as f:
    st.download_button("Returns & shipping policy (PDF)", f, "returns_policy.pdf")

with open("data/hearthstone_faq.txt", "rb") as f:
    st.download_button("FAQ (TXT)", f, "hearthstone_faq.txt")

with open("data/brewing_guide.docx", "rb") as f:
    st.download_button("Brewing guide (DOCX)", f, "brewing_guide.docx")