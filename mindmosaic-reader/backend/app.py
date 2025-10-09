from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import DyslexiaAssistAgent

app = FastAPI()
agent = DyslexiaAssistAgent()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class TextInput(BaseModel):
    text: str
    user_speed: float | None = None

@app.post("/analyze")
def analyze_text(data: TextInput):
    result = agent.observe_text(data.text, data.user_speed)
    return result

