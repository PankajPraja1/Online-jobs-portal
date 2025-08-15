import io
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(file_obj):
    try:
        reader = PdfReader(file_obj)
        text = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text.append(t)
        return "\n".join(text)
    except Exception:
        return ""

def extract_text_from_docx(file_obj):
    try:
        doc = Document(file_obj)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return ""
