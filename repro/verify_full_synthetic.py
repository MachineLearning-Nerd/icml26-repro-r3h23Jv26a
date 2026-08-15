#!/usr/bin/env python3
"""Independent, artifact-only verification of the PT synthetic reproduction."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
AUTHOR_TABLE3 = ROOT / "reference" / "upstream" / "table3_interval_stability.csv"


def grouped(rows: list[dict]) -> dict[tuple[float, float], list[dict]]:
    result: dict[tuple[float, float], list[dict]] = defaultdict(list)
    for row in rows:
        result[(float(row["alpha"]), float(row["p"]))].append(row)
    return result


def author_table3_check() -> dict[str, float | int | bool]:
    with AUTHOR_TABLE3.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    vcp = np.asarray([float(row["stability_VCP"]) for row in rows])
    pt = np.asarray([float(row["stability_PT_VCP"]) for row in rows])
    return {
        "rows": len(rows),
        "all_vcp_zero": bool(np.all(vcp == 0.0)),
        "all_pt_positive": bool(np.all(pt > 0.0)),
        "min_pt_stability": float(np.min(pt)),
        "scope": "Source-supplied Table-3 result artifact check only; external data/checkpoints are not rerun.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=ROOT / "outputs" / "full_synthetic_summary.json")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "independent_verification.json")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text())
    rows = payload["rows"]
    groups = grouped(rows)

    c1_rows = []
    maximum_coverage_error = 0.0
    for (alpha, p), values in sorted(groups.items()):
        base_length = float(np.mean([v["base_length"] for v in values]))
        pt_length = float(np.mean([v["pt_length"] for v in values]))
        pt_coverage = float(np.mean([v["pt_coverage"] for v in values]))
        error = abs(pt_coverage - (1.0 - alpha))
        maximum_coverage_error = max(maximum_coverage_error, error)
        c1_rows.append(
            {
                "alpha": alpha,
                "p": p,
                "base_length": base_length,
                "pt_length": pt_length,
                "pt_shorter": pt_length < base_length if p < 1.0 else abs(pt_length - base_length) <= 1e-12,
                "pt_coverage": pt_coverage,
                "target_coverage": 1.0 - alpha,
                "absolute_coverage_error": error,
            }
        )
    nontrivial = [row for row in c1_rows if row["p"] < 1.0]
    c1_pass = all(row["pt_shorter"] for row in nontrivial) and maximum_coverage_error <= 0.03

    pt_rows = [row for row in rows if float(row["p"]) < 1.0]
    null_rows = [row for row in rows if float(row["p"]) == 1.0]
    c2_pass = all(
        float(row["pt_stability"]) > 0.0
        and int(row["pt_non_singleton"]) > 0
        and int(row["pt_singleton"]) > 0
        and float(row["base_stability"]) == 0.0
        for row in pt_rows
    )

    threshold = 1e-12
    true_positive = sum(float(row["pt_stability"]) > threshold for row in pt_rows)
    true_negative = sum(float(row["pt_stability"]) <= threshold for row in null_rows)
    c3_pass = true_positive == len(pt_rows) and true_negative == len(null_rows)
    p_one_control = all(
        abs(float(row["pt_length"]) - float(row["base_length"])) <= 1e-12
        and abs(float(row["pt_coverage"]) - float(row["base_coverage"])) <= 1e-12
        and float(row["pt_stability"]) == 0.0
        for row in null_rows
    )

    result = {
        "source_equivalence_pass": payload["source_equivalence"]["cleanroom_vs_unmodified_current_max_abs_difference"] <= 1e-12,
        "claim_1": {
            "pass": c1_pass,
            "nontrivial_alpha_p_conditions": len(nontrivial),
            "maximum_aggregate_coverage_error": maximum_coverage_error,
            "conditions": c1_rows,
        },
        "claim_2": {
            "pass": c2_pass,
            "unstable_pt_rows": len(pt_rows),
            "deterministic_base_rows": len(rows),
            "same_input_two_outcomes_verified": c2_pass,
        },
        "claim_3": {
            "pass": c3_pass,
            "stability_threshold": threshold,
            "true_positive": true_positive,
            "false_negative": len(pt_rows) - true_positive,
            "true_negative": true_negative,
            "false_positive": len(null_rows) - true_negative,
            "p_equals_one_negative_control_pass": p_one_control,
            "author_supplied_table3_artifact": author_table3_check(),
        },
    }
    if not all((result["source_equivalence_pass"], c1_pass, c2_pass, c3_pass, p_one_control)):
        raise SystemExit(json.dumps(result, indent=2, sort_keys=True))
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
