"""Короткая контрольная вводного блока: примерно 20–30 минут.

Три задания ниже. Все данные, запуск и проверки уже готовы.
Обычный запуск файла проверяет все три задания независимо: пустое задание
не мешает проверить остальные. Аргументы командной строки не нужны.

Запуск из корня проекта:
    .venv/bin/python exercises/checkpoint_0_short.py

Без отчёта, графиков, установки библиотек и Docker. Решения пишешь сам.
Здесь SQLite: данные загружаются в базу автоматически, имена таблиц без схемы.
"""

import sqlite3

import numpy as np
import pandas as pd


def task_1_clean(orders: pd.DataFrame) -> pd.DataFrame:
    """1. pandas: очисти заказы (ориентир 7–10 минут).

    Одна исходная строка — один заказ, повторов нет.
    Столбцы:
      order_id — номер заказа; customer_id — номер клиента;
      amount — сумма; available_at — время доступности записи;
      prediction_at — момент, на который готовим сведения для прогноза.
    Даты уже загружены как datetime.

    Оставь строки, где:
      - customer_id известен;
      - amount конечный и неотрицательный (0 допустим);
      - available_at <= prediction_at (равенство допустимо).
    Сохрани все исходные столбцы в том же порядке.
    Сортировка order_id ASC, последовательный индекс с 0. Вход не менять.
    Верни DataFrame. Подставлять/восстанавливать суммы не нужно.
    """
    orders = orders[(orders["customer_id"].notna()) & (np.isfinite(orders["amount"]))
                    & (pd.to_datetime(orders['available_at']) <=
                    pd.to_datetime(orders['prediction_at']))
                    &( orders['amount'] >= 0)]
    orders = orders.sort_values(['order_id'], ascending=[True])
    orders = orders.reset_index(drop=True)
    return orders


def task_2_sql() -> str:
    """2. SQL: верни строку с одним SELECT (ориентир 7–10 минут).

    Таблицы базы, уже загруженные за тебя:
      customers: customer_id, name — по одной строке на клиента;
      clean_orders: order_id, customer_id, amount — только корректные заказы.
    Задание НЕ зависит от готовности твоего task_1_clean.

    Выведи ВСЕХ клиентов, включая клиентов без заказов:
      customer_id, name, orders_count, total_amount.
    orders_count — количество заказов (без заказов 0).
    total_amount — сумма заказов (без заказов NULL; НЕ заменять на 0).
    Используй LEFT JOIN и GROUP BY. Сортировка customer_id ASC.
    Напиши SQL внутри тройных кавычек после return; выполнение готово ниже.
    """
    return """
    SELECT customers.customer_id, name,
    COUNT(clean_orders.order_id) AS orders_count,
    SUM(amount) AS total_amount
    FROM customers
    LEFT JOIN clean_orders ON customers.customer_id=clean_orders.customer_id
    GROUP BY customers.customer_id
    ORDER BY customers.customer_id ASC;
    """


def task_3_numpy(seed: int, n: int) -> tuple:
    """3. NumPy: случайные данные и оси (ориентир 3–5 минут).

    Создай новый default_rng с ПЕРЕДАННЫМ seed.
    Сгенерируй X формы (n, 3): normal с loc=0, scale=1, стандартный float64.
    Посчитай среднее отдельно для каждого из трёх столбцов.
    Верни пару X, means; means — NumPy-массив формы (3,).
    Функция при повторном вызове с теми же аргументами должна повторять результат.
    n и seed не фиксируй внутри функции.
    """
    rng = np.random.default_rng(seed)
    mat = rng.normal(loc=0, scale=1, size=(n, 3))
    first = mat[:, 0].mean()
    second = mat[:, 1].mean()
    third = mat[:, 2].mean()
    return (mat, np.array([first, second, third]))

