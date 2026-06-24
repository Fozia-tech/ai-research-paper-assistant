from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os
import requests

from backend.pdf_loader import extract_text
from backend.rag_pipeline import create_chunks, store_chunks, search_chunks

from dotenv import load_dotenv

# -------------------------
# Load environment
# -------------------------
load_dotenv()

# -------------------------
# FastAPI app
# -------------------------
app = FastAPI(title="Research Paper Assistant")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------
# Request schema
# -------------------------
class QuestionRequest(BaseModel):
    question: str

# -------------------------
# Home route
# -------------------------
@app.get("/")
def home():
    return {"message": "RAG Backend Running 🚀"}

# -------------------------
# Upload PDF
# -------------------------
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)
    chunks = create_chunks(text)

    # IMPORTANT: avoid duplicate storage issues
    unique_chunks = list(dict.fromkeys(chunks))

    store_chunks(unique_chunks)

    return {
        "message": "PDF indexed successfully",
        "chunks_created": len(unique_chunks)
    }

# -------------------------
# LLM (Ollama Llama3)
# -------------------------
def generate_answer(question, context):

    if not context.strip():
        return "No relevant context found in document."

    prompt = f"""
You are a helpful AI assistant.

RULES:
- Use ONLY the given context
- If answer is not in context, say "Not found in document"
- Be precise and short

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()
        return response.json().get("response", "No response from model")

    except Exception as e:
        return f"Ollama Error: {str(e)}"

# -------------------------
# Ask endpoint
# -------------------------
@app.post("/ask/")
async def ask_question(request: QuestionRequest):

    raw_chunks = search_chunks(request.question)

    # remove duplicates + clean
    chunks = list(dict.fromkeys(raw_chunks))

    if not chunks:
        return {
            "question": request.question,
            "answer": "No relevant information found in document.",
            "relevant_chunks": []
        }

    # limit chunks (IMPORTANT for better answers)
    chunks = chunks[:4]

    context = "\n\n".join(chunks)

    answer = generate_answer(request.question, context)

    return {
        "question": request.question,
        "answer": answer,
        "relevant_chunks": chunks
    }