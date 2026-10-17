"""Математические операции над табличными данными: наивные циклы vs векторизация NumPy.

Реализует 5 базовых операций в двух вариантах для замера ускорения:
1. MinMax масштабирование: (x - min) / (max - min + eps).
2. Стандартизация: (x - mean) / (std + eps).
3. Функция активации ReLU: max(0, x).
4. Евклидово расстояние между векторами: sqrt(sum((u - v)^2)).
5. Взвешенная сумма признаков: X @ w.
"""

import math
from typing import List

import numpy as np


# ---------------------------------------------------------------------
# 1. MinMax Scaling: (x - min) / (max - min + eps)
# ---------------------------------------------------------------------
def minmax_scale_naive(data: List[float], eps: float = 1e-9) -> List[float]:
    """Наивная реализация MinMax-нормализации через цикл Python."""
    min_val = min(data)
    max_val = max(data)
    return [(x - min_val) / (max_val - min_val + eps) for x in data]


def minmax_scale_vectorized(data: np.ndarray, eps: float = 1e-9) -> np.ndarray:
    """Векторизованная реализация MinMax-нормализации в C-буфере NumPy."""
    return (data - np.min(data)) / (np.max(data) - np.min(data) + eps)


# ---------------------------------------------------------------------
# 2. Standardization: (x - mean) / (std + eps)
# ---------------------------------------------------------------------
def standardize_naive(data: List[float], eps: float = 1e-9) -> List[float]:
    """Наивная стандартизация через вычисление среднего и дисперсии циклом."""
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std = math.sqrt(variance)
    return [(x - mean) / (std + eps) for x in data]


def standardize_vectorized(data: np.ndarray, eps: float = 1e-9) -> np.ndarray:
    """Векторизованная стандартизация через np.mean и np.std."""
    return (data - np.mean(data)) / (np.std(data) + eps)


# ---------------------------------------------------------------------
# 3. ReLU: max(0, x)
# ---------------------------------------------------------------------
def relu_naive(data: List[float]) -> List[float]:
    """Наивный ReLU через список и тернарное условие."""
    return [x if x > 0.0 else 0.0 for x in data]


def relu_vectorized(data: np.ndarray) -> np.ndarray:
    """Векторизованный ReLU в NumPy."""
    return np.maximum(data, 0.0)


# ---------------------------------------------------------------------
# 4. Euclidean Distance: sqrt(sum((u - v)^2))
# ---------------------------------------------------------------------
def euclidean_distance_naive(u: List[float], v: List[float]) -> float:
    """Наивный расчет евклидова расстояния между двумя векторами (списками)."""
    if len(u) != len(v):
        raise ValueError("Ошибка: векторы имеют разную длину")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(u, v)))


def euclidean_distance_vectorized(u: np.ndarray, v: np.ndarray) -> float:
    """Векторизованный расчет расстояния между векторами NumPy."""
    if u.shape != v.shape:
        raise ValueError("Ошибка: векторы имеют разную форму")
    diff = u - v
    return float(np.sqrt(np.dot(diff, diff)))


# ---------------------------------------------------------------------
# 5. Weighted Sum: X @ w
# ---------------------------------------------------------------------
def weighted_sum_naive(X: List[List[float]], weights: List[float]) -> List[float]:
    """Наивное умножение матрицы X на вектор весов через вложенные циклы."""
    return [sum(x * w for x, w in zip(row, weights)) for row in X]


def weighted_sum_vectorized(X: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Векторизованное матричное умножение через np.dot(X, weights)."""
    return np.dot(X, weights)
