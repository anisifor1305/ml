"""Модульные тесты библиотеки mldata."""

import os
import tempfile

import numpy as np
import pandas as pd
import pytest

from mldata import (
    ExperimentConfig,
    TableDataset,
    describe,
    euclidean_distance_naive,
    euclidean_distance_vectorized,
    minmax_scale_naive,
    minmax_scale_vectorized,
    relu_naive,
    relu_vectorized,
    standardize_naive,
    standardize_vectorized,
    stream_csv,
    weighted_sum_naive,
    weighted_sum_vectorized,
)


def test_experiment_config_valid():
    """Тест 1: Корректное создание конфигурации с дефолтными значениями."""
    cfg = ExperimentConfig(name="baseline_model")
    assert cfg.name == "baseline_model"
    assert cfg.batch_size == 320000
    assert cfg.learning_rate == 0.001
    assert cfg.epochs == 10
    assert cfg.tags == []


def test_experiment_config_invalid_raises():
    """Тест 2: Проверка валидации параметров конфига."""
    with pytest.raises(ValueError):
        ExperimentConfig(name="   ")

    with pytest.raises(ValueError):
        ExperimentConfig(name="test", batch_size=-1)

    with pytest.raises(ValueError):
        ExperimentConfig(name="test", learning_rate=0.0)

    with pytest.raises(ValueError):
        ExperimentConfig(name="test", epochs=0)


def test_table_dataset_len_and_getitem():
    """Тест 3: Проверка протокола последовательности TableDataset."""
    features = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    targets = np.array([0, 1, 0])
    ds = TableDataset(features, targets)

    assert len(ds) == 3
    x, y = ds[1]
    assert np.array_equal(x, np.array([3.0, 4.0]))
    assert y == 1
    assert "TableDataset" in repr(ds)


def test_table_dataset_dimension_mismatch():
    """Тест 4: Ошибка при несовпадении длины признаков и целевой переменной."""
    features = np.zeros((10, 2))
    targets = np.zeros((8,))
    with pytest.raises(ValueError):
        TableDataset(features, targets)


def test_stream_csv_chunks():
    """Тест 5: Потоковое чтение CSV чанками через генератор."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("a,b\n")
        for i in range(25):
            f.write(f"{i},{i * 2}\n")
        temp_path = f.name

    try:
        chunks = list(stream_csv(temp_path, chunksize=10))
        assert len(chunks) == 3  # 10 + 10 + 5
        assert len(chunks[0]) == 10
        assert len(chunks[1]) == 10
        assert len(chunks[2]) == 5
        assert list(chunks[0].columns) == ["a", "b"]
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_minmax_and_standardize_match():
    """Тест 6: Численное совпадение наивной и векторизованной нормализации."""
    raw = [10.0, 20.0, 50.0, 100.0, -10.0]
    raw_np = np.array(raw, dtype=np.float32)

    # MinMax
    res_naive_mm = minmax_scale_naive(raw)
    res_vec_mm = minmax_scale_vectorized(raw_np)
    assert np.allclose(res_naive_mm, res_vec_mm, atol=1e-5)

    # Standardize
    res_naive_std = standardize_naive(raw)
    res_vec_std = standardize_vectorized(raw_np)
    assert np.allclose(res_naive_std, res_vec_std, atol=1e-5)


def test_relu_match():
    """Тест 7: Численное совпадение наивного и векторизованного ReLU."""
    raw = [-5.0, 0.0, 3.5, -0.1, 12.0]
    raw_np = np.array(raw, dtype=np.float32)

    res_naive = relu_naive(raw)
    res_vec = relu_vectorized(raw_np)
    assert np.allclose(res_naive, res_vec, atol=1e-5)


def test_euclidean_and_weighted_sum_match():
    """Тест 8: Численное совпадение евклидова расстояния и взвешенной суммы."""
    u = [1.0, 2.0, 3.0]
    v = [4.0, 0.0, -1.0]
    u_np = np.array(u, dtype=np.float32)
    v_np = np.array(v, dtype=np.float32)

    dist_naive = euclidean_distance_naive(u, v)
    dist_vec = euclidean_distance_vectorized(u_np, v_np)
    assert np.isclose(dist_naive, dist_vec, atol=1e-5)

    X = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    w = [0.5, 2.0]
    X_np = np.array(X, dtype=np.float32)
    w_np = np.array(w, dtype=np.float32)

    ws_naive = weighted_sum_naive(X, w)
    ws_vec = weighted_sum_vectorized(X_np, w_np)
    assert np.allclose(ws_naive, ws_vec, atol=1e-5)


def test_describe_statistics():
    """Тест 9: Проверка работы собственной функции describe."""
    df = pd.DataFrame(
        {
            "num1": [10.0, 20.0, 30.0],
            "num2": [100.0, 200.0, 300.0],
            "cat": ["a", "b", "c"],  # должна быть отфильтрована
        }
    )
    desc = describe(df)
    assert list(desc.columns) == ["num1", "num2"]
    assert list(desc.index) == ["count", "mean", "std", "min", "max"]
    assert desc.loc["mean", "num1"] == 20.0
    assert desc.loc["count", "num2"] == 3.0


def test_table_dataset_index_out_of_bounds():
    """Тест 10: Проверка выброса IndexError при выходе индекса за границы."""
    features = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    targets = np.array([0, 1, 0])
    ds = TableDataset(features, targets)
    with pytest.raises(IndexError):
        _ = ds[999]
