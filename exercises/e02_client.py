"""E02, этап 8: обращение к работающему сервису из отдельной программы.

Сначала запусти exercises/e02_service.py, затем обычным способом этот файл.
Реализуй request_prediction. Сервер не импортируй: обращаемся по HTTP.
"""

import json

import httpx  # noqa: F401

URL = "http://127.0.0.1:8000/predict"


def request_prediction(text: str) -> dict:
    """Отправь POST на URL, тело JSON {"text": text}, timeout=30.0.

    Вызови response.raise_for_status(): он выбросит ошибку при неуспешном
    HTTP-статусе. Затем верни response.json() — словарь ответа.
    Используй httpx.post (не client из pytest); импортировать модель не нужно.
    """
    response = httpx.post(
        "http://127.0.0.1:8000/predict",
        json={"text": text},
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    result = request_prediction("Отличный товар, всё понравилось!")
    print(json.dumps(result, ensure_ascii=False, indent=2))
