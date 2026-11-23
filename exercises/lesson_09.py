"""Занятие 09: визуализация и EDA. Реализуй только функции с TODO.

Запуск: .venv/bin/python exercises/lesson_09.py
Данные синтетические; одна строка — клиент за один фиксированный месяц.
Пропуски не заполнять нулём, строки и выбросы без обоснования не удалять.
Графики сохраняет main; в заданиях возвращай объекты Figure / PairGrid.
"""
from pathlib import Path
from typing import Tuple

import matplotlib

matplotlib.use("Agg")  # Сохранение в файлы без открытия окон.
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "lesson_09_customers.csv"
OUTPUT = ROOT / "outputs" / "lesson_09"
NUMERIC = ["age", "visits", "spend_rub", "satisfaction", "refunds"]


def task_1_audit(df: pd.DataFrame) -> pd.DataFrame:
    """Верни таблицу аудита числовых столбцов.

    Индекс: NUMERIC в указанном порядке.
    Столбцы: missing_count, missing_share, mean, median, q25, q75.
    missing_share — доля от ВСЕХ строк, не процент.
    Статистики считать по непустым значениям. Исходную таблицу не менять.
    """
    # TODO: Используй isna, sum/mean, mean/median, quantile.
    table = pd.DataFrame()
    table['missing_count']=df[NUMERIC].isna().sum()
    table['missing_share']=df[NUMERIC].isna().mean()
    table['mean']=df[NUMERIC].mean()
    table['median']=df[NUMERIC].median()
    table['q25']=df[NUMERIC].quantile(0.25)
    table['q75']=df[NUMERIC].quantile(0.75)
    return table


def task_2_distributions(df: pd.DataFrame) -> Figure:
    """Верни Figure с двумя гистограммами spend_rub, bins=30.

    Слева — линейная ось X, справа — логарифмическая ось X.
    Для логарифмической гистограммы используй histplot(log_scale=True).
    Общая компоновка 1x2. Подпиши оси, единицы и заголовки.
    Один и тот же полный набор наблюдений; выбросы не отрезать.
    """
    # TODO: subplots + histplot; объясни разницу между двумя представлениями.
    fig, axes = plt.subplots(
        figsize = (10,4),
        nrows = 1,
        ncols = 2,
        layout = "constrained",
    )
    axes[0].set_title("Распределение месячных трат")
    axes[0].set_xlabel("Траты, руб.")
    axes[0].set_ylabel("Количество клиентов")
    sns.histplot(
        data=df,
        x='spend_rub',
        bins= 30,
        stat ='count',
        ax=axes[0]
    )

    axes[1].set_title("Траты: логарифмическая шкала X")
    axes[1].set_xlabel("Траты, руб.")
    axes[1].set_ylabel("Количество клиентов")
    sns.histplot(
        data=df,
        x='spend_rub',
        bins= 30,
        stat ='count',
        log_scale=True,
        ax=axes[1]
    )
    return fig


def task_3_segments(df: pd.DataFrame) -> Tuple[pd.DataFrame, Figure]:
    """Верни сводку сегментов и Figure с boxplot трат по segment.

    Сводка: индекс segment; столбцы n, mean_spend, median_spend.
    n — число клиентов сегмента. Порядок сегментов на рисунке:
    basic, plus, premium. На оси Y — рубли, на оси X — сегмент.
    Объясни, почему точки за усами нельзя автоматически удалять.
    """
    # TODO: Именованная агрегация из занятия 08 + boxplot.
    # print(df)
    sv = df.groupby("segment").agg({'spend_rub': ['mean', 'sum'], 'segment':'count'})
    sv = df.groupby("segment").agg(n=('segment', 'count'), mean_spend=('spend_rub', 'mean'), median_spend=('spend_rub', 'median'))
    fig, ax = plt.subplots(
        figsize=(10, 4),
        layout = 'constrained'
    )
    ax.set_title("Месячные траты по сегментам")
    sns.boxplot(
        data = df,
        y = 'spend_rub',
        x = 'segment',
        ax = ax
    )
    ax.set_xlabel("Сегмент клиента")
    ax.set_ylabel("Траты за месяц, руб.")
    return sv, fig


