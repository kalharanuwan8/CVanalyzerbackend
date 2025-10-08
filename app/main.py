from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils import extract_text_from_cv
from app.services import analyze_with_gemini
from app.schemas import AnalysisResponse

app = FastAPI(title="CV Analyzer API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "CV Analyzer Backend Running ✅"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(cv: UploadFile = File(...), jd: str = Form(...)):
    try:
        cv_text = extract_text_from_cv(cv)
        if not jd.strip():
            raise HTTPException(400, "Job description cannot be empty.")
        result = analyze_with_gemini(cv_text, jd)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
