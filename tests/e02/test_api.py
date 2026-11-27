"""E02 — этап 5: шесть тестов API. Все TODO заполняешь сам.

Запуск из корня проекта:
    .venv/bin/python -m pytest tests/e02 -v

Подготовленный client приходит из соседнего conftest.py автоматически.
Не запускай сервер, не создавай свой TestClient и не загружай модель.
Тестовая модель ВСЕГДА возвращает label=positive, score=0.9.
Это проверка HTTP-обработки, а не правильности определения тональности.
Каждый тест должен содержать настоящие проверки assert.
"""


def test_health(client):
    """GET /health: статус 200 и точный JSON {"status": "ok"}."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_valid(client):
    """POST /predict, JSON {"text": "Отлично"}.

    Проверь статус 200 и точное совпадение словаря ответа с
    {"label": "positive", "score": 0.9}.
    """
    response = client.post("/predict", json={"text": "Отлично"})
    assert response.status_code == 200
    assert response.json() == {"label": "positive", "score": 0.9}


def test_predict_empty(client):
    """ДВА запроса POST /predict: {} и {"text": ""}.

    Для каждого проверь статус 422. В каждом ответе должно быть поле detail.
    Подробный текст ошибок фиксировать в тестах не нужно.
    """
    response_1 = client.post("/predict", json={})
    response_2 = client.post("/predict", json={"text": ""})
    assert response_1.status_code == 422
    assert response_2.status_code == 422
    assert response_1.json()["detail"] is not None
    assert response_2.json()["detail"] is not None


def test_predict_broken_json(client):
    """Отправь буквально незавершённый JSON: '{"text":'.

    Используй content (строка как есть), не json; Content-Type application/json.
    Проверь статус 422 и наличие detail в ответе.
    """
    response = client.post(
        "/predict", content='{"text":', headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422
    assert response.json()["detail"] is not None


def test_predict_length_limits(client):
    """Проверь границу: text из 500 букв 'а' принимается (200), из 501 — нет (422).

    Для успешного ответа проверь также label и score как в test_predict_valid.
    """
    text = "a" * 500
    response = client.post("/predict", json={"text": text})
    assert response.status_code == 200
    assert response.json() == {"label": "positive", "score": 0.9}
    response_2 = client.post("/predict", json={"text": text + "a"})
    assert response_2.status_code == 422


def test_predict_50_requests(client):
    """50 последовательных POST /predict с одним допустимым текстом.

    Для КАЖДОГО запроса проверь 200 и ожидаемый словарь ответа.
    Это обычный цикл for, без потоков, async и замера скорости.
    """
    for i in range(50):
        response = client.post("/predict", json={"text": "это ваще кал честно говоря"})
        assert response.status_code == 200
        assert response.json() == {"label": "positive", "score": 0.9}
