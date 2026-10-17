"""Бенчмарк производительности: наивные циклы vs векторизация NumPy.

Замеряет:
1. Время выполнения (сек) через time.perf_counter().
2. Пиковое потребление памяти (МБ) через tracemalloc.
3. Коэффициент ускорения (Speedup = t_naive / t_vectorized).
"""

import time
import tracemalloc
from typing import Callable, Tuple

import numpy as np

from mldata.ops import (
    minmax_scale_naive,
    minmax_scale_vectorized,
    relu_naive,
    relu_vectorized,
    standardize_naive,
    standardize_vectorized,
    weighted_sum_naive,
    weighted_sum_vectorized,
)


def profile_fn(fn: Callable, *args) -> Tuple[float, float, object]:
    """Замеряет время работы и пиковую память функции."""
    tracemalloc.start()
    t0 = time.perf_counter()
    res = fn(*args)
    t_elapsed = time.perf_counter() - t0
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_mb = peak_bytes / (1024 * 1024)
    return t_elapsed, peak_mb, res


def run_benchmarks():
    print("=" * 78)
    print("БЕНЧМАРК ПРОИЗВОДИТЕЛЬНОСТИ: НАИВНЫЕ ЦИКЛЫ vs ВЕКТОРИЗАЦИЯ NUMPY")
    print("=" * 78)

    rng = np.random.default_rng(42)
    N = 1_000_000

    # 1. Генерация данных
    arr_np = rng.normal(loc=0.0, scale=1.0, size=(N,)).astype(np.float64)
    arr_list = arr_np.tolist()

    benchmarks = []

    # Операция 1: MinMax
    t_n, m_n, _ = profile_fn(minmax_scale_naive, arr_list)
    t_v, m_v, _ = profile_fn(minmax_scale_vectorized, arr_np)
    benchmarks.append(("MinMax Scaling (1M)", t_n, m_n, t_v, m_v))

    # Операция 2: Standardize
    t_n, m_n, _ = profile_fn(standardize_naive, arr_list)
    t_v, m_v, _ = profile_fn(standardize_vectorized, arr_np)
    benchmarks.append(("Standardize (1M)", t_n, m_n, t_v, m_v))

    # Операция 3: ReLU
    t_n, m_n, _ = profile_fn(relu_naive, arr_list)
    t_v, m_v, _ = profile_fn(relu_vectorized, arr_np)
    benchmarks.append(("ReLU Activation (1M)", t_n, m_n, t_v, m_v))

    # Операция 4: Weighted Sum (50 000 строк x 50 признаков)
    N_rows, D = 50_000, 50
    mat_np = rng.normal(size=(N_rows, D))
    mat_list = mat_np.tolist()
    w_np = rng.normal(size=(D,))
    w_list = w_np.tolist()

    t_n, m_n, _ = profile_fn(weighted_sum_naive, mat_list, w_list)
    t_v, m_v, _ = profile_fn(weighted_sum_vectorized, mat_np, w_np)
    benchmarks.append((f"Weighted Sum ({N_rows}x{D})", t_n, m_n, t_v, m_v))

    # Вывод результатов в таблицу
    header = (
        f"{'Операция':<25} | {'Время Naive':<12} | "
        f"{'Время NumPy':<12} | {'Ускорение':<10} | {'Пик RAM (MB)'}"
    )
    print(header)
    print("-" * 78)

    all_passed_20x = True
    for name, tn, mn, tv, mv in benchmarks:
        speedup = tn / max(tv, 1e-9)
        if speedup < 20.0:
            all_passed_20x = False
        print(f"{name:<25} | {tn:>8.4f} сек | {tv:>8.4f} сек | {speedup:>8.1f}x | {mv:>8.2f} MB")

    print("-" * 78)
    if all_passed_20x:
        print("✅ КРИТЕРИЙ СЕССИИ E01 ВЫПОЛНЕН: ускорение векторизации >= 20x по всем операциям!")
    else:
        print("⚠️ Ускорение менее 20x на некоторых операциях.")


if __name__ == "__main__":
    run_benchmarks()
