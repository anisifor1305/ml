"""E02: локальный сервис. Начни с шага 1 — GET /health.

Обычный запуск:
    .venv/bin/python exercises/e02_service.py

Сервер работает до Ctrl+C. Адрес: http://127.0.0.1:8000
Задания дополняем после разбора инструментов; готовую модель пока не подключаем.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=500)


class InspectResponse(BaseModel):
    length: int = Field(ge=0)


app = FastAPI(title="E02: учебный AI API")


@app.get('/health')
def get_health():
    return {"status": "ok"}


@app.post('/inspect', response_model=InspectResponse)
def get_length(request: TextRequest):
    return {"length": len(request.text)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
