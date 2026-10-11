
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="NOVA DUB AI")

LANGUAGES = {
    "O‘zbekcha": "uz",
    "English": "en",
    "Русский": "ru",
    "Türkçe": "tr",
    "العربية": "ar",
    "中文": "zh-CN",
    "한국어": "ko",
    "日本語": "ja",
    "Français": "fr",
    "Deutsch": "de",
    "Español": "es"
}

class TranslationRequest(BaseModel):
    source_language: str
    target_language: str
    text: str

@app.get("/")
def home():
    return {
        "app": "NOVA DUB AI",
        "status": "online"
    }

@app.post("/translate")
def translate(request: TranslationRequest):
    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Tarjima uchun matn kiriting"
        )

    source = LANGUAGES.get(request.source_language)
    target = LANGUAGES.get(request.target_language)

    if not source or not target:
        raise HTTPException(
            status_code=400,
            detail="Til hozircha qo‘llab-quvvatlanmaydi"
        )

    if source == target:
        return {
            "status": "success",
            "translated_text": text,
            "source_language": request.source_language,
            "target_language": request.target_language
        }

    try:
        response = requests.get(
            "https://api.mymemory.translated.net/get",
            params={
                "q": text,
                "langpair": source + "|" + target
            },
            timeout=25
        )
        response.raise_for_status()
        data = response.json()

        translated = data.get(
            "responseData", {}
        ).get("translatedText")

        if data.get("responseStatus") != 200 or not translated:
            raise HTTPException(
                status_code=502,
                detail="Tarjima xizmati natija bermadi"
            )

        return {
            "status": "success",
            "source_language": request.source_language,
            "target_language": request.target_language,
            "original_text": text,
            "translated_text": translated
        }

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Tarjima xizmatiga ulanib bo‘lmadi"
        )