def task_4_relationships(df: pd.DataFrame) -> Figure:
    """Верни Figure с двумя scatterplot (сетка 1x2).

    Слева: X=visits, Y=spend_rub; hue=segment, style=segment, alpha=0.5.
    Справа: X=refunds, Y=satisfaction; alpha=0.3.
    Не соединяй точки линиями. Пропуски не заменять нулём.
    Оси и единицы подписать. Объясни наложение точек и роль сегмента.
    """
    # TODO: subplots + scatterplot. Связь сама по себе не доказывает причинность.
    fig, axes = plt.subplots(
        figsize = (10,4),
        nrows =1,
        ncols=2,
        layout='constrained'
    )
    axes[0].set_title("Посещения и месячные траты")
    sns.scatterplot(data=df, ax=axes[0], alpha=0.5, hue='segment', style='segment', x='visits', y='spend_rub')
    axes[1].set_title("Возвраты и удовлетворённость")
    sns.scatterplot(data=df, ax=axes[1], alpha=0.3, hue='segment', style='segment', x='refunds', y='satisfaction')
    axes[0].set_xlabel("Посещения за месяц, шт.")
    axes[0].set_ylabel("Траты за месяц, руб.")
    axes[1].set_xlabel("Возвраты за месяц, шт.")
    axes[1].set_ylabel("Удовлетворённость, баллы (1–10)")
    for ax in axes:
        ax.get_legend().set_title("Сегмент")
    return fig


def task_5_correlations(df: pd.DataFrame) -> Tuple[pd.DataFrame, Figure, sns.PairGrid]:
    """Верни (corr, heatmap_figure, pair_grid).

    corr: Pearson-корреляция только NUMERIC, порядок строк/столбцов как NUMERIC.
    heatmap: vmin=-1, vmax=1, center=0, annot=True, fmt='.2f', cmap='vlag'.
    pairplot: только visits, spend_rub, satisfaction; hue=segment;
    diag_kind='hist'; plot_kws={'alpha': 0.3}.
    Pairplot создаёт собственную Figure; не передавай ему ax.
    """
    # TODO: corr + heatmap + pairplot. customer_id не включать в корреляции.
    corrable = df[NUMERIC]
    cor = corrable.corr(method="pearson")
    fig, ax = plt.subplots(
    figsize = (10,4),
    layout='constrained'
    )
    ax.set_title("Корреляции Пирсона")
    sns.heatmap(data=cor, ax=ax, vmin=-1, vmax=1, center=0, annot=True, fmt=".2f", cmap='vlag')
    grid = sns.pairplot(data=df, vars=['visits', 'spend_rub', 'satisfaction'], hue='segment',  diag_kind='hist', plot_kws={'alpha': 0.3})
    labels = {
        "age": "Возраст, лет",
        "visits": "Посещения, шт./мес.",
        "spend_rub": "Траты, руб./мес.",
        "satisfaction": "Оценка (1–10)",
        "refunds": "Возвраты, шт./мес.",
    }
    ax.set_xticklabels([labels[name] for name in cor.columns], rotation=25, ha="right")
    ax.set_yticklabels([labels[name] for name in cor.index], rotation=0)
    ax.collections[0].colorbar.set_label("Коэффициент корреляции")
    grid.figure.suptitle("Посещения, траты и удовлетворённость", y=1.02)
    for pair_ax in grid.axes.flat:
        pair_ax.set_xlabel(labels.get(pair_ax.get_xlabel(), pair_ax.get_xlabel()))
        pair_ax.set_ylabel(labels.get(pair_ax.get_ylabel(), pair_ax.get_ylabel()))
    grid.legend.set_title("Сегмент")
    grid.figure.tight_layout()
    return cor, fig, grid


