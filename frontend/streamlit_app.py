import streamlit as st
import requests

st.title("📄 AI Research Paper Assistant")

# -------------------
# PDF Upload Section
# -------------------
st.header("Upload PDF")

pdf_file = st.file_uploader("Upload your research paper", type=["pdf"])

if pdf_file is not None:
    files = {"file": pdf_file.getvalue()}

    response = requests.post(
        "http://localhost:8000/upload-pdf/",
        files=files
    )

    st.success(response.json()["message"])

# -------------------
# Ask Section
# -------------------
st.header("Ask Question")

question = st.text_input("Enter your question")

if st.button("Ask"):
    response = requests.post(
        "http://localhost:8000/ask/",
        json={"question": question}
    )

    st.write("### Answer")
    st.write(response.json()["answer"])

    st.write("### Relevant chunks")
    st.write(response.json()["relevant_chunks"])