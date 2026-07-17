import math
import random

import numpy as np

from repro.src.pt_core import (
    adjusted_alpha,
    conformal_level,
    interval_stability,
    is_valid_pt_parameter,
    make_source_data,
    source_condition,
    source_seed_rows,
)


def test_adjusted_alpha_preserves_the_target_marginal_coverage_identity():
    for alpha in (0.05, 0.1, 0.2):
        for p in (0.96, 0.99, 1.0):
            assert math.isclose(p * (1.0 - adjusted_alpha(alpha, p)), 1.0 - alpha)


def test_invalid_probability_is_rejected_by_the_parameter_audit():
    assert not is_valid_pt_parameter(0.05, 0.94)
    assert is_valid_pt_parameter(0.05, 0.96)


def test_source_data_has_the_full_released_shape_and_split():
    data = make_source_data(0)
    assert data.x_train.shape == (1600, 2)
    assert data.y_train.shape == (1600, 1)
    assert data.x_test.shape == (400, 2)
    assert len(data.idx_train) == len(data.idx_calibration) == 800


def test_p_equals_one_is_exactly_the_base_interval_for_source_condition():
    calibration = np.linspace(0.1, 0.5, 800)
    test = np.array([0.05, 0.15, 0.25, 0.35])
    record = source_condition(calibration, test, 0.1, 1.0, random.Random(11))
    assert math.isclose(record["pt_length"], record["base_length"], abs_tol=1e-12)
    assert record["pt_coverage"] == record["base_coverage"]
    assert record["pt_singleton"] == 0


def test_pt_same_input_has_two_lengths_and_the_source_metric_detects_it():
    # A p<1 transformation assigns a singleton or the same adjusted interval
    # to the identical point across repeat runs; VCP's length is constant.
    stability = interval_stability(radius=3.0, p=0.96, n_test_points=400, repeats=50, seed=8)
    assert stability > 0.0
    assert interval_stability(radius=3.0, p=1.0, n_test_points=400, repeats=50, seed=8) == 0.0


def test_one_source_seed_covers_every_alpha_p_condition_in_source_order():
    rows = source_seed_rows(0)
    assert len(rows) == 20
    assert rows[0]["alpha"] == 0.05 and rows[0]["p"] == 0.96
    assert rows[-1]["alpha"] == 0.2 and rows[-1]["p"] == 1.0
    assert all(
        math.isclose(row["pt_length"], row["base_length"], abs_tol=1e-12)
        for row in rows
        if row["p"] == 1.0
    )
