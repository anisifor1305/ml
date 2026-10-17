"""Компоненты для работы с данными: потоковое чтение и структуры датасетов."""

import os
from typing import Iterator, Optional, Tuple, Union

import numpy as np
import pandas as pd


def stream_csv(path: str, chunksize: int = 1000) -> Iterator[pd.DataFrame]:
    """Потоковый генератор для чтения больших CSV файлов чанками без переполнения памяти.

    Args:
        path: Путь к файлу CSV.
        chunksize: Количество строк в одном чанке (батче).

    Yields:
        pd.DataFrame: Очередной чанк таблицы.

    Raises:
        FileNotFoundError: Если файл по пути `path` не существует (os.path.exists).
        ValueError: Если chunksize <= 0.
    """
    if not os.path.exists(path):
        raise FileNotFoundError("файл не найден")
    if chunksize <= 0:
        raise ValueError("чанксайз не может быть меньше или равен 0")

    for chunk in pd.read_csv(path, chunksize=chunksize):
        yield chunk


class TableDataset:
    """Универсальный класс датасета табличных данных на чистом Python/NumPy.

    Реализует стандартный протокол последовательности:
    - __init__: сохраняет features и targets, проверяет их длины;
    - __len__: возвращает количество образцов;
    - __getitem__: возвращает кортеж (features, target) по индексу;
    - __repr__: возвращает читаемое представление структуры датасета.
    """

    def __init__(
        self,
        features: np.ndarray,
        targets: Optional[np.ndarray] = None,
    ) -> None:
        """Сохраняет признаки и целевые значения.

        Если targets передан, проверяет, что len(features) == len(targets).
        Если длины не равны — бросает ValueError.
        """
        self.features = features
        self.targets = targets
        if targets is not None and len(features) != len(targets):
            raise ValueError("Features and targets must have same length")

    def __len__(self) -> int:
        return len(self.features)

    def __getitem__(self, idx: int) -> Tuple[np.ndarray, Optional[Union[float, int, np.ndarray]]]:
        """Возвращает кортеж (признаки_i, таргет_i) для образца по индексу idx.

        Если idx вне диапазона [0, len-1], бросает IndexError.
        Если targets нет (None), вторым элементом возвращает None.
        """
        if idx < 0 or idx >= len(self):
            raise IndexError("Index out of bounds")
        target = self.targets[idx] if self.targets is not None else None
        return (self.features[idx], target)

    def __repr__(self) -> str:
        """Возвращает строку вида: TableDataset(samples=..., features=..., has_targets=...)."""
        return f"TableDataset(samples={len(self)}, has_targets={self.targets is not None})"
