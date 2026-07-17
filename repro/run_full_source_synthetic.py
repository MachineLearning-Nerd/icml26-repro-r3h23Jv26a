#!/usr/bin/env python3
"""Run the full released synthetic PT protocol and record source equivalence."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from repro.src.pt_core import ALPHAS, N, PS, SEEDS, TEST_RATIO, interval_stability, source_layout, source_seed_rows


AUTHOR_ORDINARY = ROOT / "upstream" / "ordinary_regression_task"
AUTHOR_CHECKED_IN = AUTHOR_ORDINARY / "simulation_ablation" / "ablation_study_simulation_p.csv"
AUTHOR_GENERATED = AUTHOR_ORDINARY / "ablation_study_simulation_p.csv"


def read_author_csv(path: Path) -> np.ndarray:
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        next(reader)
        return np.asarray([[float(x) for x in row] for row in reader], dtype=float)


def aggregate(rows: list[dict[str, float | int]]) -> list[dict[str, float | int]]:
    grouped: dict[tuple[float, float], list[dict[str, float | int]]] = defaultdict(list)
    for row in rows:
        grouped[(float(row["alpha"]), float(row["p"]))].append(row)
    summary: list[dict[str, float | int]] = []
    for alpha in ALPHAS:
        for p in PS:
            group = grouped[(alpha, p)]
            summary.append(
                {
                    "alpha": alpha,
                    "p": p,
                    "base_length_mean": float(np.mean([r["base_length"] for r in group])),
                    "pt_length_mean": float(np.mean([r["pt_length"] for r in group])),
                    "base_coverage_mean": float(np.mean([r["base_coverage"] for r in group])),
                    "pt_coverage_mean": float(np.mean([r["pt_coverage"] for r in group])),
                    "pt_expected_length_mean": float(np.mean([r["expected_pt_length"] for r in group])),
                }
            )
    return summary


def add_stability(rows: list[dict[str, float | int]]) -> None:
    """Add full-source Table-3-style 50-repeat stability for every Table-1 row."""
    for index, row in enumerate(rows):
        row["base_stability"] = 0.0
        row["pt_stability"] = interval_stability(
            radius=float(row["pt_radius"]),
            p=float(row["p"]),
            n_test_points=int(N * TEST_RATIO),
            repeats=50,
            seed=90_000 + index,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "full_synthetic_summary.json")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Execute the unmodified pinned author program before comparing the clean-room
    # reconstruction.  It is a complete 5-seed / 4-alpha / 5-p run.
    subprocess.run([sys.executable, "simulation_subgaussian.py"], cwd=AUTHOR_ORDINARY, check=True)
    author_generated = read_author_csv(AUTHOR_GENERATED)
    author_checked_in = read_author_csv(AUTHOR_CHECKED_IN)

    rows = [row for seed in SEEDS for row in source_seed_rows(seed)]
    add_stability(rows)
    cleanroom = source_layout(rows)
    generated_difference = float(np.max(np.abs(cleanroom - author_generated)))
    checked_in_difference = float(np.max(np.abs(author_generated - author_checked_in)))
    if generated_difference > 1e-12:
        raise RuntimeError(
            f"Clean-room protocol disagrees with current author execution: {generated_difference}"
        )

    payload = {
        "paper": {
            "openreview_id": "r3h23Jv26a",
            "arxiv": "2601.21455",
            "author_repo": "benben-cd/PT-Conformal-Prediction",
            "author_commit": "09655d6c58be2a9b24aafb739c37397e0488e933",
        },
        "protocol": {
            "source_file": "ordinary_regression_task/simulation_subgaussian.py",
            "n": N,
            "test_ratio": TEST_RATIO,
            "seeds": list(SEEDS),
            "alphas": list(ALPHAS),
            "p_values": list(PS),
            "conditions": len(rows),
            "stability_repeats_per_test_input": 50,
        },
        "source_equivalence": {
            "cleanroom_vs_unmodified_current_max_abs_difference": generated_difference,
            "unmodified_current_vs_checked_in_historical_max_abs_difference": checked_in_difference,
            "note": "The second value records source-artifact drift; only the current pinned executable is treated as the reproducible protocol.",
        },
        "rows": rows,
        "aggregate_by_alpha_p": aggregate(rows),
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"wrote {args.output}")
    print(f"conditions={len(rows)} cleanroom_max_diff={generated_difference:.3g}")
    print(f"checked_in_historical_max_diff={checked_in_difference:.6g}")


if __name__ == "__main__":
    main()
