"""Занятие 12: качество данных. Реализуй четыре функции с TODO.

Запуск: .venv/bin/python exercises/lesson_12.py
Сначала прочитай docs/ПРАКТИКА_12_КАЧЕСТВО_ДАННЫХ.md.
Даты уже загружаются как datetime. Исходные таблицы не менять.
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "lesson_12"
OUTPUT = Path(__file__).resolve().parent / "outputs" / "lesson_12"
SNAPSHOT = pd.Timestamp("2026-11-20 12:00:00")


def task_1_profile(orders: pd.DataFrame) -> pd.DataFrame:
    """Индекс — все исходные столбцы в исходном порядке.

    Столбцы: missing_count, missing_share, unique_count.
    unique_count — количество разных НЕПУСТЫХ значений.
    Бесконечность не является пропуском: её исследуй отдельно в отчёте.
    df = pd.DataFrame()
    """
    df = pd.DataFrame()
    df['missing_count']=orders.isna().sum()
    df['missing_share']=orders.isna().mean()
    df['unique_count']=orders.nunique()
    return df


def task_2_clean(orders: pd.DataFrame, receipts: pd.DataFrame) -> pd.DataFrame:
    """Одна строка на заказ; правила отбора и исправления — в инструкции.

    Верни копию исходных столбцов orders, исправив amount и channel,
    отобрав допустимые версии/заказы. Сортировка по order_id, обычный
    последовательный индекс. Сохрани NULL цели для незрелых заказов.
    """
    df = orders.copy()
    df = df[df['available_at']<=df['prediction_at']]
    df = df.sort_values(by=['available_at', 'row_id'], ascending=[False, True])
    df = df.drop_duplicates(subset='order_id', keep='first')
    df = df.dropna(subset=['customer_id'])
    df['channel']=df['channel'].str.lower().str.strip()
    df=df[(df['channel']=='web' )| (df['channel']=='app')]
    df = df.merge(receipts[['available_at', 'order_id']], on='order_id', how='left', validate='many_to_one')
    df['amount']=df['amount'].mask((((df['amount'].isna()) | (df['amount'] <0 )| (np.isinf(df['amount']))) & (df['available_at_y']<=df['prediction_at'])), df['order_id'].map(receipts.set_index('order_id')['amount']))
    df = df[(df['amount'].notna()) & (df['amount'] >=0) & ~(np.isinf(df['amount']))]
    df = df.drop(columns=["available_at_y"])
    df = df.rename(columns={'available_at_x':'available_at'})
    df = df.sort_values('order_id', ascending=True)
    df.reset_index(drop=True, inplace=True)
    return df


def task_3_contacts(clean: pd.DataFrame, contacts: pd.DataFrame) -> pd.Series:
    """Число обращений по КАЖДОМУ заказу, доступных к его prediction_at.

    Проверяй и event_at, и available_at: оба <= prediction_at.
    Индекс Series — order_id, имя — contacts_before; порядок как у clean.
    Нет подходящих обращений — 0. Все контакты уникальны по contact_id.
    """
    contacts = contacts.merge(clean[['prediction_at', 'order_id']], on="order_id", how='left')
    contacts = contacts[(contacts['prediction_at']>=contacts['event_at'])&(contacts['prediction_at']>=contacts['available_at'])]
    contacts=contacts.groupby('order_id').size()
    contacts = contacts.reindex(clean['order_id'], fill_value=0)
    contacts_before = contacts
    contacts_before.name='contacts_before'
    # TODO: При соединении не размножь итоговые строки заказов.
    return contacts_before


def task_4_training(clean: pd.DataFrame, counts: pd.Series) -> pd.DataFrame:
    """Собери таблицу обучения только для заказов с полным 30-дневным окном.

    Готовность: placed_at + 30 дней <= SNAPSHOT и цель не пропущена.
    Столбцы в порядке: order_id, customer_id, amount, channel,
    contacts_before, returned_30d.
    lifetime_spend_at_extract исключить. returned_30d — цель, не признак.
    order_id/customer_id — служебные ID, не готовые числовые признаки модели.
    Сортировка по order_id, последовательный индекс.
    """
    clean = clean.merge(counts, on='order_id')
    clean = clean[pd.to_datetime(clean["placed_at"])+pd.Timedelta(days=30)<= pd.Timestamp("2026-11-20 12:00:00")]
    clean = clean[clean['returned_30d'].notna()]
    clean = clean.loc[:, ['order_id', 'customer_id', 'amount', 'channel', 'contacts_before', 'returned_30d']]
    clean = clean.sort_values(by='order_id', ascending=True)
    return clean.reset_index(drop=True)


def main() -> None:
    # Инфраструктура загрузки и проверки уже готова.
    import json

    expected = json.loads((DATA / "checks.json").read_text())
    orders = pd.read_csv(DATA / "orders_dirty.csv",
                         parse_dates=["placed_at", "prediction_at", "available_at"])
    receipts = pd.read_csv(DATA / "receipts.csv", parse_dates=["available_at"])
    contacts = pd.read_csv(DATA / "contacts.csv", parse_dates=["event_at", "available_at"])
    originals = [x.copy(deep=True) for x in [orders, receipts, contacts]]
    OUTPUT.mkdir(parents=True, exist_ok=True)

    profile = task_1_profile(orders)
    assert list(profile.index) == list(orders.columns)
    assert list(profile.columns) == ["missing_count", "missing_share", "unique_count"]
    for col in orders:
        values = orders[col]
        n_missing = len(values) - values.count()
        np.testing.assert_allclose(
            profile.loc[col].to_numpy(dtype=float),
            [n_missing, n_missing / len(values), len(set(values.dropna()))],
        )
    profile.to_csv(OUTPUT / "profile.csv")
    print("1/4: профиль — OK")

    clean = task_2_clean(orders, receipts)
    reference = pd.DataFrame(expected["clean"])
    date_cols = ["placed_at", "prediction_at", "available_at"]
    for col in date_cols:
        reference[col] = pd.to_datetime(reference[col])
    assert list(clean.columns) == list(orders.columns), "Сохрани исходные столбцы"
    assert clean["order_id"].is_unique
    assert clean.index.equals(pd.RangeIndex(len(clean))), "Сбрось индекс"
    pd.testing.assert_frame_equal(
        clean[list(reference.columns)], reference, check_dtype=False,
    )
    # Все остальные поля должны происходить из выбранной исходной строки.
    untouched = [c for c in orders if c not in ["amount", "channel"]]
    selected = orders.set_index("row_id").loc[clean["row_id"]].reset_index()
    pd.testing.assert_frame_equal(clean[untouched], selected[untouched], check_dtype=False)
    clean.to_csv(OUTPUT / "clean_orders.csv", index=False)
    print("2/4: очистка — OK")

    counts = task_3_contacts(clean, contacts)
    assert isinstance(counts, pd.Series) and counts.name == "contacts_before"
    assert counts.index.name == "order_id"
    assert list(counts.index) == list(clean["order_id"])
    for oid in clean["order_id"]:
        # Ожидаемое значение — метаданные синтетического сценария.
        assert counts.loc[oid] == expected["contacts"][str(int(oid))]
    counts.to_csv(OUTPUT / "contacts_before.csv")
    print("3/4: история без будущего — OK")

    training = task_4_training(clean, counts)
    reference = pd.DataFrame(expected["features"])
    pd.testing.assert_frame_equal(training, reference, check_dtype=False)
    training.to_csv(OUTPUT / "training.csv", index=False)
    for actual, original in zip([orders, receipts, contacts], originals):
        pd.testing.assert_frame_equal(actual, original)
    print("4/4: таблица обучения — OK")
    print("Осталась защита отчёта: docs/ОТЧЕТ_12_КАЧЕСТВО_ДАННЫХ.md")


if __name__ == "__main__":
    main()
