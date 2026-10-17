"""
Занятие 05: NumPy: ndarray, манипуляции с осями и Broadcasting.
Практические задания и тренажер размерностей.
"""

import numpy as np


# =====================================================================
# Задание 1. Базовые операции и создание массивов
# =====================================================================
def task_1_creation():
    """
    1. Создай массив zeros_arr из нулей формы (3, 4) типа float32.
    2. Создай массив seq_arr из четных чисел от 10 до 30 (не включая 30) через np.arange.
    3. Создай массив grid_arr из 5 чисел от 0 до 1 включительно через np.linspace.
    """
    zeros_arr = np.zeros((3, 4), dtype="float32")
    seq_arr = np.arange(10, 30, 2)
    grid_arr = np.linspace(0, 1, 5)

    return zeros_arr, seq_arr, grid_arr


# =====================================================================
# Задание 2. Views vs Copies (Безопасность памяти)
# =====================================================================
def task_2_views_copies():
    """
    Дана матрица A (3x3).
    1. Создай view первой строки (индекс 0) и измени ее первый элемент на 999.
       (Убедись, что исходная матрица A изменилась).
    2. Создай независимую копию (copy) второй строки (индекс 1) и измени ее элемент на 777.
       (Убедись, что исходная матрица A НЕ изменилась во второй строке).
    """
    A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    b = A[0]
    b[0] = 999
    print(A)
    c = A[1].copy()
    c[0] = 777
    print(A)

    # TODO: сделай view первой строки, измени view[0] = 999
    # TODO: сделай copy второй строки, измени copy[0] = 777

    return A


# =====================================================================
# Задание 3. Агрегации и оси (axis)
# =====================================================================
def task_3_axes():
    """
    Таблица данных: 4 студента (строки), 3 теста (столбцы).
    """
    scores = np.array([[80, 90, 85], [70, 75, 80], [95, 90, 92], [60, 65, 70]])

    # 1. Посчитай средний балл каждого студента (схлопнуть столбцы, движение по строкам)
    # Форма результата должна быть (4,)
    student_means = np.mean(scores, axis=1)
    # 2. Посчитай максимальный балл по каждому тесту (схлопнуть строки, движение по столбцам)
    # Форма результата должна быть (3,)
    test_maxes = np.max(scores, axis=0)

    return student_means, test_maxes


# =====================================================================
# Задание 4. Тренажер Broadcasting (Предсказание shape)
# =====================================================================
# Назови итоговый shape в виде кортежа, например: (3, 4) или (5, 3, 2).
# Если операция вызовет ошибку несовместимости, напиши строку "error".
# =====================================================================

BROADCASTING_TASKS = [
    # 1. Сложение матрицы и скаляра
    {"a_shape": (3, 4), "b_shape": (), "expected": (3, 4)},  # TODO
    # 2. Матрица (2, 3) и вектор (3,)
    {"a_shape": (2, 3), "b_shape": (3,), "expected": (2, 3)},  # TODO
    # 3. Матрица (2, 3) и вектор (2,)
    {"a_shape": (2, 3), "b_shape": (2,), "expected": "error"},  # TODO
    # 4. Столбец (4, 1) и строка (1, 5)
    {"a_shape": (4, 1), "b_shape": (1, 5), "expected": (4, 5)},  # TODO
    # 5. Вектор (5,) и вектор (5, 1)
    {"a_shape": (5,), "b_shape": (5, 1), "expected": (5, 5)},  # TODO
    # 6. Тензор (8, 1, 6, 1) и (7, 1, 5)
    {"a_shape": (8, 1, 6, 1), "b_shape": (7, 1, 5), "expected": (8, 7, 6, 5)},  # TODO
    # 7. Батч картинок (32, 64, 64, 3) и нормализация по каналам (3,)
    {"a_shape": (32, 64, 64, 3), "b_shape": (3,), "expected": (32, 64, 64, 3)},  # TODO
    # 8. Несовместимые размеры: (3, 4, 5) и (4, 3)
    {"a_shape": (3, 4, 5), "b_shape": (4, 3), "expected": "error"},  # TODO
]


def check_broadcasting_predictions():
    print("\n--- Проверка тренажера Broadcasting ---")
    correct = 0
    total = len(BROADCASTING_TASKS)

    for i, task in enumerate(BROADCASTING_TASKS, start=1):
        a_shape = task["a_shape"]
        b_shape = task["b_shape"]
        user_ans = task["expected"]

        # Вычисляем истинный ответ через NumPy
        try:
            arr_a = np.ones(a_shape)
            arr_b = np.ones(b_shape)
            real_res = (arr_a + arr_b).shape
        except ValueError:
            real_res = "error"

        if user_ans == real_res:
            print(f"[{i}/{total}] ✅ Верно! {a_shape} + {b_shape} -> {user_ans}")
            correct += 1
        else:
            print(
                f"[{i}/{total}] ❌ Ошибка! {a_shape} + {b_shape}: твой ответ {user_ans}, правильный: {real_res}"
            )

    print(f"\nИтог: {correct} из {total} верно.")


if __name__ == "__main__":
    print("=== Занятие 05: Запуск тестов ===")

    # Тест 1
    z, s, g = task_1_creation()
    if z is not None:
        print("Задание 1: zeros shape =", z.shape, "dtype =", z.dtype)
        print("Задание 1: seq =", s)
        print("Задание 1: grid =", g)

    # Тест 2
    a_res = task_2_views_copies()
    if a_res is not None and a_res[0, 0] == 999 and a_res[1, 0] == 4:
        print("Задание 2: ✅ View и Copy отработали корректно!")

    # Тест 3
    s_means, t_maxes = task_3_axes()
    if s_means is not None:
        print("Задание 3: Средние студентов:", s_means)
        print("Задание 3: Максимумы тестов:", t_maxes)

    # Тест 4 (Broadcasting)
    check_broadcasting_predictions()
