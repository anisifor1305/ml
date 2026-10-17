"""Конфигурация экспериментов машинного обучения со строгой валидацией."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ExperimentConfig:
    """Конфигурационный класс эксперимента.

    Атрибуты:
        name: Уникальное название эксперимента (строка, не должна быть пустой).
        batch_size: Размер мини-батча (целое число, по умолчанию 32, строго > 0).
        learning_rate: Скорость обучения (float, по умолчанию 0.001, строго > 0.0).
        epochs: Число эпох обучения (целое число, по умолчанию 10, строго > 0).
        seed: Сид случайных чисел (целое число, по умолчанию 42).
        tags: Список тегов (list[str], по умолчанию пустой список).
        description: Опциональное описание (Optional[str], по умолчанию None).
    """

    name: str
    batch_size: int = 32
    learning_rate: float = 0.001
    epochs: int = 10
    seed: int = 42
    tags: list[str] = field(default_factory=list)
    description: Optional[str] = None

    def __post_init__(self) -> None:
        """Валидация параметров после создания объекта.

        Должна бросать ValueError, если:
        - name пустое или состоит только из пробелов;
        - batch_size <= 0;
        - learning_rate <= 0.0;
        - epochs <= 0.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Имя не должно быть пустым")
        if self.batch_size <= 0:
            raise ValueError("batch_size должен быть > 0")
        if self.learning_rate <= 0:
            raise ValueError("learning_rate должен быть > 0")
        if self.epochs <= 0:
            raise ValueError("epochs должно быть > 0")