# Готовые исходные данные. Их можно смотреть, но не менять ради сдачи.
def source_orders() -> pd.DataFrame:
    df = pd.DataFrame({
        "order_id": [106, 102, 108, 101, 105, 103, 107, 104],
        "customer_id": [3, 1, 1, 1, 2, 2, None, 2],
        "amount": [300., 50., np.inf, 100., 0., np.nan, 20., -10.],
        "available_at": ["10:00", "13:00", "11:00", "11:00", "12:00",
                         "11:00", "11:00", "11:00"],
    })
    df["available_at"] = pd.to_datetime("2026-11-01 " + df["available_at"])
    df["prediction_at"] = pd.Timestamp("2026-11-01 12:00")
    return df


def check_pandas() -> None:
    orders = source_orders()
    before = orders.copy(deep=True)
    actual = task_1_clean(orders)
    expected = before.set_index("order_id").loc[[101, 105, 106]].reset_index()
    pd.testing.assert_frame_equal(actual, expected)
    pd.testing.assert_frame_equal(orders, before)
    # Выбор не должен зависеть от текущего порядка строк или старого индекса.
    shuffled = before.iloc[::-1].copy()
    pd.testing.assert_frame_equal(task_1_clean(shuffled), expected)
    pd.testing.assert_frame_equal(shuffled, before.iloc[::-1])


def check_sql() -> None:
    query = task_2_sql()
    if not query.strip() or query.strip().startswith("-- TODO"):
        raise NotImplementedError("Задание 2: напиши SELECT внутри строки")
    customers = pd.DataFrame({"customer_id": [1, 2, 3, 4],
                              "name": ["Ада", "Борис", "Вера", "Глеб"]})
    # Отдельный набор с двумя заказами одного клиента и нулевой покупкой другого.
    # Это позволяет проверить агрегацию и различие 'нет заказов' / 'сумма 0'.
    clean_orders = pd.DataFrame({"order_id": [201, 202, 203, 204],
                                 "customer_id": [1, 1, 2, 3],
                                 "amount": [100., 40., 0., 300.]})
    with sqlite3.connect(":memory:") as connection:
        customers.to_sql("customers", connection, index=False)
        clean_orders.to_sql("clean_orders", connection, index=False)
        cursor = connection.execute(query)
        assert [c[0] for c in cursor.description] == [
            "customer_id", "name", "orders_count", "total_amount"
        ], "Проверь имена и порядок столбцов"
        assert cursor.fetchall() == [
            (1, "Ада", 2, 140.), (2, "Борис", 1, 0.),
            (3, "Вера", 1, 300.), (4, "Глеб", 0, None),
        ], "Проверь подсчёт заказов, сохранение всех клиентов, NULL и сортировку"


def check_numpy() -> None:
    for seed, n in [(42, 5), (17, 2)]:
        x, means = task_3_numpy(seed, n)
        assert isinstance(x, np.ndarray) and x.shape == (n, 3)
        assert x.dtype == np.float64 and np.isfinite(x).all()
        assert isinstance(means, np.ndarray) and means.shape == (3,)
        reference = np.random.default_rng(seed).normal(loc=0., scale=1., size=(n, 3))
        np.testing.assert_array_equal(x, reference)
        expected_means = [sum(x[:, i]) / n for i in range(3)]
        np.testing.assert_allclose(means, expected_means)
        again_x, again_means = task_3_numpy(seed, n)
        np.testing.assert_array_equal(x, again_x)
        np.testing.assert_array_equal(means, again_means)


def main() -> None:
    print("Короткая контрольная: 3 задания. Пустые задания не блокируют другие.")
    passed = 0
    for name, check in [("1. pandas", check_pandas),
                        ("2. SQL", check_sql), ("3. NumPy", check_numpy)]:
        try:
            check()
        except NotImplementedError as error:
            print(f"{name}: ЕЩЁ НЕ ГОТОВО — {error}")
        except Exception as error:
            print(f"{name}: ОШИБКА — {type(error).__name__}: {error}")
        else:
            print(f"{name}: OK")
            passed += 1
    print(f"Пройдено: {passed}/3")
    if passed != 3:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
