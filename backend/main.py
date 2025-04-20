from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from response_logic import generate_supportive_feedback

app = FastAPI()

# Allow frontend (e.g., Streamlit) to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnswerItem(BaseModel):
    question: str
    answer: str

class SurveyRequest(BaseModel):
    responses: List[AnswerItem]

@app.post("/generate_feedback")
def generate_feedback(request: SurveyRequest):
    feedback = generate_supportive_feedback(request.responses)
    return {"feedback": feedback}
