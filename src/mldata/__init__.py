"""mldata — библиотека потоковой обработки таблиц и базовых ML-операций."""

from mldata.config import ExperimentConfig
from mldata.dataset import TableDataset, stream_csv
from mldata.ops import (
    euclidean_distance_naive,
    euclidean_distance_vectorized,
    minmax_scale_naive,
    minmax_scale_vectorized,
    relu_naive,
    relu_vectorized,
    standardize_naive,
    standardize_vectorized,
    weighted_sum_naive,
    weighted_sum_vectorized,
)
from mldata.stats import describe

__version__ = "0.1.0"

__all__ = [
    "ExperimentConfig",
    "TableDataset",
    "stream_csv",
    "minmax_scale_naive",
    "minmax_scale_vectorized",
    "standardize_naive",
    "standardize_vectorized",
    "relu_naive",
    "relu_vectorized",
    "euclidean_distance_naive",
    "euclidean_distance_vectorized",
    "weighted_sum_naive",
    "weighted_sum_vectorized",
    "describe",
]
