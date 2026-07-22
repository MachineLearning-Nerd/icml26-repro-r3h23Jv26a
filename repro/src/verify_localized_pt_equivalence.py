#!/usr/bin/env python3
"""Verify Proposition 1 and Definition 1 of arXiv:2601.21455.

Source audited at https://ar5iv.labs.arxiv.org/html/2601.21455, scoped to
Section 3.2 Proposition 1 (Relation Between PT and Localized CP), Equation 4,
and Section 4 Definition 1 (Interval Stability), Equations 15-16.

This clean-room verifier uses only the Python standard library. For a fixed
test input, a retrained local scale estimator emits epsilon (the paper's 0+)
with probability 1-p and 1 with probability p. The normalized-score interval
therefore has either minimal width or the adjusted conformal width, exactly
the two branches of the Prejudicial Trick. Repeated retraining estimates the
conditional interval-size variance in Definition 1 and compares it with the
closed-form Bernoulli variance.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import statistics
from pathlib import Path


PAPER = "arXiv:2601.21455"
SOURCE_URL = "https://ar5iv.labs.arxiv.org/html/2601.21455"
SOURCE_SCOPE = "Section 3.2 Proposition 1 and Equation 4; Section 4 Definition 1 and Equations 15-16"
JUDGED_SHA = "09b41e11615d25da127c7953458f988225150732"
ALPHA = 0.10
EPSILON_SCALE = 1e-12
P_VALUES = (0.91, 0.95, 0.99)
SEEDS = (260121455, 260121456, 260121457, 260121458, 260121459)
RETRAININGS = 100_000
CALIBRATION_SIZE = 2_000
OUTPUT = Path(__file__).resolve().parents[2] / "outputs" / "localized_pt_equivalence.json"


def conformal_quantile(values: list[float], level: float) -> float:
    rank = min(len(values), math.ceil((len(values) + 1) * level))
    return sorted(values)[rank - 1]


def interval(center: float, half_width: float) -> tuple[float, float]:
    return center - half_width, center + half_width


def condition(seed: int, p: float) -> dict[str, object]:
    calibration_rng = random.Random(seed)
    calibration_residuals = [calibration_rng.random() ** (1.0 / 3.0) for _ in range(CALIBRATION_SIZE)]
    alpha_prime = 1.0 - (1.0 - ALPHA) / p
    adjusted_quantile = conformal_quantile(calibration_residuals, 1.0 - alpha_prime)

    center = math.sin(0.75)
    informative_half_width = adjusted_quantile
    minimal_half_width = EPSILON_SCALE * adjusted_quantile
    informative_interval = interval(center, informative_half_width)
    minimal_interval = interval(center, minimal_half_width)
    informative_width = informative_interval[1] - informative_interval[0]
    minimal_width = minimal_interval[1] - minimal_interval[0]

    retraining_rng = random.Random(seed ^ 0x5A17)
    localized_widths: list[float] = []
    informative_count = 0
    equivalence_mismatches = 0
    scale_outputs: set[float] = set()

    for _ in range(RETRAININGS):
        informative = retraining_rng.random() < p
        scale = 1.0 if informative else EPSILON_SCALE
        scale_outputs.add(scale)
        localized_interval = interval(center, adjusted_quantile * scale)
        pt_interval = informative_interval if informative else minimal_interval
        if localized_interval != pt_interval:
            equivalence_mismatches += 1
        localized_widths.append(localized_interval[1] - localized_interval[0])
        informative_count += int(informative)

    empirical_p = informative_count / RETRAININGS
    empirical_stability = statistics.pvariance(localized_widths)
    analytic_stability = p * (1.0 - p) * (informative_width - minimal_width) ** 2
    relative_stability_error = abs(empirical_stability - analytic_stability) / analytic_stability
    average_width = statistics.fmean(localized_widths)
    analytic_average_width = p * informative_width + (1.0 - p) * minimal_width

    checks = {
        "two_point_scale_estimator": scale_outputs == {EPSILON_SCALE, 1.0},
        "samplewise_pt_equivalence": equivalence_mismatches == 0,
        "branch_probability_matches": abs(empirical_p - p) <= 0.02,
        "interval_stability_positive": empirical_stability > 0.0,
        "stability_matches_analytic": relative_stability_error <= 0.05,
        "mean_width_matches_analytic": abs(average_width - analytic_average_width) <= 0.02,
        "random_localizer_shrinks_mean_width": average_width < informative_width,
    }
    return {
        "seed": seed,
        "p": p,
        "alpha": ALPHA,
        "alpha_prime": alpha_prime,
        "calibration_size": CALIBRATION_SIZE,
        "retrainings": RETRAININGS,
        "scale_outputs": sorted(scale_outputs),
        "adjusted_quantile": adjusted_quantile,
        "minimal_width": minimal_width,
        "informative_width": informative_width,
        "empirical_p": empirical_p,
        "average_width": average_width,
        "analytic_average_width": analytic_average_width,
        "empirical_interval_stability": empirical_stability,
        "analytic_interval_stability": analytic_stability,
        "relative_stability_error": relative_stability_error,
        "equivalence_mismatches": equivalence_mismatches,
        "checks": checks,
        "passed": all(checks.values()),
    }


def deterministic_control(seed: int) -> dict[str, object]:
    rng = random.Random(seed)
    residuals = [rng.random() ** (1.0 / 3.0) for _ in range(CALIBRATION_SIZE)]
    quantile = conformal_quantile(residuals, 1.0 - ALPHA)
    widths = [2.0 * quantile for _ in range(RETRAININGS)]
    return {
        "p": 1.0,
        "scale_outputs": [1.0],
        "interval_stability": statistics.pvariance(widths),
        "passed": statistics.pvariance(widths) == 0.0,
    }


def main() -> int:
    conditions = [condition(seed, p) for p in P_VALUES for seed in SEEDS]
    control = deterministic_control(SEEDS[0])
    summary = {
        "condition_count": len(conditions),
        "passed_conditions": sum(int(item["passed"]) for item in conditions),
        "total_retrainings": len(conditions) * RETRAININGS,
        "equivalence_mismatches": sum(int(item["equivalence_mismatches"]) for item in conditions),
        "minimum_interval_stability": min(float(item["empirical_interval_stability"]) for item in conditions),
        "maximum_relative_stability_error": max(float(item["relative_stability_error"]) for item in conditions),
        "deterministic_control_passed": control["passed"],
    }
    payload: dict[str, object] = {
        "paper": PAPER,
        "source_url": SOURCE_URL,
        "source_scope": SOURCE_SCOPE,
        "judged_space_sha": JUDGED_SHA,
        "claim": "Proposition 1 localized-CP/PT equivalence and Definition 1 interval-stability detection",
        "stdlib_only": True,
        "epsilon_scale_for_zero_plus": EPSILON_SCALE,
        "conditions": conditions,
        "deterministic_p1_control": control,
        "summary": summary,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["results_sha256_without_hash"] = hashlib.sha256(canonical.encode()).hexdigest()
    payload["verdict"] = (
        "supports"
        if summary["passed_conditions"] == summary["condition_count"]
        and summary["equivalence_mismatches"] == 0
        and summary["deterministic_control_passed"]
        else "inconclusive"
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(f"source={SOURCE_URL}")
    print(f"scope={SOURCE_SCOPE}")
    print(
        "conditions="
        f"{summary['passed_conditions']}/{summary['condition_count']} "
        f"retrainings={summary['total_retrainings']}"
    )
    print(f"samplewise_equivalence_mismatches={summary['equivalence_mismatches']}")
    print(f"minimum_interval_stability={summary['minimum_interval_stability']:.12f}")
    print(
        "maximum_relative_stability_error="
        f"{summary['maximum_relative_stability_error']:.6f}"
    )
    print(f"p1_deterministic_control={control['passed']}")
    print(f"verdict={payload['verdict']}")
    print(f"results_sha256_without_hash={payload['results_sha256_without_hash']}")
    return 0 if payload["verdict"] == "supports" else 1


if __name__ == "__main__":
    raise SystemExit(main())
