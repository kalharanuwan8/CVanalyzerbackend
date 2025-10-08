from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber, docx, tempfile, json, os
from google import genai

app = FastAPI()

# ✅ Allow frontend URLs (for local testing)
origins = [
    "http://localhost:3000",
    "https://cv-analyzer.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text(file: UploadFile) -> str:
    ext = file.filename.lower().split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    if ext == "pdf":
        with pdfplumber.open(tmp_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif ext in ["docx", "doc"]:
        doc = docx.Document(tmp_path)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        raise HTTPException(400, "Unsupported file type")

@app.post("/api/analyze")
async def analyze(cv: UploadFile = File(...), jd: str = Form(...)):
    try:
        cv_text = extract_text(cv)

        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        prompt = f"""
        Compare this candidate's CV with the job description deeply with if the requirements are defined in the job description check with them, else check with the general mentioned job and return JSON:
        {{
          "fitScore": "Poor|Okay|Good|Great",
          "confidencePct": number,
          "strengths": [list],
          "weaknesses": [list],
          "suggestions": [list]
        }}
        CV:
        {cv_text}
        JOB:
        {jd}
        """

        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )

        return json.loads(response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
