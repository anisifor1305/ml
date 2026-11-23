"""Автопроверка SQL занятия 11; запросы находятся в exercises/sql/lesson_11/."""
import argparse
import json
from pathlib import Path

from lesson_10 import check

TASKS = Path(__file__).resolve().parent / "sql" / "lesson_11"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", type=int, choices=range(1, 9))
    parser.add_argument("--backend", choices=["local", "docker"], default="local")
    args = parser.parse_args()
    expected = json.loads((TASKS / "expected.json").read_text())
    numbers = [f"{args.task:02d}"] if args.task is not None else expected
    for number in numbers:
        try:
            check(number, args.backend, expected[number], tasks=TASKS)
        except (RuntimeError, ValueError, AssertionError) as error:
            parser.exit(1, f"Задание {number}: {error}\n")
    print("Выбранные проверки пройдены.")


if __name__ == "__main__":
    main()
