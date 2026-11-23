"""Готовые проверки контракта. Это не решение функций задания."""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
from omegaconf import OmegaConf

from exercises import lesson_13 as lesson


@pytest.fixture
def config():
    return OmegaConf.create({"seed": 42, "n_a": 3, "n_b": 2, "dimensions": 2})


def test_config_and_zero_override(tmp_path):
    path = tmp_path / "settings.yaml"
    path.write_text("seed: 42\nn_a: 3\nn_b: 2\ndimensions: 2\n")
    before = path.read_bytes()
    original = lesson.load_config(path)
    changed = lesson.load_config(path, seed_override=0)
    assert original.seed == 42 and changed.seed == 0
    assert changed.n_a == 3 and changed.n_b == 2 and changed.dimensions == 2
    assert path.read_bytes() == before


def test_inputs_shapes_and_reproducibility(config):
    a, b = lesson.generate_inputs(config)
    again_a, again_b = lesson.generate_inputs(config)
    assert a.shape == (3, 2) and b.shape == (2, 2)
    assert a.dtype == np.float64 and b.dtype == np.float64
    assert np.isfinite(a).all() and np.isfinite(b).all()
    np.testing.assert_array_equal(a, again_a)
    np.testing.assert_array_equal(b, again_b)
    assert a.tobytes() == again_a.tobytes() and b.tobytes() == again_b.tobytes()
    # Фиксированный внешний ориентир для последовательности default_rng(42).
    np.testing.assert_allclose(a[0], [0.30471707975443135, -1.0399841062404955])
    np.testing.assert_allclose(b[0], [0.12784040316728537, -0.3162425923435822])


def test_different_seeds_change_inputs(config):
    a, b = lesson.generate_inputs(config)
    other = OmegaConf.create(OmegaConf.to_container(config))
    other.seed = 17
    different_a, different_b = lesson.generate_inputs(other)
    assert not np.array_equal(a, different_a)
    assert not np.array_equal(b, different_b)


def test_experiment_matches_distances_and_preserves_config(config):
    before = OmegaConf.to_container(config)
    a, b = lesson.generate_inputs(config)
    distances, metrics = lesson.run_experiment(config)
    # Независимый численный ориентир: норма для каждой пары точек.
    expected = np.array([[np.linalg.norm(x - y) for y in b] for x in a])
    np.testing.assert_allclose(distances, expected, atol=1e-12)
    assert distances.shape == (3, 2)
    assert np.isfinite(distances).all() and (distances >= 0).all()
    assert set(metrics) == {"seed", "n_a", "n_b", "dimensions", "mean_distance"}
    assert all(metrics[key] == before[key] for key in before)
    assert isinstance(metrics["mean_distance"], float)
    assert metrics["mean_distance"] == pytest.approx(expected.mean())
    assert OmegaConf.to_container(config) == before


def test_cli_arguments():
    default = lesson.parse_args([])
    assert default.config == lesson.DEFAULT_CONFIG
    assert default.output == lesson.DEFAULT_OUTPUT
    assert default.seed is None
    args = lesson.parse_args(["--config", "custom.yaml", "--output", "result", "--seed", "0"])
    assert args.config == Path("custom.yaml") and args.output == Path("result")
    assert args.seed == 0


def test_cli_help():
    proc = subprocess.run(
        [sys.executable, str(Path(lesson.__file__)), "--help"],
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert proc.returncode == 0, proc.stderr
    assert all(flag in proc.stdout for flag in ["--config", "--output", "--seed"])


def test_three_real_launches(tmp_path):
    results = []
    for name, seed in [("first", "42"), ("second", "42"), ("other", "17")]:
        output = tmp_path / name
        proc = subprocess.run(
            [
                sys.executable,
                str(Path(lesson.__file__)),
                "--config",
                str(lesson.DEFAULT_CONFIG),
                "--output",
                str(output),
                "--seed",
                seed,
            ],
            capture_output=True,
            text=True,
            timeout=20,
        )
        assert proc.returncode == 0, proc.stderr
        distances = np.load(output / "distances.npy")
        metrics = json.loads((output / "metrics.json").read_text())
        saved_config = OmegaConf.load(output / "config.yaml")
        log = (output / "experiment.log").read_text()
        assert log.count("INFO:") >= 3, "Нужны сообщения начала, итога и сохранения"
        assert "INFO:" in proc.stderr, "Логи должны быть и в консоли"
        assert str(seed) in log
        assert saved_config.seed == int(seed) == metrics["seed"]
        assert distances.shape == (saved_config.n_a, saved_config.n_b)
        assert metrics["mean_distance"] == pytest.approx(float(distances.mean()))
        results.append((distances, metrics))
    assert results[0][0].tobytes() == results[1][0].tobytes()
    assert results[0][1] == results[1][1]
    assert not np.array_equal(results[0][0], results[2][0])
    assert results[0][1]["mean_distance"] != results[2][1]["mean_distance"]
