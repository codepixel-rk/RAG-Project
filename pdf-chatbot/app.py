import streamlit as st
from rag import ask_question

st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="📄"
)

st.title("📄 PDF Chatbot using RAG")

st.write(
    "Ask questions from your PDF document."
)
if "answer" not in st.session_state:
    st.session_state.answer = ""

question = st.text_input(
    "Enter your question"
)

if st.button("Ask"):

    if question.strip():

        with st.spinner("Searching PDF and generating answer..."):

            st.session_state.answer = ask_question(question)

if st.session_state.answer:

    st.success("Answer")

    st.write(st.session_state.answer)