"""E02, этап 6. Запросы пиши в exercises/sql/e02/01.sql ... 08.sql.

Обычный запуск проверяет все восемь независимо. Без Docker и настройки БД.
Условия и таблицы: docs/E02_ЭТАП_06_SQL.md.
"""

import json
import math
import re
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "exercises" / "data" / "e02"
TASKS = ROOT / "exercises" / "sql" / "e02"
OUTPUT = ROOT / "exercises" / "outputs" / "e02"


def connect():
    connection = sqlite3.connect(":memory:")
    for table in ["trips", "zones"]:
        pd.read_csv(DATA / f"{table}.csv").to_sql(table, connection, index=False)
    connection.execute("PRAGMA query_only=ON")
    return connection


def main():
    expected = json.loads((DATA / "checks.json").read_text())
    OUTPUT.mkdir(parents=True, exist_ok=True)
    passed = 0
    connection = connect()
    try:
        for number, reference in expected.items():
            query = (TASKS / f"{number}.sql").read_text()
            query = re.sub(r"--[^\n]*", "", query).strip()
            if not query:
                print(f"{number}: ещё не написано")
                continue
            try:
                cursor = connection.execute(query)
                columns = [c[0] for c in cursor.description]
                assert columns == reference["columns"], f"Столбцы: {columns}"
                actual = cursor.fetchall()
                assert len(actual) == len(reference["rows"]), f"Число строк: {len(actual)}"
                for i, (row, correct) in enumerate(zip(actual, reference["rows"]), 1):
                    for col, value, target in zip(columns, row, correct):
                        if isinstance(target, (int, float)):
                            ok = isinstance(value, (int, float)) and math.isclose(
                                value, target, rel_tol=1e-9, abs_tol=1e-8
                            )
                        else:
                            ok = value == target
                        assert ok, f"Строка {i}, {col}: {value!r}, ожидалось {target!r}"
                pd.DataFrame(actual, columns=columns).to_csv(
                    OUTPUT / f"sql_{number}.csv", index=False
                )
                print(f"{number}: OK, строк: {len(actual)}")
                passed += 1
            except (sqlite3.Error, AssertionError, TypeError) as error:
                print(f"{number}: ошибка — {error}")
    finally:
        connection.close()
    print(f"Пройдено {passed}/8. Решения дополнительно проверяем по коду.")
    if passed != 8:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
