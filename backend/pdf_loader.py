from pypdf import PdfReader
import re

def clean_text(text):
    # remove extra spaces, weird line breaks
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            cleaned = clean_text(page_text)
            text.append(cleaned)

    return "\n".join(text)