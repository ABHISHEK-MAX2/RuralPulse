import os
import re
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions

PDF_PATH = "medical_guidelines.pdf"
DB_DIR = "./chroma_db"
COLLECTION_NAME = "medical_triage"

if not os.path.exists(PDF_PATH):
    raise FileNotFoundError(f"Missing '{PDF_PATH}'. Place the ESI PDF in this directory.")

def clean_extracted_text(text: str) -> str:
    """Repairs font-encoding corruptions without deleting legitimate 'w' letters."""
    if not text:
        return ""
    # Strip persistent base64 / font artifact tokens
    text = re.sub(r'[A-Za-z0-9+/=]{20,}', ' ', text)
    # Normalize excessive whitespaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

print("Extracting clean pages from ESI Handbook using pdfplumber...")
documents = []
metadatas = []

with pdfplumber.open(PDF_PATH) as pdf:
    for page_idx, page in enumerate(pdf.pages):
        raw_text = page.extract_text()
        if raw_text:
            cleaned = clean_extracted_text(raw_text)
            if len(cleaned) > 40:
                documents.append(cleaned)
                metadatas.append({"page": page_idx + 1})

print(f"Extracted {len(documents)} clean pages.")

# Chunking
splitter = RecursiveCharacterTextSplitter(
    chunk_size=750,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " "]
)

chunks = []
chunk_metas = []
chunk_ids = []

counter = 0
for doc_text, meta in zip(documents, metadatas):
    sub_chunks = splitter.split_text(doc_text)
    for sub_chunk in sub_chunks:
        chunks.append(sub_chunk)
        chunk_metas.append(meta)
        chunk_ids.append(f"esi_chunk_{counter}")
        counter += 1

print(f"Generated {len(chunks)} cleaned chunks.")

# Rebuild ChromaDB
client = chromadb.PersistentClient(path=DB_DIR)

if COLLECTION_NAME in [c.name for c in client.list_collections()]:
    client.delete_collection(COLLECTION_NAME)

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_fn
)

batch_size = 200
for i in range(0, len(chunks), batch_size):
    collection.add(
        documents=chunks[i:i + batch_size],
        metadatas=chunk_metas[i:i + batch_size],
        ids=chunk_ids[i:i + batch_size]
    )

print(f"Successfully re-indexed clean database into '{DB_DIR}'.")