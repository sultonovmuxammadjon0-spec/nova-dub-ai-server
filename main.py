
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="NOVA DUB AI")

class TranslationRequest(BaseModel):
    source_language: str
    target_language: str

@app.get("/")
def home():
    return {
        "app": "NOVA DUB AI",
        "status": "online"
    }

@app.post("/translate")
def translate(request: TranslationRequest):
    return {
        "status": "connected",
        "source_language": request.source_language,
        "target_language": request.target_language,
        "message": "AI translation engine is not connected yet"
    }
