"""
Занятие 06: NumPy: векторизация и производительность.
Практические задания и ускорение вычислений.
"""

import time
import numpy as np


# =====================================================================
# Задание 1. Булевы маски, замена значений и численные проверки
# =====================================================================
def task_1_data_cleaning():
    """
    1.1. Реализуй ReLU: во входном массиве x занули все отрицательные числа на месте.
    1.2. Бинаризация через np.where: в массиве probs переведи вероятности в классы:
         если prob >= 0.5 -> 1, иначе -> 0.
    1.3. Защита от переполнения через np.clip: обрежь массив values так,
         чтобы все числа лежали строго в отрезке [0.01, 0.99].
    1.4. Очистка от NaN: с помощью np.nan_to_num замени все NaN на 0.0,
         а inf на 100.0 в массиве dirty_data.
    """
    # 1.1. ReLU
    x = np.array([-3.0, 5.0, -1.0, 0.0, 2.0])
    # TODO: занули отрицательные в x
    x_relu = np.where(x >= 0, x, 0)  # измени x на месте или верни измененный

    # 1.2. np.where
    probs = np.array([0.15, 0.85, 0.49, 0.50, 0.99])
    binary_classes = np.where(probs >= 0.5, 1, 0)  # TODO: примени np.where

    # 1.3. np.clip
    raw_values = np.array([-0.5, 0.0, 0.05, 0.5, 0.95, 1.0, 2.5])
    clipped_values = np.clip(raw_values, 0.01, 0.99)  # TODO: примени np.clip

    # 1.4. Очистка
    dirty_data = np.array([1.0, np.nan, 2.0, np.inf, -np.inf])
    cleaned_data = np.nan_to_num(dirty_data, 0.0, 100.0)  # TODO: примени np.nan_to_num

    return x_relu, binary_classes, clipped_values, cleaned_data


# =====================================================================
# Задание 2. Воспроизводимый генератор случайных чисел
# =====================================================================
def task_2_random_generation():
    """
    Создай генератор случайных чисел с фиксированным seed=42 через default_rng.
    1. Сгенерируй матрицу признаков X формы (100, 4) из стандартного нормального
       распределения (loc=0.0, scale=1.0).
    2. Сгенерируй вектор меток y формы (100,) из случайных целых чисел 0 или 1
       через метод rng.integers.
    """
    rng = np.random.default_rng(seed=42)

    X = rng.normal(size=(100, 4), loc=0.0, scale=1.0)
    y = rng.integers(0, 2, size=(100,))

    return X, y


# =====================================================================
# Задание 3. Битва векторизации: Попарные расстояния
# =====================================================================
# Даны две матрицы векторов:
# A формы (N, D) и B формы (M, D).
# Нужно посчитать матрицу евклидовых расстояний формы (N, M).


