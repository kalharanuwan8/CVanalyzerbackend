from pydantic import BaseModel
from typing import List, Literal

class AnalysisResponse(BaseModel):
    fitScore: Literal["Poor", "Okay", "Good", "Great"]
    confidencePct: int
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
