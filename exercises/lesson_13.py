"""Занятие 13. Сначала читай docs/ПРАКТИКА_13_ИНЖЕНЕРНАЯ_ГИГИЕНА.md.

Реализуй четыре функции с TODO. Сохранение файлов и настройка логов готовы.
Модель не обучаем: организуем воспроизводимый NumPy-эксперимент из занятия 06.
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import numpy as np
from omegaconf import DictConfig, OmegaConf

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs" / "lesson_13.yaml"
DEFAULT_OUTPUT = ROOT / "exercises" / "outputs" / "lesson_13" / "run_01"
LOGGER = logging.getLogger("lesson13")


def load_config(path: Path, seed_override: int = None) -> DictConfig:
    """Задание 1: прочитай YAML через OmegaConf.load.

    Если seed_override не None, замени seed в прочитанном конфиге.
    Ноль — допустимый сид: проверка просто `if seed_override` не подходит.
    Файл на диске не меняй. Верни объект конфига.
    """
    conf = OmegaConf.load(path)
    if seed_override is not None:
        conf.seed = seed_override
    return conf


def generate_inputs(config: DictConfig) -> tuple:
    """Задание 2: верни пару массивов A, B.

    Один НОВЫЙ default_rng(config.seed) на вызов функции.
    Сначала A формы (n_a, dimensions), затем B формы (n_b, dimensions).
    Оба из normal(loc=0, scale=1), обычный float64; вход не менять.
    Не используй глобальный np.random.seed и не переустанавливай сид между A и B.
    """
    rng = np.random.default_rng(config.seed)
    A = rng.normal(loc=0, scale=1, size=(config.n_a, config.dimensions))
    B = rng.normal(loc=0, scale=1, size=(config.n_b, config.dimensions))

    return A,B


def run_experiment(config: DictConfig) -> tuple:
    LOGGER.info((config.seed, config.n_a, config.n_b))
    inputs = generate_inputs(config)
    distances = distances_from_lesson_06(inputs[0], inputs[1])
    assert distances.shape == (config.n_a, config.n_b) and np.isfinite(distances).all() and np.all(distances>=0)
    mean_distance = distances.mean()
    LOGGER.info(float(distances.mean()))
    """Задание 3: верни (distances, metrics), входной конфиг не менять.

    Через LOGGER.info сообщи seed и размеры в начале; среднее расстояние в конце.
    Вызови generate_inputs, затем distances_from_lesson_06 (она уже готова).
    Проверь assert: shape == (n_a, n_b), все числа конечные и >= 0.
    metrics — словарь ровно с ключами seed, n_a, n_b, dimensions, mean_distance.
    Первые четыре значения бери из конфига, последнее — float(distances.mean()).
    Файлы здесь не сохраняй: этим занимается готовая функция save_results.
    """
    return ((distances, {"seed":config.seed,
                         "n_a":config.n_a,
                        "n_b":config.n_b,
                        "dimensions":config.dimensions,
                          "mean_distance":float(mean_distance)}))


def parse_args(argv=None) -> argparse.Namespace:
    """Задание 4: argparse; три аргумента, без запуска эксперимента.

    --config: type=Path, default=DEFAULT_CONFIG.
    --output: type=Path, default=DEFAULT_OUTPUT.
    --seed: type=int, default=None (нет переопределения).
    Верни parser.parse_args(argv). argv нужен для проверки без настоящей консоли.
    --help должен обрабатываться самим argparse.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=None)

    return parser.parse_args(argv)


# Ниже готовая инфраструктура. Реализовывать её не нужно.
def distances_from_lesson_06(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Твой векторный подход из занятия 06, без запуска старого бенчмарка."""
    return np.sqrt(np.sum((a[:, None, :] - b[None, :, :]) ** 2, axis=-1))


def configure_logging(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for handler in LOGGER.handlers[:]:
        LOGGER.removeHandler(handler)
        handler.close()
    LOGGER.setLevel(logging.INFO)
    LOGGER.propagate = False
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handlers = [logging.StreamHandler(), logging.FileHandler(output / "experiment.log", mode="w")]
    for handler in handlers:
        handler.setFormatter(formatter)
        LOGGER.addHandler(handler)


def save_results(output: Path, config: DictConfig, distances: np.ndarray, metrics: dict) -> None:
    np.save(output / "distances.npy", distances)
    (output / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    OmegaConf.save(config, output / "config.yaml")


def main(argv=None) -> None:
    args = parse_args(argv)
    config = load_config(args.config, args.seed)
    configure_logging(args.output)
    distances, metrics = run_experiment(config)
    save_results(args.output, config, distances, metrics)
    LOGGER.info("Результаты сохранены: %s", args.output)


def run_task(task: int) -> None:
    """Учебный запуск отдельного задания; не зависит от задания 4."""
    if task == 4:
        main([])
        return
    config = load_config(DEFAULT_CONFIG)
    if task == 1:
        print(config)
    elif task == 2:
        a, b = generate_inputs(config)
        print("A:", a, "\nФорма A:", a.shape)
        print("B:", b, "\nФорма B:", b.shape)
    elif task == 3:
        configure_logging(DEFAULT_OUTPUT)
        distances, metrics = run_experiment(config)
        print("Форма матрицы расстояний:", distances.shape)
        print("Метрики:", metrics)


def dispatch(argv=None) -> None:
    """Без аргументов запускает задание 3; --task выбирает другое задание.

    Обычные аргументы эксперимента передаются в main без изменений.
    Этот служебный разбор готов; parse_args в задании 4 реализуешь сам.
    """
    argv = sys.argv[1:] if argv is None else argv
    if argv and "--task" not in argv and not any(x.startswith("--task=") for x in argv):
        main(argv)
        return
    parser = argparse.ArgumentParser(description="Запуск отдельного задания занятия 13")
    parser.add_argument("--task", type=int, choices=[1, 2, 3, 4], default=3)
    args = parser.parse_args(argv)
    run_task(args.task)


if __name__ == "__main__":
    dispatch()
