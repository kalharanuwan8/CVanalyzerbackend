import pdfplumber
import docx
import tempfile
from fastapi import UploadFile, HTTPException

def extract_text_from_cv(file: UploadFile) -> str:
    filename = file.filename.lower()
    suffix = filename.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    try:
        if suffix == "pdf":
            with pdfplumber.open(tmp_path) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)
        elif suffix in ["docx", "doc"]:
            doc = docx.Document(tmp_path)
            return "\n".join(p.text for p in doc.paragraphs)
        else:
            raise HTTPException(400, "Unsupported file type. Please upload PDF or DOCX.")
    except Exception as e:
        raise HTTPException(500, f"Error reading file: {e}")
