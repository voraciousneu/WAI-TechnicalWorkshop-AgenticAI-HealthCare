from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from agent import MedicalDyslexiaAgent

app = FastAPI()
agent = MedicalDyslexiaAgent()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class MedicalTextInput(BaseModel):
    text: str
    user_context: Optional[dict] = None

@app.post("/analyze")
def analyze_medical_text(data: MedicalTextInput):
    """Analyze medical text with dyslexia-focused agentic AI"""
    result = agent.analyze_medical_text(data.text, data.user_context)
    return result

@app.get("/profile")
def get_user_profile():
    """Get current user profile and progress"""
    return agent.user_profile

