"""Задание 5: три небольших теста. Инструменты — в инструкции.

Фикстуры и генерация данных не нужны: примеры должны быть заданы явно.
Не удаляй TODO через pass: тест должен действительно проверять результат.
"""

import numpy as np

from exercises.lesson_13 import distances_from_lesson_06


def test_known_distance():
    """A = [[0., 0.]], B = [[3., 4.]]; ожидаем матрицу [[5.]].

    Передай NumPy-массивы в distances_from_lesson_06 и сравни с ожидаемой матрицей.
    """
    np.testing.assert_allclose(
        distances_from_lesson_06(np.array([[0.0, 0.0]]), np.array([[3.0, 4.0]])), np.array([[5.0]])
    )


def test_identical_points():
    """Расстояние между двумя одинаковыми точками равно нулю.

    Выбери конкретную двумерную точку; проверь и форму (1, 1), и значение.
    """
    dst = distances_from_lesson_06(np.array([[1.0, 1.0]]), np.array([[1.0, 1.0]]))
    np.testing.assert_allclose(dst, np.array([[0.0]]))
    assert dst.shape == (1, 1)


def test_inputs_unchanged():
    """Задай два маленьких массива, сохрани .copy(), вызови функцию.

    Проверь, что исходные массивы остались равны сохранённым копиям.
    """
    a = np.array([[0.0, 0.0]])
    a_1 = a.copy()
    b = np.array([[3.0, 4.0]])
    b_1 = b.copy()
    distances_from_lesson_06(a, b)
    np.testing.assert_array_equal(a, a_1)
    np.testing.assert_array_equal(b, b_1)


# Импорт выше понадобится в твоих тестах.
assert callable(distances_from_lesson_06)
