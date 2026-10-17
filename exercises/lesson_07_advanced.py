"""
Занятие 07 (Расширенная практика): Безопасная индексация, модификация данных
и реальный эксперимент CSV против Parquet.

Темы:
1. Фильтрация и модификация (.loc vs .iloc) со сложным нечисловым индексом.
2. Безопасная вставка и модификация без SettingWithCopyWarning.
3. Эксперимент: CSV vs Parquet на реальном объеме данных:
   - Размер файла на диске (сжатие).
   - Время полной загрузки (read throughput).
   - Время выборочного чтения колонок (column projection pushdown).
   - Сохранение строгой схемы типов данных (schema preservation).
"""

import os
import shutil
from typing import Tuple
import numpy as np
import pandas as pd


# =====================================================================
# Генератор тестового датасета
# =====================================================================
def generate_dataset(n_rows: int = 150_000, seed: int = 42) -> pd.DataFrame:
    """Генерирует реалистичный табличный датасет пользователей."""
    rng = np.random.default_rng(seed)
    departments = ["ML", "Backend", "Frontend", "Analytics", "DevOps", "QA"]
    grades = ["Junior", "Middle", "Senior", "Lead"]

    # Кастомный строковый индекс (например, уникальный код сотрудника)
    emp_ids = [f"EMP_{i:06d}" for i in range(1, n_rows + 1)]

    df = pd.DataFrame(
        {
            "dept": rng.choice(departments, size=n_rows),
            "grade": rng.choice(grades, size=n_rows),
            "experience_years": rng.integers(1, 15, size=n_rows, dtype=np.int16),
            "salary": rng.uniform(80_000.0, 500_000.0, size=n_rows).astype(np.float32),
            "projects_completed": rng.integers(1, 40, size=n_rows, dtype=np.int16),
            "is_mentor": rng.choice([True, False], size=n_rows, p=[0.2, 0.8]),
        },
        index=emp_ids,
    )
    # Приводим строки к category для оптимизации памяти
    df["dept"] = df["dept"].astype("category")
    df["grade"] = df["grade"].astype("category")
    return df


# =====================================================================
# Задание 1. Продвинутая индексация и булевы условия
# =====================================================================
def task_1_indexing_and_filtering(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series, float]:
    """
    1.1. Получи срез первых 10 сотрудников (позиции от 0 до 9 включительно)
         и первые 3 колонки. Используй ТОЛЬКО .iloc
    1.2. Найди зарплаты (salary) сотрудников, которые удовлетворяют условию:
         (отдел 'ML' ИЛИ 'Analytics') И при этом (grade == 'Senior' ИЛИ grade == 'Lead').
         Используй .loc и булеву маску со скобками.

    1.3. Посчитай среднюю зарплату (.mean()) для сотрудников из пункта 1.2.
    """
    # TODO 1.1: используй .iloc
    slice_top10 = df.iloc[0:10, 0:3]

    # TODO 1.2: используй .loc с побитовыми операторами & и |
    senior_ai_salaries = df.loc[
        ((df["dept"] == "ML") | (df["dept"] == "Analytics"))
        & ((df["grade"] == "Senior") | (df["grade"] == "Lead")),
        "salary",
    ]
    # 1.3: вызови .mean() от senior_ai_salaries
    mean_ai_salary = senior_ai_salaries.mean()

    return slice_top10, senior_ai_salaries, float(mean_ai_salary)