def pairwise_slow(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Способ 1: Двойной цикл for (ЧЕРЕПАХА). Уже написан как эталон.
    """
    N, D = A.shape
    M, _ = B.shape
    dists = np.zeros((N, M), dtype=np.float32)
    for i in range(N):
        for j in range(M):
            diff = A[i] - B[j]
            dists[i, j] = np.sqrt(np.sum(diff**2))
    return dists


def pairwise_semi_vectorized(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Способ 2: Полувекторный подход (один цикл for по i от 0 до N).
    Внутри цикла вычитаем вектор A[i] сразу из ВСЕЙ матрицы B через broadcasting!
    """
    N, D = A.shape
    M, _ = B.shape
    dists = np.zeros((N, M), dtype=np.float32)

    # TODO: реализуй цикл по i от 0 до N.
    # На каждом шаге: вычти A[i] из B, возведи в квадрат,
    # просуммируй по строкам B (axis=1) и возьми корень np.sqrt.
    for i in range(N):
        diff = B - A[i]
        dists[i] = np.sqrt(np.sum(diff**2, axis=1))

    return dists


def pairwise_fully_vectorized(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Способ 3: Полностью векторный подход (БЕЗ ЕДИНОГО ЦИКЛА FOR).
    Используем трюк "столбик минус строчка" через расширение размерностей:
    - A расширяем до формы (N, 1, D) через np.newaxis или A[:, None, :]
    - B расширяем до формы (1, M, D) через np.newaxis или B[None, :, :]
    - вычитаем: diff = A_expanded - B_expanded (форма станет N, M, D)
    - квадраты суммируем по последней оси (axis=-1)
    - берем корень np.sqrt()
    """
    # TODO: твой код в 1-3 строки
    A = A[:, np.newaxis, :]
    B = B[np.newaxis, :, :]
    dists = np.sqrt(np.sum((A - B) ** 2, axis=-1))
    return dists


# =====================================================================
# Задание 4. Бенчмарк и проверка критерия ускорения (>= 50x)
# =====================================================================
def benchmark_and_verify():
    print("\n--- Запуск бенчмарка попарных расстояний ---")
    rng = np.random.default_rng(seed=42)

    # Для теста берем N=800, M=800, D=30 (всего 640 000 попарных расстояний)
    N, M, D = 800, 800, 30
    A = rng.normal(loc=0.0, scale=1.0, size=(N, D)).astype(np.float32)
    B = rng.normal(loc=0.0, scale=1.0, size=(M, D)).astype(np.float32)

    # 1. Замер медленного способа
    t0 = time.perf_counter()
    res_slow = pairwise_slow(A, B)
    t_slow = time.perf_counter() - t0
    print(f"1. Двойной цикл for:        {t_slow:.4f} сек")

    # 2. Замер полувекторного способа
    t0 = time.perf_counter()
    res_semi = pairwise_semi_vectorized(A, B)
    t_semi = time.perf_counter() - t0
    print(f"2. Полувекторный (1 цикл):   {t_semi:.4f} сек")

    # 3. Замер полностью векторного способа
    t0 = time.perf_counter()
    res_fast = pairwise_fully_vectorized(A, B)
    t_fast = time.perf_counter() - t0
    print(f"3. Векторный (без циклов):   {t_fast:.4f} сек")

    # Проверка точности (паритет с эталоном)
    if res_fast is not None:
        matches = np.allclose(res_slow, res_fast, atol=1e-5)
        print(f"\nПобитовое совпадение с эталоном: {'✅ ДА' if matches else '❌ НЕТ'}")

        speedup = t_slow / max(t_fast, 1e-9)
        print(f"Итоговое ускорение: в {speedup:.1f} раз!")
        if speedup >= 50.0 and matches:
            print("🎉 КРИТЕРИЙ СДАН: Ускорение >= 50x и результат математически точен!")
        else:
            print("⚠️ Ускорение меньше 50x или результаты не сошлись.")


if __name__ == "__main__":
    print("=== Занятие 06: Запуск практики ===")

    # Проверка Задания 1
    xr, bc, cv, cd = task_1_data_cleaning()
    if xr is not None and np.all(xr >= 0):
        print("Задание 1.1 (ReLU): ✅ Зачтено!")
    if bc is not None and set(np.unique(bc)).issubset({0, 1}):
        print("Задание 1.2 (np.where): ✅ Зачтено!")
    if cv is not None and np.all(cv >= 0.01) and np.all(cv <= 0.99):
        print("Задание 1.3 (np.clip): ✅ Зачтено!")
    if cd is not None and not np.any(np.isnan(cd)) and not np.any(np.isinf(cd)):
        print("Задание 1.4 (np.nan_to_num): ✅ Зачтено!")

    # Проверка Задания 2
    X_rnd, y_rnd = task_2_random_generation()
    if X_rnd is not None and X_rnd.shape == (100, 4) and y_rnd.shape == (100,):
        print("Задание 2 (default_rng): ✅ Зачтено!")

    # Запуск бенчмарка
    benchmark_and_verify()
