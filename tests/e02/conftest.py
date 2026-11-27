"""Готовая подготовка клиента для этапа 5. Менять этот файл не требуется.

pytest передаёт client тестам, которые указывают параметр с таким именем.
Подмена загрузчика действует только внутри каждого теста; обычный запуск сервиса
продолжает использовать настоящую модель. Сам FastAPI и lifespan остаются реальными.
"""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from exercises import e02_service


def fake_classifier(text, **kwargs):
    """Предсказуемый ответ для проверки API, а не качества нейросети."""
    return [{"label": "positive", "score": 0.9}]


@pytest.fixture
def client():
    with patch.object(e02_service, "load_classifier", return_value=fake_classifier):
        with TestClient(e02_service.app) as test_client:
            yield test_client
