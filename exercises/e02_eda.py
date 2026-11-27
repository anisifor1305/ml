"""E02 — этап 7: качество данных, графики и устный разбор утечек.

Обычный запуск файла проверяет задания независимо, без аргументов.
Исходные данные те же: 300 поездок exercises/data/e02/trips.csv.
Письменный отчёт не требуется. Решения функций пишешь сам.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Рисунки сохраняются в файлы, отдельные окна не нужны.
import matplotlib.pyplot as plt  # noqa: E402, F401
import numpy as np  # noqa: E402, F401
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402, F401

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "exercises" / "data" / "e02" / "trips.csv"
OUTPUT = ROOT / "exercises" / "outputs" / "e02" / "eda"


def task_1_profile(trips: pd.DataFrame) -> pd.DataFrame:
    """Для КАЖДОГО исходного столбца: missing_count, missing_share, unique_count.

    Индекс — имена столбцов в исходном порядке; unique_count исключает пропуски.
    Верни DataFrame, вход не меняй. Знакомое задание из занятия 12.
    """
    missing_count = trips.isna().sum()
    missing_share = missing_count / (trips.shape[0])
    unique_count = trips.nunique()
    return pd.DataFrame(
        {
            "missing_count": missing_count,
            "missing_share": missing_share,
            "unique_count": unique_count,
        }
    )


def task_2_distribution(trips: pd.DataFrame, output: Path) -> None:
    """Один рисунок с двумя графиками: гистограмма и boxplot столбца total.

    Создай 1 строку и 2 колонки графиков, figsize=(12, 4).
    Слева гистограмма: X — total, Y — число поездок, bins=20.
    Справа boxplot: X — total; каждая точка исходника — одна поездка.
    Данные не фильтровать, шкала обычная линейная, выбросы не скрывать.
    Подпиши оси/заголовки. Сохрани output / 'total_distribution.png'.
    Закрой фигуру через plt.close(fig). Ничего возвращать не нужно.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(data=trips, x="total", bins=20, ax=axes[0])
    sns.boxplot(data=trips, x="total", ax=axes[1])
    axes[0].set_title("Распределение стоимости поездок")
    axes[0].set_xlabel("Стоимость, $")
    axes[0].set_ylabel("Количество поездок")
    axes[1].set_title("Разброс стоимости поездок")
    axes[1].set_xlabel("Стоимость, $")
    axes[1].set_ylabel("")
    fig.tight_layout()
    plt.savefig(output / "total_distribution.png", bbox_inches="tight")
    plt.close(fig)


def task_3_correlations(trips: pd.DataFrame, output: Path) -> pd.DataFrame:
    """Возьми distance, total, tip в таком порядке, посчитай корреляции Пирсона.

    Получится DataFrame 3x3: сохрани его изображение через sns.heatmap.
    Требования: annot=True, vmin=-1, vmax=1, center=0, cmap='coolwarm'.
    Подпиши заголовок, сохрани output / 'correlations.png', закрой фигуру.
    Верни САМУ матрицу корреляций (DataFrame), а не рисунок.
    Не включай trip_id и zone_id: номера не считаем числовыми характеристиками.
    """
    trips = trips[["distance", "total", "tip"]]
    trips = trips.corr(method="pearson")
    fig, ax = plt.subplots()
    sns.heatmap(data=trips, annot=True, vmin=-1, vmax=1, center=0, cmap="coolwarm", ax=ax)
    ax.set_title("Корреляции расстояния, стоимости и чаевых")
    fig.savefig(output / "correlations.png", bbox_inches="tight")
    plt.close(fig)
    return trips


def quality_summary(trips):
    """Готовая диагностика, чтобы не повторять большой набор упражнений."""
    print("Строк:", len(trips))
    print("Повторных trip_id:", int(trips.trip_id.duplicated().sum()))
    print("Повторных записей без учёта ID:", int(trips.drop(columns="trip_id").duplicated().sum()))
    print("Окончание раньше начала:", int((trips.dropoff_at < trips.pickup_at).sum()))
    print("Нулевое расстояние:", int((trips.distance == 0).sum()))
    print("Нулевое число пассажиров:", int((trips.passengers == 0).sum()))
    print("Отрицательный total:", int((trips.total < 0).sum()))
    print("Максимальный total:", trips.total.max())
    print("Средний total:", trips.total.mean())
    print("Медианный total:", trips.total.median())


def main():
    trips = pd.read_csv(DATA, parse_dates=["pickup_at", "dropoff_at"])
    OUTPUT.mkdir(parents=True, exist_ok=True)
    quality_summary(trips)
    passed = 0
    for number, function in [
        (1, task_1_profile),
        (2, task_2_distribution),
        (3, task_3_correlations),
    ]:
        source = trips.copy(deep=True)
        try:
            if number == 1:
                result = function(source)
                expected = pd.DataFrame(
                    {
                        "missing_count": trips.isna().sum(),
                        "missing_share": trips.isna().mean(),
                        "unique_count": trips.nunique(),
                    }
                )
                pd.testing.assert_frame_equal(result, expected, check_dtype=False)
                result.to_csv(OUTPUT / "profile.csv")
                print(result.to_string())
            elif number == 2:
                function(source, OUTPUT)
                assert (OUTPUT / "total_distribution.png").is_file(), "Не сохранён рисунок"
            else:
                result = function(source, OUTPUT)
                expected = trips[["distance", "total", "tip"]].corr(method="pearson")
                pd.testing.assert_frame_equal(result, expected)
                assert (OUTPUT / "correlations.png").is_file(), "Не сохранён рисунок"
                result.to_csv(OUTPUT / "correlations.csv")
                print(result.to_string())
            pd.testing.assert_frame_equal(source, trips)
            passed += 1
            print(f"{number}: OK (графики дополнительно смотрим глазами)")
        except NotImplementedError as error:
            print(f"{number}: ещё не готово — {error}")
        except Exception as error:
            print(f"{number}: ошибка — {type(error).__name__}: {error}")
        finally:
            plt.close("all")
    print(f"Код: {passed}/3. Для сдачи этапа ещё нужны просмотр рисунков и устный разбор.")
    if passed != 3:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
