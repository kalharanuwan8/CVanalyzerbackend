from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils import extract_text_from_cv
from app.services import analyze_with_gemini
from app.schemas import AnalysisResponse
import os

app = FastAPI(title="CV Analyzer API")

# CORS (adjust when you deploy your frontend)
ALLOWED_ORIGINS = [
    os.getenv("FRONTEND_ORIGIN", "http://localhost:3000"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "CV Analyzer Backend Running ✅"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(cv: UploadFile = File(...), jd: str = Form(...)):
    cv_text = extract_text_from_cv(cv)
    if not jd.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")
    return analyze_with_gemini(cv_text, jd)
