# AI Research Paper Assistant (RAG-based Chatbot)

An AI-powered Research Paper Assistant that allows users to upload PDFs and ask questions.  
It uses Retrieval-Augmented Generation (RAG) with semantic search and LLM (Llama3) for intelligent answers.

## Features

- Upload PDF documents
- Automatic text extraction & chunking
- Semantic search using ChromaDB + Sentence Transformers
- AI answers using Llama3 (Ollama)
- Streamlit chat interface
- FastAPI backend APIs

## Tech Stack

- Python
- FastAPI
- Streamlit
- ChromaDB
- LangChain
- Sentence Transformers
- Ollama (Llama3)

## Project Structure

research-paper-assistant/
backend/
main.py
pdf_loader.py
rag_pipeline.py

frontend/
app.py

uploads/
chroma_db/

README.md

## Setup Instructions

1. Clone repo
git clone <your-repo-link>
cd research-paper-assistant

2. Create virtual environment
python -m venv venv
venv\Scripts\activate   (Windows)

3. Install dependencies
pip install -r requirements.txt

4. Run backend
uvicorn backend.main:app --reload

5. Run frontend
streamlit run frontend/app.py

## How it works

1. Upload PDF
2. Text is extracted
3. Split into chunks
4. Store in vector database (ChromaDB)
5. User asks question
6. Semantic search retrieves relevant chunks
7. LLM generates answer

## Future Improvements

- Multi-PDF support
- Chat memory
- Cloud deployment
- Better ranking system

## Author

Fozia
AI/ML Student | RAG Project