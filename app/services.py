import os
from google import genai
from app.config import settings
from app.schemas import AnalysisResponse
import json

def analyze_with_gemini(cv_text: str, jd_text: str) -> AnalysisResponse:
    # Initialize Gemini client
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    prompt = f"""
You are a professional AI recruiter. Compare the candidate’s CV and the job description.
Return your analysis strictly in JSON with this structure:
{{
  "fitScore": "Poor|Okay|Good|Great",
  "confidencePct": number,
  "strengths": [list of strengths],
  "weaknesses": [list of weaknesses],
  "suggestions": [list of improvement tips]
}}

CV:
{cv_text}

JOB DESCRIPTION:
{jd_text}
"""

    response = client.models.generate_content(
        model=settings.MODEL_NAME,
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )

    try:
        result_json = json.loads(response.text)
        return AnalysisResponse(**result_json)
    except Exception as e:
        raise ValueError(f"Error parsing Gemini response: {e}")
