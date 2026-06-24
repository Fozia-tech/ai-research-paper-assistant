import os

os.environ.pop("SSL_CERT_FILE", None)
os.environ.pop("REQUESTS_CA_BUNDLE", None)

from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from sentence_transformers import SentenceTransformer

# -------------------------
# Embedding Model
# -------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------
# ChromaDB Setup
# -------------------------
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="research_papers")

# -------------------------
# Chunking
# -------------------------
def create_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_text(text)

# -------------------------
# Store chunks (FIXED DUPLICATES ISSUE)
# -------------------------
def store_chunks(chunks):
    embeddings = model.encode(chunks).tolist()

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[f"chunk_{hash(chunk)}"]
        )

    return len(chunks)

# -------------------------
# Search chunks (IMPROVED + CLEAN)
# -------------------------
def search_chunks(query, top_k=5):

    print("Searching for:", query)

    query = query.lower()

    # query expansion (smart boost)
    if "conclusion" in query:
        query += " summary result ending final"

    if "rules" in query:
        query += " instructions guidelines requirements process"

    if "definition" in query:
        query += " meaning explanation what is"

    query_embedding = model.encode([query])[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    docs = results.get("documents", [[]])[0]

    # safety check
    if not docs:
        return []

    # filter noise + short chunks remove
    docs = [d for d in docs if d and len(d.split()) > 20]

    return docs

# -------------------------
# Context helper
# -------------------------
def get_context(query):
    return "\n\n".join(search_chunks(query))