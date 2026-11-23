"""E02: локальный сервис тональности текста, этапы 1–3 выполнены.

Обычный запуск:
    .venv/bin/python exercises/e02_service.py

Сервер работает до Ctrl+C. Адрес: http://127.0.0.1:8000
Маршруты: GET /health, POST /inspect и POST /predict.
Готовая модель загружается один раз при создании приложения и работает на CPU.
"""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from mldata.e02_model import load_classifier


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=500)


class InspectResponse(BaseModel):
    length: int = Field(ge=0)


class PredictResponse(BaseModel):
    label: Literal["negative", "neutral", "positive"]
    score: float = Field(le=1, ge=0)


app = FastAPI(title="E02: учебный AI API")
classifier = load_classifier()


@app.get("/health")
def get_health():
    return {"status": "ok"}


@app.post("/inspect", response_model=InspectResponse)
def get_length(request: TextRequest):
    return {"length": len(request.text)}


@app.post("/predict", response_model=PredictResponse)
def get_predict(request: TextRequest):
    return classifier(request.text, truncation=True, max_length=512)[0]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
