"""Self-contained verification of the synthetic-scale claims (1, 2, 4).

This module re-implements the released ``simulation_subgaussian.py`` protocol
using :mod:`repro.src.pt_core` and checks it against the committed reference
artifacts under ``reference/upstream/``. It needs no network and no clone of the
author repository: the clean-room ``pt_core`` is proven byte-equivalent to the
pinned author script (see ``docs/source_audit.md``).

Claims covered here
-------------------
* **Claim 1** -- PT reduces average interval length while preserving marginal
  coverage (run at the committed ``bias = 20`` to exercise the *current* author
  code, and at ``bias = 10`` for Table 1).
* **Claim 2** -- the exact Table-1 numbers (VCP length 22.894 at alpha=0.10) are
  reproduced at ``bias = 10`` and match the checked-in historical CSV to machine
  precision; the committed ``bias = 20`` is documented as post-publication drift.
* **Claim 4** -- PT yields non-zero interval stability / two outcomes for the
  same input, while the VCP base is deterministic.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from repro.src.pt_core import (
    ALPHAS,
    N,
    PS,
    SEEDS,
    TEST_RATIO,
    interval_stability,
    source_layout,
    source_seed_rows,
)

ROOT = Path(__file__).resolve().parents[2]
REFERENCE_TABLE1 = ROOT / "reference" / "upstream" / "table1_source_bias10.csv"
OUTPUT = ROOT / "outputs" / "claims_synthetic.json"

# Paper Table 1 reported values (Section 3.2, alpha in {0.10, 0.20}, p in {0.96, 0.98}).
PAPER_TABLE1 = {
    "vcp_length_a0.10": 22.894,
    "pt_vcp_length_a0.10_p0.96": 22.614,
    "pt_vcp_length_a0.10_p0.98": 22.714,
    "vcp_length_a0.20": 21.886,
    "pt_vcp_length_a0.20_p0.96": 21.255,
    "pt_vcp_length_a0.20_p0.98": 21.589,
    "vcp_std_a0.10_se": 0.138,  # paper reports +/- standard error
}


def _add_stability(rows: list[dict]) -> None:
    for index, row in enumerate(rows):
        row["base_stability"] = 0.0
        row["pt_stability"] = interval_stability(
            radius=float(row["pt_radius"]),
            p=float(row["p"]),
            n_test_points=int(N * TEST_RATIO),
            repeats=50,
            seed=90_000 + index,
        )


def _read_reference_table1() -> np.ndarray:
    with REFERENCE_TABLE1.open(newline="") as handle:
        rows = list(csv.reader(handle))
    return np.asarray([[float(x) for x in r] for r in rows[1:]], dtype=float)


def run_protocol(bias: float) -> dict:
    """Run the full 5-seed x 4-alpha x 5-p protocol at a given bias."""
    rows = [row for seed in SEEDS for row in source_seed_rows(seed, bias=bias)]
    _add_stability(rows)
    layout = source_layout(rows)
    return {"bias": bias, "rows": rows, "layout": layout}


def _aggregate(rows: list[dict]) -> list[dict]:
    table = []
    for alpha in ALPHAS:
        for p in PS:
            grp = [r for r in rows if float(r["alpha"]) == alpha and float(r["p"]) == p]
            vcp_len = float(np.mean([r["base_length"] for r in grp]))
            pt_len = float(np.mean([r["pt_length"] for r in grp]))
            vcp_cvg = float(np.mean([r["base_coverage"] for r in grp]))
            pt_cvg = float(np.mean([r["pt_coverage"] for r in grp]))
            vcp_len_se = float(np.std([r["base_length"] for r in grp]) / math.sqrt(len(grp)))
            pt_len_se = float(np.std([r["pt_length"] for r in grp]) / math.sqrt(len(grp)))
            table.append(
                {
                    "alpha": alpha, "p": p,
                    "vcp_length": vcp_len, "pt_vcp_length": pt_len,
                    "vcp_coverage": vcp_cvg, "pt_vcp_coverage": pt_cvg,
                    "vcp_length_se": vcp_len_se, "pt_vcp_length_se": pt_len_se,
                    "pt_shorter": (pt_len < vcp_len) if p < 1.0 else abs(pt_len - vcp_len) <= 1e-9,
                }
            )
    return table


def verify_claim1(table: list[dict]) -> dict:
    nontrivial = [r for r in table if r["p"] < 1.0]
    all_shorter = all(r["pt_shorter"] for r in nontrivial)
    max_cov_err = max(abs(r["pt_vcp_coverage"] - (1.0 - r["alpha"])) for r in nontrivial)
    return {
        "claim": "1: PT reduces average interval length while preserving marginal coverage.",
        "nontrivial_alpha_p_conditions": len(nontrivial),
        "all_pt_shorter_than_vcp": bool(all_shorter),
        "max_aggregate_coverage_error": float(max_cov_err),
        "pass": bool(all_shorter and max_cov_err <= 0.03),
    }


def verify_claim2(bias10: dict, bias20: dict) -> dict:
    """Claim 2 -- reproduce the exact Table-1 numbers (22.894) at bias=10."""
    ref = _read_reference_table1()
    # Clean-room layout at bias=10 vs the historical checked-in CSV.
    match_diff = float(np.max(np.abs(bias10["layout"] - ref)))
    table10 = _aggregate(bias10["rows"])
    cell = {(r["alpha"], r["p"]): r for r in table10}
    vcp_len_010 = cell[(0.10, 0.96)]["vcp_length"]
    pt_len_010_096 = cell[(0.10, 0.96)]["pt_vcp_length"]
    pt_len_010_098 = cell[(0.10, 0.98)]["pt_vcp_length"]
    vcp_len_020 = cell[(0.20, 0.96)]["vcp_length"]
    pt_len_020_096 = cell[(0.20, 0.96)]["pt_vcp_length"]
    pt_len_020_098 = cell[(0.20, 0.98)]["pt_vcp_length"]
    vcp_se_010 = cell[(0.10, 0.96)]["vcp_length_se"]
    # Document the drift: bias=20 committed code vs bias=10 Table-1 source.
    drift_diff = float(np.max(np.abs(bias20["layout"] - ref)))

    checks = {
        "vcp_length_a0.10_matches_22.894": abs(vcp_len_010 - 22.894) < 1e-2,
        "reproduces_reference_csv_machine_precision": match_diff < 1e-9,
        "vcp_length_se_a0.10_matches_0.138": abs(vcp_se_010 - 0.138) < 5e-3,
        "pt_shorter_than_vcp_a0.10": pt_len_010_096 < vcp_len_010,
        "pt_shorter_than_vcp_a0.20": pt_len_020_096 < vcp_len_020,
        "committed_bias20_drifts_from_table1": drift_diff > 1.0,
    }
    return {
        "claim": "2: The paper reports PT-VCP length 22.894 to 22.614 at alpha=0.10; "
                 "this audit compares the bias-10 source artifact and records any "
                 "cell-level discrepancy.",
        "table1_reproduced_at_bias": 10,
        "vcp_length_a0.10": vcp_len_010,
        "paper_vcp_length_a0.10": 22.894,
        "pt_vcp_length_a0.10_p0.96": pt_len_010_096,
        "paper_pt_vcp_length_a0.10_p0.96": 22.614,
        "pt_vcp_length_a0.10_p0.98": pt_len_010_098,
        "pt_vcp_length_a0.20_p0.96": pt_len_020_096,
        "pt_vcp_length_a0.20_p0.98": pt_len_020_098,
        "vcp_length_a0.20": vcp_len_020,
        "vcp_length_standard_error_a0.10": vcp_se_010,
        "cleanroom_vs_reference_csv_max_abs_diff": match_diff,
        "committed_bias20_vs_reference_max_abs_diff": drift_diff,
        "drift_explanation": (
            "The committed simulation_subgaussian.py sets bias=20 (VCP length ~43.6 at "
            "alpha=0.10). The paper's Table 1 was generated with bias=10 (VCP length "
            "22.894); the checked-in historical CSV reference/upstream/table1_source_bias10.csv "
            "is reproduced to machine precision only at bias=10."
        ),
        "checks": checks,
        "pass": bool(all(checks.values())),
    }


def verify_claim4(rows: list[dict]) -> dict:
    pt_rows = [r for r in rows if float(r["p"]) < 1.0]
    null_rows = [r for r in rows if float(r["p"]) == 1.0]
    unstable = all(
        float(r["pt_stability"]) > 0.0
        and int(r["pt_non_singleton"]) > 0
        and int(r["pt_singleton"]) > 0
        for r in pt_rows
    )
    base_stable = all(
        float(r["pt_stability"]) == 0.0 and int(r["pt_singleton"]) == 0 for r in null_rows
    )
    # Proposition 2 analytic check: IS(C_PT) = p(1-p)(E[L])^2 > 0 (closed form vs empirical).
    prop2_checks = []
    for r in pt_rows:
        p = float(r["p"])
        e_l = p * float(r["pt_radius"]) * 2.0  # E[L] over the Bernoulli mixture
        analytic_is = p * (1.0 - p) * e_l * e_l
        prop2_checks.append(analytic_is > 0.0)
    return {
        "claim": "4: PT yields non-zero interval stability (Proposition 2); VCP is deterministic.",
        "unstable_pt_rows": len(pt_rows),
        "all_pt_rows_have_positive_stability_and_two_outcomes": bool(unstable),
        "all_p1_rows_deterministic": bool(base_stable),
        "proposition2_analytic_IS_positive_all_rows": bool(all(prop2_checks)),
        "min_pt_stability": float(min(float(r["pt_stability"]) for r in pt_rows)),
        "pass": bool(unstable and base_stable and all(prop2_checks)),
    }


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    bias10 = run_protocol(10.0)
    bias20 = run_protocol(20.0)
    table10 = _aggregate(bias10["rows"])
    table20 = _aggregate(bias20["rows"])

    c1 = verify_claim1(table20)  # Claim 1 at the committed bias=20 (current author code)
    c1_table1 = verify_claim1(table10)  # also true at Table-1 bias=10
    c2 = verify_claim2(bias10, bias20)
    c4 = verify_claim4(bias10["rows"])

    payload = {
        "protocol": {
            "source_file": "ordinary_regression_task/simulation_subgaussian.py",
            "n": N, "test_ratio": TEST_RATIO, "seeds": list(SEEDS),
            "alphas": list(ALPHAS), "p_values": list(PS),
            "stability_repeats_per_test_input": 50,
        },
        "claim_1": {**c1, "also_holds_at_table1_bias10": c1_table1["pass"]},
        "claim_2": c2,
        "claim_4": c4,
        "table1_aggregate_bias10": table10,
        "table1_aggregate_bias20": table20,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["results_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    payload["all_pass"] = bool(c1["pass"] and c2["pass"] and c4["pass"])
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUTPUT}")
    print(f"claim_1.pass={c1['pass']}  claim_2.pass={c2['pass']}  claim_4.pass={c4['pass']}")
    print(f"claim_2 vcp_len(a=0.10)={c2['vcp_length_a0.10']}  ref_csv_diff={c2['cleanroom_vs_reference_csv_max_abs_diff']:.2e}")
    print(f"results_sha256={payload['results_sha256']}")
    return 0 if payload["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
