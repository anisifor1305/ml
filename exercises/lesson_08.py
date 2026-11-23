"""Занятие 08: pandas — агрегации, merge и трансформация формы (reshape).

Практическая работа: Сборка витрины признаков (Feature Store) для ML-модели.
Все задачи выполняются строго с использованием векторизованных методов pandas.
"""

from typing import Tuple

import numpy as np
import pandas as pd


# =====================================================================
# Генерация синтетических данных реального ML-пайплайна
# =====================================================================
def generate_ecommerce_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Генерирует три связанные таблицы: пользователи, транзакции, тикеты."""
    rng = np.random.default_rng(42)

    # 1. Таблица пользователей (users)
    n_users = 100
    user_ids = np.arange(1, n_users + 1)
    cities = rng.choice(["MSK", "SPB", "KZN", "NSK"], size=n_users, p=[0.4, 0.3, 0.15, 0.15])
    ages = rng.integers(18, 65, size=n_users)
    reg_dates = pd.date_range("2025-01-01", periods=60, freq="D")
    user_reg = rng.choice(reg_dates, size=n_users)

    users = pd.DataFrame({
        "user_id": user_ids,
        "city": cities,
        "age": ages,
        "registration_date": user_reg,
    })

    # 2. Таблица транзакций (transactions)
    # Заметь: у части пользователей транзакций может не быть, а у кого-то их много
    n_tx = 1500
    tx_users = rng.choice(user_ids[:85], size=n_tx)  # у пользователей 86..100 нет покупок!
    tx_dates = pd.date_range("2026-01-01 08:00:00", periods=5000, freq="15min")
    cat_list = ["Food", "Tech", "Travel", "Clothes"]
    categories = rng.choice(cat_list, size=n_tx, p=[0.4, 0.2, 0.1, 0.3])
    amounts = np.round(rng.exponential(scale=1500.0, size=n_tx) + 100.0, 2)

    transactions = pd.DataFrame({
        "tx_id": np.arange(1001, 1001 + n_tx),
        "user_id": tx_users,
        "timestamp": rng.choice(tx_dates, size=n_tx),
        "category": categories,
        "amount": amounts,
    })

    # 3. Таблица обращений в поддержку (support_tickets)
    n_tickets = 200
    ticket_users = rng.choice(user_ids[:60], size=n_tickets)
    issue_types = rng.choice(["Delivery", "Payment", "Refund"], size=n_tickets)
    resolution_hours = np.round(rng.uniform(1.0, 48.0, size=n_tickets), 1)

    tickets = pd.DataFrame({
        "ticket_id": np.arange(5001, 5001 + n_tickets),
        "user_id": ticket_users,
        "issue_type": issue_types,
        "resolution_hours": resolution_hours,
    })

    return users, transactions, tickets


# =====================================================================
# Задание 1. Группировка и мульти-агрегация (.agg)
# =====================================================================
def task_1_user_aggregations(transactions: pd.DataFrame) -> pd.DataFrame:
    """Считает агрегированные признаки по каждому пользователю на основе транзакций.

    Args:
        transactions: Таблица транзакций (колонки: tx_id, user_id, amount, ...).

    Returns:
        pd.DataFrame: Таблица, где индекс — user_id, а колонки:
            - 'total_spend': суммарные траты пользователя (сумма amount);
            - 'mean_spend': средний чек пользователя (среднее amount);
            - 'tx_count': количество транзакций пользователя (count по tx_id);
            - 'max_spend': максимальная сумма покупки (максимум amount).
    """
    # TODO 1.1: Сгруппируй transactions по 'user_id'.
    tr_grouped = transactions.groupby('user_id')
    # TODO 1.2: Используй .agg(...) со словарём или кортежами названий колонок:
    #           amount -> 'sum', 'mean', 'max'
    #           tx_id -> 'count'
    user_stats = tr_grouped.agg({
        'amount': ['sum', 'mean', 'max'],
        'tx_id': ['count']
    })
    # TODO 1.3: Переименуй колонки в 'total_spend', 'mean_spend', 'max_spend', 'tx_count'.
    user_stats.columns = ["total_spend", "mean_spend", "max_spend", "tx_count"]
    return user_stats


# =====================================================================
# Задание 2. Внутригрупповая нормализация (.transform)
# =====================================================================
def task_2_group_transform(transactions: pd.DataFrame) -> pd.DataFrame:
    """Вычисляет отклонение транзакции от среднего чека категории через .transform.

    В ML полезен признак: «насколько эта конкретная покупка отличается от средней
    покупки в этой же категории (Food, Tech и т.д.)».

    Args:
        transactions: Датафрейм транзакций.

    Returns:
        pd.DataFrame: Копия датафрейма transactions с двумя новыми колонками:
            - 'cat_mean_amount': средний чек по категории (через transform('mean'));
            - 'diff_from_cat_mean': разность (amount - cat_mean_amount).
    """
    # TODO 2.1: Сделай копию transactions: df = transactions.copy()
    df = transactions.copy()
    # TODO 2.2: Сгруппируй df по 'category' и примени к 'amount' метод .transform('mean').
    #           Сохрани в df['cat_mean_amount'].
    df['cat_mean_amount']= df.groupby('category')['amount'].transform('mean')
    # TODO 2.3: Посчитай df['diff_from_cat_mean'] = df['amount'] - df['cat_mean_amount'].
    df['diff_from_cat_mean']=df['amount']-df['cat_mean_amount']
    return df


# =====================================================================
# Задание 3. Объединение витрины признаков (merge)
# =====================================================================
def task_3_feature_store_merge(
    users: pd.DataFrame,
    user_stats: pd.DataFrame,
) -> pd.DataFrame:
    """Объединяет базовую таблицу пользователей со статистиками трат через left join.

    Args:
        users: Таблица пользователей (100 строк, уникальный user_id).
        user_stats: Таблица агрегатов из Задания 1 (индекс user_id).

    Returns:
        pd.DataFrame: Итоговая таблица со 100 строками.
            Пропуски (NaN) в колонках 'total_spend', 'mean_spend', 'max_spend', 'tx_count'
            должны быть заполнены нулями (0.0).
            Проверка: должна быть строгая валидация '1:1' (один юзер — одна строка стат).
    """
    # TODO 3.1: Сделай сброс индекса у user_stats (.reset_index()), чтобы user_id стал колонкой.
    user_stats = user_stats.reset_index()
    # TODO 3.2: Вызови pd.merge(users, user_stats, on='user_id', how='left', validate='1:1').
    result_users = pd.merge(users, user_stats, on="user_id", how="left", validate='1:1')
    # TODO 3.3: Заполни пропуски в числовых колонках нулями через .fillna(0.0).
    result_users[['total_spend', 'mean_spend', 'max_spend', 'tx_count']] = result_users[['total_spend', 'mean_spend', 'max_spend', 'tx_count']].fillna(0)
    return result_users


# =====================================================================
# Задание 4. Трансформация формы (pivot_table vs melt)
# =====================================================================
def task_4_category_pivot(transactions: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Разворачивает категории трат в широкую матрицу признаков и обратно.

    Args:
        transactions: Таблица транзакций.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]:
            1. wide_df: Сводная таблица (pivot_table), где:
               - индекс: user_id;
               - колонки: категории товаров (Food, Tech, Travel, Clothes);
               - значения: сумма покупок ('sum' по amount);
               - пропуски заполнены нулем (fill_value=0.0).
            2. long_df: Обратное преобразование wide_df в длинный формат через .melt():
               - колонки: ['user_id', 'category', 'total_amount'].
    """
    # TODO 4.1: Сформируй wide_df через transactions.pivot_table(...)
    wide_df = transactions.pivot_table(index="user_id", columns="category", values='amount', aggfunc='sum', fill_value=0.0)
    # TODO 4.2: Сформируй long_df через wide_df.reset_index().melt(...)
    long_df = wide_df.reset_index().melt(id_vars="user_id", var_name="category", value_name="total_amount")
    return (wide_df, long_df)



