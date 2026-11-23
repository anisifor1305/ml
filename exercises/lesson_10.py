"""Проверка SQL занятия 10. Запросы пиши в exercises/sql/lesson_10/NN.sql."""
import argparse
import csv
import io
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.lesson10_db import execute  # noqa: E402

TASKS = ROOT / "exercises/sql/lesson_10"


def read_query(number, tasks=TASKS):
    path = tasks / (number + ".sql")
    if not path.exists():
        raise ValueError("Номер задания должен быть от 1 до 15")
    sql = re.sub(r"--[^\n]*", "", path.read_text()).strip().rstrip(";").strip()
    if not sql:
        raise NotImplementedError("Заполни TODO в " + str(path))
    return sql


def equivalent(actual, expected):
    if expected is None:
        return actual == "\\N"
    if isinstance(expected, (int, float)):
        try:
            return Decimal(actual) == Decimal(str(expected))
        except InvalidOperation:
            return False
    return actual == expected


def check(number, backend, expected, tasks=TASKS):
    sql = read_query(number, tasks)
    # Проверяемая SQL-команда выполняется в транзакции только для чтения.
    wrapper = (
        "BEGIN READ ONLY; SET LOCAL search_path TO lesson10; "
        "SET LOCAL statement_timeout = '10s'; "
        "COPY (" + sql + ") TO STDOUT WITH (FORMAT CSV, HEADER TRUE, NULL '\\N'); "
        "ROLLBACK;"
    )
    result = list(csv.reader(io.StringIO(execute(backend, wrapper))))
    assert result and result[0] == expected["columns"], "Неверные названия/порядок столбцов"
    rows = result[1:]
    assert len(rows) == len(expected["rows"]), (
        "Ожидалось {} строк, получено {}".format(len(expected["rows"]), len(rows))
    )
    for i, (actual, reference) in enumerate(zip(rows, expected["rows"]), 1):
        assert len(actual) == len(reference)
        assert all(equivalent(a, b) for a, b in zip(actual, reference)), (
            "Строка {}: получено {}, ожидалось {}. Проверь также ORDER BY.".format(
                i, actual, reference
            )
        )
    print("Задание {}: OK, строк: {}".format(number, len(rows)))
    for row in result:
        print(" | ".join(row))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", type=int, help="Проверить одно задание: 1–15")
    parser.add_argument("--explain", type=int, help="Показать план заполненного задания")
    parser.add_argument("--backend", choices=["local", "docker"], default="local")
    args = parser.parse_args()
    try:
        if args.explain is not None:
            sql = read_query("{:02d}".format(args.explain))
            print(execute(args.backend, "BEGIN READ ONLY; SET LOCAL search_path TO lesson10; "
                          "SET LOCAL statement_timeout = '10s'; EXPLAIN " + sql + "; ROLLBACK;"))
            return
        expected = json.loads((TASKS / "expected.json").read_text())
        numbers = ["{:02d}".format(args.task)] if args.task is not None else list(expected)
        for number in numbers:
            if number not in expected:
                raise ValueError("Номер задания должен быть от 1 до 15")
            check(number, args.backend, expected[number])
        print("Выбранные проверки пройдены. Объяснения JOIN и EXPLAIN — в отчёте.")
    except (RuntimeError, ValueError, AssertionError, NotImplementedError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