def check_figure(fig: Figure, axes_count: int) -> None:
    """Минимальная проверка структуры; содержимое проверяем также визуально."""
    assert isinstance(fig, Figure), "Нужно вернуть Figure"
    assert len(fig.axes) == axes_count, "Неверное количество областей построения"
    for ax in fig.axes:
        assert ax.has_data(), "Обнаружен пустой график"
        assert ax.get_xlabel() and ax.get_ylabel(), "Подпиши обе оси"
        assert ax.get_title(), "Добавь заголовок"


def save_figure(fig: Figure, name: str) -> None:
    """PNG для просмотра, PDF для экспорта; Figure после сохранения закрывается."""
    fig.savefig(OUTPUT / (name + ".png"), dpi=160, bbox_inches="tight")
    fig.savefig(OUTPUT / (name + ".pdf"), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    original = df.copy(deep=True)
    assert len(df) == 600 and df["customer_id"].is_unique
    assert (df["spend_rub"] > 0).all(), "Для log нужны положительные траты"

    audit = task_1_audit(df)
    assert isinstance(audit, pd.DataFrame)
    assert list(audit.index) == NUMERIC
    expected = ["missing_count", "missing_share", "mean", "median", "q25", "q75"]
    assert list(audit.columns) == expected
    for col in NUMERIC:
        values = df[col].dropna().to_numpy()
        missing = len(df) - len(values)
        reference = [missing, missing / len(df), np.mean(values), np.median(values),
                     np.quantile(values, .25), np.quantile(values, .75)]
        np.testing.assert_allclose(audit.loc[col].to_numpy(dtype=float), reference)
    audit.to_csv(OUTPUT / "audit.csv")
    print("1/5: аудит — OK")

    fig = task_2_distributions(df)
    check_figure(fig, 2)
    assert fig.axes[0].get_xscale() == "linear"
    assert fig.axes[1].get_xscale() == "log"
    save_figure(fig, "02_distributions")
    print("2/5: структура распределений — OK")

    summary, fig = task_3_segments(df)
    assert list(summary.columns) == ["n", "mean_spend", "median_spend"]
    assert summary.index.is_unique
    assert set(summary.index) == set(df["segment"])
    for segment in summary.index:
        values = df.loc[df["segment"] == segment, "spend_rub"].to_numpy()
        np.testing.assert_allclose(
            summary.loc[segment].to_numpy(dtype=float),
            [len(values), np.mean(values), np.median(values)],
        )
    summary.to_csv(OUTPUT / "segments.csv")
    check_figure(fig, 1)
    save_figure(fig, "03_segments")
    print("3/5: сводка и структура boxplot — OK")

    fig = task_4_relationships(df)
    check_figure(fig, 2)
    save_figure(fig, "04_relationships")
    print("4/5: структура scatterplot — OK")

    corr, fig, grid = task_5_correlations(df)
    assert list(corr.columns) == NUMERIC and list(corr.index) == NUMERIC
    for a in NUMERIC:
        for b in NUMERIC:
            pair = df[[a, b]].dropna().to_numpy()
            expected_r = np.corrcoef(pair[:, 0], pair[:, 1])[0, 1]
            assert np.isclose(corr.loc[a, b], expected_r)
    assert isinstance(fig, Figure) and fig.axes[0].has_data()
    assert isinstance(grid, sns.PairGrid) and grid.axes.shape == (3, 3)
    save_figure(fig, "05_correlations")
    save_figure(grid.figure, "05_pairs")
    pd.testing.assert_frame_equal(df, original)
    print("5/5: корреляции и структура pairplot — OK")
    print("Далее: проверь картинки и заполни docs/ОТЧЕТ_09_EDA.md.")
    print("Зачёт — после защиты пяти выводов; автопроверка не проверяет смысл графиков.")


if __name__ == "__main__":
    main()
