"""
Занятие 04: Итераторы, генераторы, профилирование памяти.
Практические задания.
"""

from typing import Iterable, Iterator, List, Any
import tracemalloc
from contextlib import contextmanager


# =====================================================================
# Задание 1. Свой итератор через класс: StreamRange
# =====================================================================
# Напиши класс StreamRange(start, stop, step=1).
# Он должен вести себя как range(), но быть явным итератором:
# - в __init__ сохранять параметры и текущее положение;
# - в __iter__ возвращать self;
# - в __next__ возвращать следующее число или бросать StopIteration, если вышли за границы stop.


class StreamRange:
    def __init__(self, start: int, stop: int, step: int = 1):
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        # TODO: верни итератор
        return self

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        self.current += self.step
        return self.current - self.step


# =====================================================================
# Задание 2. Генератор батчей через yield: batch_stream
# =====================================================================
# Напиши функцию-генератор batch_stream(data: Iterable, batch_size: int).
# Она принимает любой итерируемый объект и отдает данные батчами (списками длины batch_size).
# Если в конце данных осталось меньше, чем batch_size — последний батч отдается неполным.
# Никаких промежуточных списков на все данные! Только yield.


def batch_stream(data: Iterable[Any], batch_size: int) -> Iterator[List[Any]]:
    batch = []
    for i in data:
        batch.append(i)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch != []:
        yield batch


# =====================================================================
# Задание 3. Контекстный менеджер замера памяти: track_memory
# =====================================================================
# Напиши контекстный менеджер через @contextmanager из contextlib.
# Внутри блока with:
# - запускаем замер памяти через tracemalloc.start();
# - передаем управление в блок with через yield;
# - после выхода замеряем пик через tracemalloc.get_traced_memory();
# - останавливаем tracemalloc.stop();
# - печатаем пиковый расход RAM в МБ.


@contextmanager
def track_memory(name: str):
    try:
        tracemalloc.start()
        yield
    finally:
        current, peak = tracemalloc.get_traced_memory()
        print(f"Расход такеой: {peak / 1024 / 1024:.2f}" + " МБ для " + name)
        tracemalloc.stop()


# =====================================================================
# Задание 4. Битва за память: List Comprehension vs Generator
# =====================================================================
def compare_memory():
    n_elements = 1_000_000

    print("\n--- Сравнение памяти на 1 000 000 чисел ---")

    with track_memory("list"):
        variant1 = [i**2 for i in range(1000000)]

    with track_memory("generator"):
        variant2 = (i**2 for i in range(1000000))
    # Способ А: создаем список всех чисел и считаем сумму
    # с контекстным менеджером track_memory("Список")
    # ...

    # Способ Б: создаем генератор и передаем в sum()
    # с контекстным менеджером track_memory("Генератор")
    # ...


if __name__ == "__main__":
    print("Занятие 04: запуск тестов...")
    sr = StreamRange(1, 5)
    for x in sr:
        print(x)

    print("#######################")

    for batch in batch_stream(range(10), batch_size=4):
        print(batch)
    compare_memory()
