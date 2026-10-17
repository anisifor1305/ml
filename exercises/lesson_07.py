"""
Занятие 07: pandas: Series, DataFrame, индексация и память.
Практические задания и тесты.
"""

from numpy import exceptions
import numpy as np
import pandas as pd


def generate_dataset(n_rows: int = 50_000) -> pd.DataFrame:
    """Генерация синтетического датасета клиентов для практики."""
    rng = np.random.default_rng(seed=42)
    cities = ["Москва", "СПб", "Казань", "Екатеринбург", "Новосибирск"]
    devices = ["ios", "android", "web"]

    df = pd.DataFrame(
        {
            "user_id": np.arange(100_000, 100_000 + n_rows, dtype=np.int64),
            "city": rng.choice(cities, size=n_rows),
            "age": rng.integers(18, 70, size=n_rows, dtype=np.int64),
            "device": rng.choice(devices, size=n_rows),
            "spend": rng.uniform(100.0, 10_000.0, size=n_rows),  # float64
            "is_subscriber": rng.choice([True, False], size=n_rows),
        }
    )
    return df


# =====================================================================
# Задание 1. loc против iloc до автоматизма
# =====================================================================
def task_1_indexing(df: pd.DataFrame):
    """
    1.1. С помощью .iloc выбери первые 5 строк (0..4) и первые 3 колонки (0..2).
    1.2. С помощью .iloc выбери значение из последней строки и последней колонки (скаляр).
    1.3. С помощью .loc выбери строки с метками от 10 до 15 (включительно!)
         и только колонки ['city', 'spend'].
    1.4. С помощью .loc достань возраст пользователя со строки с индексом 42 (скаляр).
    """
    # 1.1
    part_1 = df.iloc[:5, :3]  # TODO: df.iloc[...]

    # 1.2
    part_2 = df.iloc[(0, -1)]

    # 1.3
    part_3 = df.loc[10:15, ["city", "spend"]]

    # 1.4
    part_4 = df.loc[42, "age"]

    return part_1, part_2, part_3, part_4


# =====================================================================
# Задание 2. Булева фильтрация
# =====================================================================
def task_2_filtering(df: pd.DataFrame):
    """
    2.1. Отфильтруй пользователей: возраст >= 25 И устройство == 'ios' (все колонки).
    2.2. С помощью .loc выбери только колонку 'spend' для пользователей из города 'Москва'
         с возрастом < 30.
    2.3. Отфильтруй пользователей: траты spend > 8000 ИЛИ являются подписчиками is_subscriber == True.
    """
    # 2.1
    ios_seniors = df[(df["age"] >= 25) & (df["device"] == "ios")]

    # 2.2
    moscow_young_spend = df.loc[(df["city"] == "Москва") & (df["age"] < 30), "spend"]

    # 2.3
    rich_or_subscribers = df.loc[(df["spend"] > 8000) | (df["is_subscriber"] == True)]

    return ios_seniors, moscow_young_spend, rich_or_subscribers


# =====================================================================
# Задание 3. Модификация без SettingWithCopyWarning
# =====================================================================
def task_3_modification(df: pd.DataFrame):
    """
    3.1. Создай срез ios_df, содержащий пользователей с device == 'ios'.
         Сделай это БЕЗОПАСНО через .copy(), чтобы не было предупреждений.
         Затем добавь в ios_df новую колонку 'bonus', равную spend * 0.1.

    3.2. В ИСХОДНОМ датафрейме df с помощью .loc увеличь траты (spend) на 1000.0
         всем, у кого is_subscriber == True.
    """
    # 3.1
    ios_df = df[df["device"] == "ios"].copy()
    ios_df["bonus"] = ios_df["spend"] * 0.1

    # 3.2
    df.loc[df["is_subscriber"] == True, "spend"] += 1000

    return ios_df, df


# =====================================================================
# Задание 4. Оптимизация памяти (минимум в 3 раза)
# =====================================================================
def task_4_memory_optimization(df: pd.DataFrame):
    """
    Уменьши потребление памяти датафрейма df:
    1. Переведи текстовые колонки 'city' и 'device' в тип 'category'.
    2. Переведи колонку 'age' в 'int8' (значения от 18 до 70 легко влезают в int8 от -128 до 127).
    3. Переведи колонку 'spend' из float64 в float32.
    4. Переведи колонку 'user_id' из int64 в int32.
    """
    initial_mem_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

    # TODO: примени .astype(...) к колонкам df:
    df["city"] = df["city"].astype("category")
    df["device"] = df["device"].astype("category")
    df["age"] = df["age"].astype("int8")
    df["spend"] = df["spend"].astype("float32")
    df["user_id"] = df["user_id"].astype("int32")

    final_mem_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    compression_ratio = initial_mem_mb / max(final_mem_mb, 1e-9)

    return df, initial_mem_mb, final_mem_mb, compression_ratio


if __name__ == "__main__":
    print("=== Занятие 07: Практика по pandas ===")
    raw_df = generate_dataset(50_000)
    print(f"Исходный датасет: {raw_df.shape[0]} строк, {raw_df.shape[1]} колонок.")

    # Проверка Задания 1
    p1, p2, p3, p4 = task_1_indexing(raw_df)
    if p1 is not None and p1.shape == (5, 3):
        print("Задание 1.1 (.iloc срез): ✅ Зачтено!")
    if p2 is not None and isinstance(p2, (bool, np.bool_)):
        print("Задание 1.2 (.iloc скаляр): ✅ Зачтено!")
    if p3 is not None and p3.shape == (6, 2) and list(p3.columns) == ["city", "spend"]:
        print("Задание 1.3 (.loc срез): ✅ Зачтено!")
    if p4 is not None and isinstance(p4, (int, np.integer)):
        print("Задание 1.4 (.loc скаляр): ✅ Зачтено!")

    # Проверка Задания 2
    f1, f2, f3 = task_2_filtering(raw_df)
    if f1 is not None and np.all((f1["age"] >= 25) & (f1["device"] == "ios")):
        print("Задание 2.1 (фильтр AND): ✅ Зачтено!")
    if f2 is not None and isinstance(f2, pd.Series):
        print("Задание 2.2 (.loc колонка): ✅ Зачтено!")
    if f3 is not None and np.all((f3["spend"] > 8000) | (f3["is_subscriber"] == True)):
        print("Задание 2.3 (фильтр OR): ✅ Зачтено!")

    # Проверка Задания 3
    ios_res, df_mod = task_3_modification(raw_df.copy())
    if ios_res is not None and "bonus" in ios_res.columns:
        print("Задание 3.1 (.copy + bonus): ✅ Зачтено!")
    if df_mod is not None:
        sub_mean = df_mod.loc[df_mod["is_subscriber"] == True, "spend"].mean()
        raw_sub_mean = raw_df.loc[raw_df["is_subscriber"] == True, "spend"].mean()
        if np.isclose(sub_mean - raw_sub_mean, 1000.0):
            print("Задание 3.2 (.loc in-place modify): ✅ Зачтено!")

    # Проверка Задания 4
    opt_df, init_mb, fin_mb, ratio = task_4_memory_optimization(raw_df.copy())
    if opt_df is not None and ratio >= 3.0:
        print(f"\nЗадание 4 (Оптимизация памяти): ✅ Зачтено!")
        print(
            f"Было: {init_mb:.2f} МБ -> Стало: {fin_mb:.2f} МБ (Сжатие в {ratio:.1f} раз!)"
        )
    elif opt_df is not None:
        print(f"\nЗадание 4: ⚠️ Сжатие составило {ratio:.1f}x (требуется >= 3.0x).")
