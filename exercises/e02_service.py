"""E02: локальный сервис тональности текста, этапы 1–3 выполнены.

Обычный запуск:
    .venv/bin/python exercises/e02_service.py

Сервер работает до Ctrl+C. Адрес: http://127.0.0.1:8000
Маршруты: GET /health, POST /inspect и POST /predict.
Готовая модель загружается один раз при создании приложения и работает на CPU.
"""

import logging
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from mldata.e02_model import load_classifier

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=500)


class InspectResponse(BaseModel):
    length: int = Field(ge=0)


class PredictResponse(BaseModel):
    label: Literal["negative", "neutral", "positive"]
    score: float = Field(le=1, ge=0)


@asynccontextmanager
async def lifespan(app):
    try:
        LOGGER.info("попытка загрузки")
        try:
            app.state.classifier = load_classifier()
            LOGGER.info("загрузилось все")
        except Exception:
            LOGGER.exception("ошибка загрузки")
            raise
        yield
    finally:
        LOGGER.info("выгрузилось все")
        app.state.classifier = None


app = FastAPI(title="E02: учебный AI API", lifespan=lifespan)


@app.get("/health")
def get_health():
    return {"status": "ok"}


@app.post("/inspect", response_model=InspectResponse)
def get_length(request: TextRequest):
    return {"length": len(request.text)}


@app.post("/predict", response_model=PredictResponse)
def get_predict(request: TextRequest):
    try:
        return app.state.classifier(request.text, truncation=True, max_length=512)[0]
    except RuntimeError:
        LOGGER.exception("Ошибка выполнения модели")
        raise HTTPException(status_code=500, detail="Ошибка выполнения модели")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