# =====================================================================
# Задание 2. Безопасная модификация без SettingWithCopyWarning
# =====================================================================
def task_2_safe_modification(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    2.1. Создай изолированную копию менторов:
         Отбери сотрудников, у которых is_mentor == True.
         Обязательно сделай .copy()!
         Добавь в этот НОВЫЙ датафрейм колонку 'mentor_bonus',
         равную 15% от их текущей зарплаты (salary * 0.15).

    2.2. Измени данные В ИСХОДНОМ датафрейме df БЕЗ ПРЕДУПРЕЖДЕНИЙ:
         Всем сотрудникам, у которых projects_completed > 25,
         увеличь зарплату (salary) на фиксированные 50 000.
         Используй строго .loc[условие, 'salary'] += 50000.
    """
    # TODO 2.1:
    mentors_df = df.loc[df["is_mentor"] == True].copy()
    mentors_df["mentor_bonus"] = mentors_df["salary"] * 0.15
    # TODO 2.2:
    # df.loc[...] += 50000
    df.loc[df["projects_completed"] > 25, "salary"] += 50000

    return mentors_df, df


# =====================================================================
# Задание 3. Ручная работа с Parquet (Колонки, Фильтры и Партиции)
# =====================================================================
def task_3_hands_on_parquet(
    df: pd.DataFrame, data_dir: str = "data/parquet_practice"
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    3.1. Сохранение и проекция колонок:
         - Сохрани датафрейм `df` в файл `f"{data_dir}/employees.parquet"`.
         - Считай из этого файла ТОЛЬКО две колонки: ['dept', 'salary'].
           Используй аргумент `columns=[...]` в `pd.read_parquet`.
    3.2. Фильтрация на диске без чтения лишних строк (Predicate Pushdown):
         - Считай из `f"{data_dir}/employees.parquet"` только тех сотрудников,
           у которых стаж `experience_years >= 10`.
           Используй аргумент `filters=[('experience_years', '>=', 10)]`.

    3.3. Физическое партиционирование по папкам на диске:
         - Сохрани `df` в директорию `f"{data_dir}/by_department"`
           с разделением по отделам через `partition_cols=['dept']`.
         - Считай из этой директории только отдел 'ML' через filters:
           `filters=[('dept', '==', 'ML')]`.
    """
    os.makedirs(data_dir, exist_ok=True)
    parquet_file = os.path.join(data_dir, "employees.parquet")
    partitioned_dir = os.path.join(data_dir, "by_department")

    # 3.1: Сохрани df в parquet_file, затем считай только ['dept', 'salary']
    df.to_parquet(parquet_file)
    df_cols = pd.read_parquet(parquet_file, columns=["dept", "salary"])

    # 3.2: Считай parquet_file с фильтром на стаж >= 10
    df_exp10 = pd.read_parquet(parquet_file, filters=[("experience_years", ">=", 10)])

    # 3.3: Сохрани с partition_cols=['dept'], затем считай только dept == 'ML'
    df.to_parquet(partitioned_dir, partition_cols=["dept"])
    df_ml = pd.read_parquet(partitioned_dir, filters=[("dept", "==", "ML")])

    return df_cols, df_exp10, df_ml


# =====================================================================
# Автоматическая проверка и запуск
# =====================================================================
def run_all_checks():
    print("=" * 65)
    print("Запуск проверки расширенной практики (Занятие 07)")
    print("=" * 65)

    df_raw = generate_dataset(n_rows=150_000, seed=42)
    print(f"Сгенерирован датасет: {df_raw.shape[0]} строк, {df_raw.shape[1]} колонок.")

    # Проверка Задания 1
    top10, ai_salaries, mean_ai = task_1_indexing_and_filtering(df_raw)
    if top10 is not None and ai_salaries is not None and mean_ai > 0:
        assert top10.shape == (10, 3), f"Ошибка формы top10: {top10.shape}"
        assert len(ai_salaries) > 0, "ai_salaries пустой!"
        print(f"\nЗадание 1 (Индексация и фильтрация): ✅ Зачтено!")
        print(f" - Средняя зарплата Senior/Lead в AI/Analytics: {mean_ai:,.2f} руб.")
    else:
        print("\nЗадание 1: ⚠️ Решение не закончено (вернулись None/нули).")

    # Проверка Задания 2
    df_for_task2 = df_raw.copy()
    mentors, df_mod = task_2_safe_modification(df_for_task2)
    if mentors is not None and "mentor_bonus" in mentors.columns and df_mod is not None:
        high_proj_mask = df_raw["projects_completed"] > 25
        salary_diff = df_mod.loc[high_proj_mask, "salary"] - df_raw.loc[high_proj_mask, "salary"]
        assert np.allclose(salary_diff, 50_000.0, atol=1.0), "Зарплата увеличена не на 50 000!"
        print(f"\nЗадание 2 (Безопасная модификация): ✅ Зачтено!")
        print(f" - Менторов выделено: {len(mentors):,}")
        print(f" - Зарплаты успешно повышены сотрудникам с >25 проектов.")
    else:
        print("\nЗадание 2: ⚠️ Решение не закончено.")

    # Проверка Задания 3 (Ручная работа с Parquet)
    print("\n--- Проверка Задания 3 (Ручная работа с Parquet) ---")
    data_dir = "data/parquet_practice"
    try:
        df_cols, df_exp10, df_ml = task_3_hands_on_parquet(df_raw, data_dir=data_dir)

        # Проверка 3.1
        if df_cols is not None:
            assert list(df_cols.columns) == ["dept", "salary"], (
                f"3.1: Ожидались колонки ['dept', 'salary'], получено: {list(df_cols.columns)}"
            )
            print(" - 3.1 (Чтение только нужных колонок): ✅ Зачтено!")
        else:
            print(" - 3.1: ⚠️ Решение не закончено.")

        # Проверка 3.2
        if df_exp10 is not None:
            assert (df_exp10["experience_years"] >= 10).all(), (
                "3.2: В датафрейм попали сотрудники со стажем < 10 лет!"
            )
            assert len(df_exp10) > 0, "3.2: Датафрейм пустой!"
            print(
                f" - 3.2 (Фильтрация на диске filters=[...]): ✅ Зачтено! (отобрано {len(df_exp10):,} чел)"
            )
        else:
            print(" - 3.2: ⚠️ Решение не закончено.")

        # Проверка 3.3
        if df_ml is not None:
            assert (df_ml["dept"] == "ML").all(), "3.3: В датафрейм попали не только из ML!"
            assert len(df_ml) > 0, "3.3: Датафрейм пустой!"
            part_dirs = os.listdir(os.path.join(data_dir, "by_department"))
            print(
                f" - 3.3 (Партиции на диске partition_cols): ✅ Зачтено! (созданы папки: {part_dirs[:3]}...)"
            )
        else:
            print(" - 3.3: ⚠️ Решение не закончено.")

        if df_cols is not None and df_exp10 is not None and df_ml is not None:
            print("\nЗадание 3 (Parquet API): ✅ Все пункты выполнены идеально!")

    finally:
        # Очищаем созданные файлы
        if os.path.exists(data_dir):
            shutil.rmtree(data_dir)


if __name__ == "__main__":
    run_all_checks()
