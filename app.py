import streamlit as st
from src.embeddings import load_data, answer_question

st.title("Hearthstone Coffee Assistant")

all_chunks, embeddings = load_data()

question = st.text_input("Ask a question about our coffee:")

if question:
    answer, source, score = answer_question(question, all_chunks, embeddings)
    st.write(answer)
    if source:
        st.caption(f"Source: {source}")