# =====================================================================
# Задание 5. Временные признаки (.dt и ресемплинг)
# =====================================================================
def task_5_datetime_features(transactions: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Извлекает календарные признаки и считает среднесуточный объем трат.

    Args:
        transactions: Датафрейм транзакций.

    Returns:
        Tuple[pd.DataFrame, pd.Series]:
            1. df_with_features: Копия transactions с тремя новыми колонками:
               - 'hour': час транзакции (0..23);
               - 'dayofweek': день недели (0 = понедельник, 6 = воскресенье);
               - 'is_weekend': булев флаг (True, если dayofweek >= 5, иначе False).
            2. daily_spend: Series с суммарными тратами по дням:
               - сгруппируй transactions по дате без времени (через .dt.floor('D') или .dt.date)
                 и посчитай сумму amount.
    """
    # TODO 5.1: Убедись, что transactions['timestamp'] имеет тип datetime64 (pd.to_datetime).
    df_with_features = transactions.copy()
    df_with_features['timestamp'] = pd.to_datetime(transactions['timestamp'])
    # TODO 5.2: Извлеки hour, dayofweek и is_weekend через аксессор .dt.
    df_with_features['hour'] = df_with_features['timestamp'].dt.hour
    df_with_features['dayofweek'] = df_with_features['timestamp'].dt.day_of_week
    df_with_features['is_weekend'] = df_with_features['timestamp'].dt.day_of_week>=5

    # TODO 5.3: Посчитай daily_spend.
    daily_spend = df_with_features.groupby(df_with_features['timestamp'].dt.floor('D'))["amount"].agg("sum")
    return df_with_features, daily_spend


# =====================================================================
# Автоматическая проверка всех заданий
# =====================================================================
def main() -> None:
    print("=" * 70)
    print("ТЕСТИРОВАНИЕ: ЗАНЯТИЕ 08 (PANDAS АГРЕГАЦИИ, MERGE, RESHAPE)")
    print("=" * 70)

    users, tx, tickets = generate_ecommerce_data()

    # --- Проверка Задания 1 ---
    print("\n[1/5] Проверка task_1_user_aggregations...")
    u_stats = task_1_user_aggregations(tx)
    assert u_stats is not None, "task_1 вернула None!"
    assert len(u_stats) == 85, f"Ожидалось 85 пользователей с покупками, получено {len(u_stats)}"
    for col in ["total_spend", "mean_spend", "max_spend", "tx_count"]:
        assert col in u_stats.columns, f"Колонка {col} отсутствует в результате!"
    assert u_stats["tx_count"].sum() == 1500, "Сумма всех tx_count должна быть равна 1500!"
    print("✅ Задание 1 пройдено успешно!")

    # --- Проверка Задания 2 ---
    print("\n[2/5] Проверка task_2_group_transform...")
    tx_trans = task_2_group_transform(tx)
    assert tx_trans is not None, "task_2 вернула None!"
    assert len(tx_trans) == len(tx), "Длина таблицы после transform должна совпадать с исходной!"
    assert "cat_mean_amount" in tx_trans.columns
    assert "diff_from_cat_mean" in tx_trans.columns
    # Проверяем математику: сумма отклонений внутри категории должна быть около 0
    food_diff_sum = tx_trans.loc[tx_trans["category"] == "Food", "diff_from_cat_mean"].sum()
    assert np.isclose(food_diff_sum, 0.0, atol=1e-3), "Сумма отклонений от среднего должна быть 0!"
    print("✅ Задание 2 пройдено успешно!")

    # --- Проверка Задания 3 ---
    print("\n[3/5] Проверка task_3_feature_store_merge...")
    feature_store = task_3_feature_store_merge(users, u_stats)
    assert feature_store is not None, "task_3 вернула None!"
    assert len(feature_store) == 100, f"Ожидалось 100 юзеров, получено {len(feature_store)}"
    # Проверяем, что у юзеров без покупок пропуски стали 0.0
    user_100 = feature_store.loc[feature_store["user_id"] == 100].iloc[0]
    assert user_100["total_spend"] == 0.0, "У пользователя 100 траты должны быть 0.0!"
    assert user_100["tx_count"] == 0, "У пользователя 100 число покупок должно быть 0!"
    print("✅ Задание 3 пройдено успешно!")

    # --- Проверка Задания 4 ---
    print("\n[4/5] Проверка task_4_category_pivot...")
    wide, long_df = task_4_category_pivot(tx)
    assert wide is not None and long_df is not None, "task_4 вернула None!"
    assert wide.shape[0] == 85, f"В широкой таблице должно быть 85 юзеров, получено {wide.shape[0]}"
    for cat in ["Food", "Tech", "Travel", "Clothes"]:
        assert cat in wide.columns, f"Категория {cat} отсутствует в колонках!"
    assert len(long_df) == 340, f"Ожидалось 340 строк, получено {len(long_df)}"
    print("✅ Задание 4 пройдено успешно!")

    # --- Проверка Задания 5 ---
    print("\n[5/5] Проверка task_5_datetime_features...")
    df_dt, daily = task_5_datetime_features(tx)
    assert df_dt is not None and daily is not None, "task_5 вернула None!"
    for col in ["hour", "dayofweek", "is_weekend"]:
        assert col in df_dt.columns, f"Колонка {col} отсутствует!"
    assert df_dt["is_weekend"].dtype == bool, "is_weekend должен иметь тип bool!"
    assert np.isclose(daily.sum(), tx["amount"].sum()), "Сумма трат по дням должна совпадать!"
    print("✅ Задание 5 пройдено успешно!")

    print("\n" + "=" * 70)
    print("🎉 ВСЕ 5 ЗАДАНИЙ ЗАНЯТИЯ 08 ВЫПОЛНЕНЫ БЕЗУПРЕЧНО!")
    print("=" * 70)


if __name__ == "__main__":
    main()
