

import os
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from huggingface_hub import login

login(token=os.getenv("HF_TOKEN"))
loader = PyPDFLoader(
    r"G:\AI Project\pdf-chatbot\data\Kafka.pdf"
)

start=time.time()
docs = loader.load()
print("Loading PDF...time taken", time.time()-start)
print(f"Pages Loaded: {len(docs)}")
# LLMs cannot process hundreds of pages.

start=time.time()
# Split into smaller pieces.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(docs)
print(f"Chunks Created: {len(chunks)}")

print("Splitting Documents time taken...", time.time()-start)

# Then Add Embeddings
# "What is Kafka?"

# ↓

# [0.21,0.44,0.55,0.99,....]

print("Generating embeddings...")
start=time.time()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Generating embeddings time taken...", time.time()-start)

# Create FAISS Database
# Chunk 1 → Vector
# Chunk 2 → Vector
# Chunk 3 → Vector
# Chunk 4 → Vector

print("Creating FAISS database...")
start=time.time()


db = FAISS.from_documents(
    chunks,
    embeddings
)

# Save Database
db.save_local("vectorstore")
print("Vector DB Saved Successfully")
print("Creating FAISS database time taken...", time.time()-start)