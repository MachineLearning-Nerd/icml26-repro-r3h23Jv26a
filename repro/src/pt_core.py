"""Clean-room implementation of the released Table-1 synthetic PT protocol.

This module mirrors the numerical protocol in
``upstream/ordinary_regression_task/simulation_subgaussian.py`` at the pinned
source revision.  It is intentionally small and separately testable; the full
runner also executes the unmodified author script and requires an exact summary
match before recording results.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

import numpy as np
from sklearn.linear_model import LinearRegression


N = 2_000
TEST_RATIO = 0.2
BIAS = 20.0
ALPHAS = (0.05, 0.10, 0.15, 0.20)
PS = (0.96, 0.97, 0.98, 0.99, 1.0)
SEEDS = tuple(range(5))


def adjusted_alpha(alpha: float, p: float) -> float:
    """The PT calibration level from the released source."""
    return 1.0 - (1.0 - alpha) / p


def is_valid_pt_parameter(alpha: float, p: float) -> bool:
    """Return whether the adjusted level is a probability in [0, 1]."""
    return 0.0 <= adjusted_alpha(alpha, p) <= 1.0


def conformal_level(n_calibration: int, alpha: float) -> float:
    """Finite-sample quantile level used verbatim by the author script."""
    return math.ceil((n_calibration + 1) * (1.0 - alpha)) / n_calibration


def conformal_radius(residuals: np.ndarray, alpha: float) -> float:
    """Author-script percentile calculation for an absolute-residual radius."""
    level = conformal_level(len(residuals), alpha)
    return float(np.percentile(np.sort(residuals), level * 100.0))


@dataclass(frozen=True)
class SyntheticData:
    x_train: np.ndarray
    y_train: np.ndarray
    x_test: np.ndarray
    y_test: np.ndarray
    idx_train: np.ndarray
    idx_calibration: np.ndarray


def make_source_data(seed: int) -> SyntheticData:
    """Recreate one source seed using NumPy's legacy global-RNG semantics."""
    rng = np.random.RandomState(seed)
    x1 = rng.normal(0.0, 1.0, (N, 1))
    x2 = rng.normal(0.0, 1.0, (N, 1))
    eps_pos = rng.normal(BIAS, 1.0, (N // 2, 1))
    eps_neg = rng.normal(-BIAS, 1.0, (N // 2, 1))
    eps = np.vstack((eps_pos, eps_neg))
    rng.shuffle(eps)
    rng.shuffle(x1)
    rng.shuffle(x2)
    y = x1 + x2 + eps

    n_train = int(N * (1.0 - TEST_RATIO))
    x_train = np.column_stack((x1[:n_train], x2[:n_train]))
    y_train = y[:n_train]
    x_test = np.column_stack((x1[n_train:], x2[n_train:]))
    y_test = y[n_train:]
    indices = rng.permutation(n_train)
    n_half = n_train // 2
    return SyntheticData(
        x_train=x_train,
        y_train=y_train,
        x_test=x_test,
        y_test=y_test,
        idx_train=indices[:n_half],
        idx_calibration=indices[n_half : 2 * n_half],
    )


def fit_source_model(data: SyntheticData) -> tuple[np.ndarray, np.ndarray]:
    """Fit the source linear model and return calibration/test residuals."""
    model = LinearRegression(fit_intercept=True)
    model.fit(data.x_train[data.idx_train], data.y_train[data.idx_train])
    calibration_prediction = model.predict(data.x_train[data.idx_calibration])
    test_prediction = model.predict(data.x_test)
    calibration_residuals = np.abs(
        data.y_train[data.idx_calibration] - calibration_prediction
    ).reshape(-1)
    test_residuals = np.abs(data.y_test - test_prediction).reshape(-1)
    return calibration_residuals, test_residuals


def source_condition(
    calibration_residuals: np.ndarray,
    test_residuals: np.ndarray,
    alpha: float,
    p: float,
    python_rng: random.Random,
) -> dict[str, float | int]:
    """Run one VCP/PT-VCP condition with the author's per-test randomization."""
    base_radius = conformal_radius(calibration_residuals, alpha)
    pt_radius = conformal_radius(calibration_residuals, adjusted_alpha(alpha, p))
    flags = np.fromiter(
        (python_rng.random() < p for _ in range(len(test_residuals))),
        dtype=bool,
        count=len(test_residuals),
    )
    pt_radii = np.where(flags, pt_radius, 0.0)
    base_coverage = float(np.mean(test_residuals < base_radius))
    pt_coverage = float(np.mean(test_residuals < pt_radii))
    return {
        "base_radius": base_radius,
        "base_length": 2.0 * base_radius,
        "base_coverage": base_coverage,
        "pt_radius": pt_radius,
        "pt_length": float(np.mean(2.0 * pt_radii)),
        "pt_coverage": pt_coverage,
        "pt_non_singleton": int(np.sum(flags)),
        "pt_singleton": int(np.sum(~flags)),
        "expected_pt_length": float(p * 2.0 * pt_radius),
    }


def source_seed_rows(seed: int) -> list[dict[str, float | int]]:
    """Run all 20 author Table-1 conditions for one seed, in source order."""
    data = make_source_data(seed)
    calibration_residuals, test_residuals = fit_source_model(data)
    python_rng = random.Random(seed)
    rows: list[dict[str, float | int]] = []
    for alpha in ALPHAS:
        for p in PS:
            record: dict[str, float | int] = {"seed": seed, "alpha": alpha, "p": p}
            record.update(
                source_condition(
                    calibration_residuals, test_residuals, alpha, p, python_rng
                )
            )
            rows.append(record)
    return rows


def interval_stability(
    radius: float,
    p: float,
    n_test_points: int,
    repeats: int,
    seed: int,
) -> float:
    """Reimplement the source Table-3 per-point stability estimator.

    The author metric is the mean, across test inputs, of the standard
    deviation of repeated interval lengths divided by sqrt(repeats).  The
    random seed is deliberately independent of the Table-1 draw sequence.
    """
    if p == 1.0:
        return 0.0
    rng = np.random.default_rng(seed)
    lengths = np.where(rng.random((n_test_points, repeats)) < p, 2.0 * radius, 0.0)
    return float(np.mean(np.std(lengths, axis=1) / math.sqrt(repeats)))


def source_layout(rows: list[dict[str, float | int]]) -> np.ndarray:
    """Produce the 32-by-5 numeric body written by the author script."""
    body: list[list[float]] = []
    for key in ("base_coverage", "base_length", "pt_coverage", "pt_length"):
        values = np.empty((len(SEEDS), len(ALPHAS), len(PS)), dtype=float)
        for row in rows:
            seed_index = SEEDS.index(int(row["seed"]))
            alpha_index = ALPHAS.index(float(row["alpha"]))
            p_index = PS.index(float(row["p"]))
            values[seed_index, alpha_index, p_index] = float(row[key])
        body.extend(np.mean(values, axis=0).tolist())
        body.extend(np.std(values, axis=0).tolist())
    return np.asarray(body, dtype=float)
