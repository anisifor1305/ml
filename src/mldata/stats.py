"""Модуль описательной статистики для табличных данных."""

import numpy as np
import pandas as pd


def describe(df: pd.DataFrame) -> pd.DataFrame:
    """Вычисляет базовые описательные статистики для числовых колонок датафрейма.

    Аналог базовой функциональности `pandas.DataFrame.describe`.
    Рассчитывает: count, mean, std, min, max.

    Args:
        df: Исходный датафрейм pandas.

    Returns:
        pd.DataFrame: Таблица статистик, где строки — метрики
                      ('count', 'mean', 'std', 'min', 'max'),
                      а столбцы — числовые признаки.
    """
    # TODO:
    # 1. Отбери числовые колонки: df.select_dtypes(include=[np.number])
    # 2. Посчитай для них count(), mean(), std(), min(), max()
    # 3. Сформируй и верни итоговый DataFrame с индексом ['count', 'mean', 'std', 'min', 'max']
    num_df = df.select_dtypes(include=[np.number])
    count = num_df.count()
    mean = num_df.mean()
    std = num_df.std()
    min = num_df.min()
    max = num_df.max()
    return pd.DataFrame([count, mean, std, min, max], index=["count", "mean", "std", "min", "max"])
