"""Готовая загрузка модели E02. Обработчик /predict пишет ученик.

Загрузка не происходит при импорте этого модуля: вызывай load_classifier один раз
при создании приложения. Модель работает локально на CPU.
"""

MODEL_ID = "cointegrated/rubert-tiny-sentiment-balanced"
MODEL_REVISION = "e0679dd4460e48648f5d4d819ae0f505384f5a9d"


def load_classifier():
    from transformers import pipeline

    return pipeline(
        "text-classification",
        model=MODEL_ID,
        revision=MODEL_REVISION,
        framework="pt",
        device=-1,
        model_kwargs={"use_safetensors": True},
    )
