"""
Практика: Создание массивов NumPy и датафреймов pandas с нуля.

Цель: набить руку на всех основных конструкторах данных,
которые используются в машинном обучении и анализе данных.
"""

import numpy as np
import pandas as pd


# =====================================================================
# Часть 1. Создание массивов NumPy
# =====================================================================
def task_1_numpy_creation() -> tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray
]:
    """
    Создай следующие 5 массивов:

    1.1. `arr_zeros`: 2D-матрица нулей формы (3, 4) строго типа float32.
         Используй: np.zeros(...

    1.2. `arr_range`: 1D-массив четных чисел от 10 до 30 включительно (10, 12, ..., 30).
         Используй: np.arange(...)

    1.3. `arr_linspace`: 1D-массив ровно из 5 чисел, равномерно разбивающих
         отрезок от 0.0 до 1.0 (т.е. 0.0, 0.25, 0.5, 0.75, 1.0).
         Используй: np.linspace(...)

    1.4. `arr_identity`: Единичная матрица (identity matrix) размера 4x4 типа float32.
         Используй: np.eye(...)

    1.5. `arr_synthetic_features`: Случайная матрица признаков для 100 объектов,
         у каждого 5 признаков (форма (100, 5)).
         Числа должны быть из нормального распределения (среднее loc=0.0, разброс scale=1.0).
         Используй: rng = np.random.default_rng(42); rng.normal(...)
    """
    # 1.1:
    arr_zeros = np.zeros(shape=(3, 4), dtype="float32")

    # 1.2:
    arr_range = np.arange(10, 31, 2)

    # 1.3:
    arr_linspace = np.linspace(0, 1, 5)

    # 1.4:
    arr_identity = np.eye(4, 4, dtype="float32")

    # TODO 1.5:
    rng = np.random.default_rng(42)
    arr_synthetic_features = rng.normal(loc=0.0, scale=1.0, size=(100, 5))
    return arr_zeros, arr_range, arr_linspace, arr_identity, arr_synthetic_features


# =====================================================================
# Часть 2. Создание pandas Series и DataFrame
# =====================================================================
def task_2_pandas_creation() -> tuple[
    pd.Series, pd.DataFrame, pd.DataFrame, pd.DataFrame
]:
    """
    Создай следующие 4 объекта pandas:

    2.1. `s_users`: Series с зарплатами трех человек:
         - Значения: [150_000, 220_000, 310_000]
         - Метки индекса: ['Alice', 'Bob', 'Charlie']
         - Имя Series (параметр name): 'salary'

    2.2. `df_from_dict`: DataFrame, созданный ИЗ СЛОВАРЯ СПИСКОВ/МАССИВОВ (самый частый способ в ML):
         - Колонка 'model': ['ResNet', 'BERT', 'LLaMA']
         - Колонка 'params_millions': [25.5, 110.0, 7000.0]
         - Колонка 'is_llm': [False, False, True]

    2.3. `df_from_records`: DataFrame, созданный ИЗ СПИСКА СЛОВАРЕЙ (как приходят ответы из API / JSON / БД):
         Записи о трех покупках:
         [
             {"order_id": 101, "item": "GPU", "price": 1200.0},
             {"order_id": 102, "item": "RAM", "price": 150.0},
             {"order_id": 103, "item": "SSD", "price": 90.0},
         ]

    2.4. `df_from_numpy`: DataFrame, созданный НАПРЯМУЮ ИЗ ЧИСЛОВОЙ МАТРИЦЫ NUMPY:
         - Сгенерируй матрицу NumPy формы (5, 3) из единиц (np.ones)
         - Создай из неё DataFrame с именами колонок: ['feature_1', 'feature_2', 'feature_3']
         - И кастомным индексом строк: ['sample_1', 'sample_2', 'sample_3', 'sample_4', 'sample_5']
    """
    # TODO 2.1:
    s_users = pd.Series(
        [150_000, 220_000, 310_000], index=["Alice", "Bob", "Charlie"], name="salary"
    )

    # TODO 2.2:
    df_from_dict = pd.DataFrame(
        {
            "model": ["ResNet", "BERT", "LLaMA"],
            "params_millions": [25.5, 110.0, 7000.0],
            "is_llm": [False, False, True],
        }
    )

    # TODO 2.3:
    df_from_records = pd.DataFrame(
        [
            {"order_id": 101, "item": "GPU", "price": 1200.0},
            {"order_id": 102, "item": "RAM", "price": 150.0},
            {"order_id": 103, "item": "SSD", "price": 90.0},
        ]
    )

    # TODO 2.4:
    np_matr = np.ones(shape=(5, 3))
    df_from_numpy = pd.DataFrame(
        np_matr,
        columns=["feature_1", "feature_2", "feature_3"],
        index=["sample_1", "sample_2", "sample_3", "sample_4", "sample_5"],
    )

    return s_users, df_from_dict, df_from_records, df_from_numpy


