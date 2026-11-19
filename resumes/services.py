from pathlib import Path
from docx import Document
from pypdf import PdfReader

def extract_resume_text(file_path: str) -> str:
    suffix = Path(file_path).suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif suffix == ".docx":
        doc = Document(file_path)
        text = "\n".join(p.text for p in doc.paragraphs)
        for table in doc.tables:
            for row in table.rows:
                text += "\n" + " | ".join(cell.text for cell in row.cells)
    else:
        raise ValueError("Unsupported resume format.")
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    if not text.strip():
        raise ValueError("No readable text was found. Please upload a text-based PDF or DOCX.")
    return text
