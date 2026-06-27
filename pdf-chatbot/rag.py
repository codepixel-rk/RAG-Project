from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
import streamlit as st

import os
import time
from huggingface_hub import login

# Optional: remove if using only public models
login(token=os.getenv("HF_TOKEN"))
start=time.time()

# -----------------------------
# Load Embedding Model (Only Once)
# -----------------------------
@st.cache_resource
def load_embeddings():
    print("Loading Embedding Model...")

    start = time.time()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print(f"Embedding loaded in {time.time()-start:.2f} sec")

    return embeddings


# -----------------------------
# Load FAISS Database (Only Once)
# -----------------------------
@st.cache_resource
def load_db():

    embeddings = load_embeddings()

    print("Loading FAISS Database...")

    start = time.time()

    db = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )

    print(f"FAISS loaded in {time.time()-start:.2f} sec")

    return db

# -----------------------------
# Load Ollama Model (Only Once)
# -----------------------------
@st.cache_resource
def load_llm():

    print("Loading Ollama Model...")

    start = time.time()

    llm = OllamaLLM(
        model="llama3"
    )

    print(f"Ollama loaded in {time.time()-start:.2f} sec")

    return llm

db = load_db()
llm = load_llm()

# -----------------------------
# Cache Similarity Search
# -----------------------------
@st.cache_data(show_spinner=False)
def retrieve_docs(question):

    docs = db.similarity_search(
        question,
        k=3
    )

    return docs

# -----------------------------
# Cache Answers
# -----------------------------
@st.cache_data(show_spinner=False)
def ask_question(question):

    start = time.time()

    docs = retrieve_docs(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = f"""
You are a helpful assistant.

Answer ONLY from the provided context.

If the answer is not available in the context,
say "I don't know."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    print(f"Total Response Time : {time.time()-start:.2f} sec")

    return response