# =====================================================================
# Проверка и запуск
# =====================================================================
def run_checks():
    print("=" * 60)
    print("Проверка навыка создания массивов NumPy и датафреймов pandas")
    print("=" * 60)

    # 1. NumPy
    zeros, rng_arr, linsp, eye, feats = task_1_numpy_creation()

    np_success = True
    if zeros is not None:
        assert zeros.shape == (3, 4), (
            f"arr_zeros форма должна быть (3, 4), получена {zeros.shape}"
        )
        assert zeros.dtype == np.float32, (
            f"arr_zeros dtype должен быть float32, получен {zeros.dtype}"
        )
        assert np.all(zeros == 0), "arr_zeros должен содержать только нули"
        print("1.1 np.zeros:           ✅ Зачтено!")
    else:
        np_success = False

    if rng_arr is not None:
        assert np.array_equal(rng_arr, np.arange(10, 31, 2)), (
            "arr_range должен содержать [10, 12, ..., 30]"
        )
        print("1.2 np.arange:          ✅ Зачтено!")
    else:
        np_success = False

    if linsp is not None:
        assert len(linsp) == 5, (
            f"arr_linspace должен содержать 5 чисел, получено {len(linsp)}"
        )
        assert np.allclose(linsp, [0.0, 0.25, 0.5, 0.75, 1.0]), "arr_linspace неверен"
        print("1.3 np.linspace:        ✅ Зачтено!")
    else:
        np_success = False

    if eye is not None:
        assert eye.shape == (4, 4), (
            f"arr_identity форма должна быть (4, 4), получена {eye.shape}"
        )
        assert eye.dtype == np.float32, (
            f"arr_identity dtype должен быть float32, получен {eye.dtype}"
        )
        assert np.array_equal(eye, np.eye(4, dtype=np.float32)), (
            "arr_identity должна быть единичной матрицей"
        )
        print("1.4 np.eye:             ✅ Зачтено!")
    else:
        np_success = False

    if feats is not None:
        assert feats.shape == (100, 5), (
            f"arr_synthetic_features форма должна быть (100, 5), получена {feats.shape}"
        )
        print("1.5 rng.normal:         ✅ Зачтено!")
    else:
        np_success = False

    if not np_success:
        print("\nЧасть 1 (NumPy): ⚠️ Не все массивы созданы.")

    # 2. pandas
    s_u, df_dict, df_rec, df_np = task_2_pandas_creation()
    pd_success = True

    if s_u is not None:
        assert isinstance(s_u, pd.Series), "s_users должен быть pd.Series"
        assert list(s_u.index) == ["Alice", "Bob", "Charlie"], (
            f"Неверный индекс у s_users: {list(s_u.index)}"
        )
        assert s_u.name == "salary", (
            f"Имя Series должно быть 'salary', получено {s_u.name}"
        )
        assert s_u["Alice"] == 150_000, "Значения зарплат неверны"
        print("\n2.1 pd.Series:          ✅ Зачтено!")
    else:
        pd_success = False

    if df_dict is not None:
        assert isinstance(df_dict, pd.DataFrame), (
            "df_from_dict должен быть pd.DataFrame"
        )
        assert list(df_dict.columns) == ["model", "params_millions", "is_llm"], (
            "Неверные колонки в df_from_dict"
        )
        assert len(df_dict) == 3, "В df_from_dict должно быть 3 строки"
        print("2.2 DataFrame из dict:  ✅ Зачтено!")
    else:
        pd_success = False

    if df_rec is not None:
        assert isinstance(df_rec, pd.DataFrame), (
            "df_from_records должен быть pd.DataFrame"
        )
        assert list(df_rec.columns) == ["order_id", "item", "price"], (
            "Неверные колонки в df_from_records"
        )
        assert df_rec.iloc[0]["item"] == "GPU", "Первый заказ должен быть GPU"
        print("2.3 DataFrame из JSON:  ✅ Зачтено!")
    else:
        pd_success = False

    if df_np is not None:
        assert isinstance(df_np, pd.DataFrame), "df_from_numpy должен быть pd.DataFrame"
        assert df_np.shape == (5, 3), (
            f"Форма df_from_numpy должна быть (5, 3), получена {df_np.shape}"
        )
        assert list(df_np.columns) == ["feature_1", "feature_2", "feature_3"], (
            "Неверные колонки"
        )
        assert df_np.index[0] == "sample_1", "Неверный индекс строк"
        assert np.all(df_np.values == 1.0), "Значения должны быть единицами"
        print("2.4 DataFrame из NumPy: ✅ Зачтено!")
    else:
        pd_success = False

    if not pd_success:
        print("\nЧасть 2 (pandas): ⚠️ Не все объекты созданы.")

    if np_success and pd_success:
        print("\n🎉 Все 9 способов создания массивов и датафреймов успешно освоены!")


if __name__ == "__main__":
    run_checks()
