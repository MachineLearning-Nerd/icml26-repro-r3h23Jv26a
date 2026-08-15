"""Fail-closed verification of the committed ICML 2026 audit snapshot."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    claims = read_json("outputs/claims_synthetic.json")
    require(claims["all_pass"] is True, "synthetic producer did not pass")
    require(claims["claim_1"]["pass"] is True, "C1 failed")
    require(claims["claim_1"]["nontrivial_alpha_p_conditions"] == 16, "C1 grid changed")
    require(claims["claim_1"]["max_aggregate_coverage_error"] <= 0.03, "C1 coverage bound changed")
    require(claims["claim_2"]["pass"] is True, "C2 producer checks failed")
    require(claims["claim_2"]["table1_reproduced_at_bias"] == 10, "C2 bias audit changed")
    require(claims["claim_2"]["cleanroom_vs_reference_csv_max_abs_diff"] < 1e-9, "C2 historical match failed")
    require(claims["claim_2"]["committed_bias20_vs_reference_max_abs_diff"] > 1.0, "C2 drift disappeared")
    require(claims["claim_4"]["pass"] is True, "C4 failed")
    require(claims["claim_4"]["unstable_pt_rows"] == 80, "C4 stochastic row count changed")

    full = read_json("outputs/full_synthetic_summary.json")
    require(full["protocol"]["conditions"] == 100, "synthetic protocol row count changed")
    require(len(full["rows"]) == 100, "synthetic evidence rows changed")
    require(full["source_equivalence"]["cleanroom_vs_unmodified_current_max_abs_difference"] == 0.0, "source equivalence failed")
    require(full["source_equivalence"]["unmodified_current_vs_checked_in_historical_max_abs_difference"] > 1.0, "source drift is missing")

    independent = read_json("outputs/independent_verification.json")
    require(independent["source_equivalence_pass"] is True, "independent source check failed")
    require(independent["claim_1"]["pass"] is True, "independent C1 failed")
    require(independent["claim_2"]["pass"] is True, "independent C4 path failed")
    require(independent["claim_3"]["pass"] is True, "independent stability check failed")
    require(independent["claim_3"]["false_positive"] == 0, "stability false positive appeared")
    require(independent["claim_3"]["false_negative"] == 0, "stability false negative appeared")

    real = read_json("outputs/claim3_real_world.json")
    require(real["pass"] is True, "real-world producer did not pass")
    require(real["n_datasets"] == 7, "real-world dataset count changed")
    require(real["n_paper_datasets"] == 3, "paper dataset count changed")
    require(real["n_pt_shorter"] == 7, "real-world shorter count changed")
    require(real["paper_datasets_shorter"] == 3, "paper dataset shorter count changed")
    require(real["protocol"]["n_seeds"] == 5, "real-world seed count changed")
    require(real["protocol"]["max_epochs"] == 200, "real-world epoch cap changed")

    trained = read_json("outputs/claim5_localized_cp.json")
    require(trained["pass"] is True, "trained-localizer producer did not pass")
    localizer = trained["realistic_trained_localizer"]
    require(localizer["all_is_positive"] is True, "trained-localizer IS check failed")
    require(localizer["is_vcp"] == 0.0, "VCP negative control changed")
    require(abs(localizer["mean_localized_coverage"] - 0.90625) < 1e-12, "localizer coverage changed")

    equivalence = read_json("outputs/localized_pt_equivalence.json")
    require(equivalence["verdict"] == "supports", "localized equivalence verdict changed")
    require(equivalence["summary"]["passed_conditions"] == 15, "localized condition count changed")
    require(equivalence["summary"]["equivalence_mismatches"] == 0, "localized mismatch appeared")
    require(equivalence["deterministic_p1_control"]["passed"] is True, "localized p=1 control failed")

    audit = read_json("outputs/localized_pt_equivalence_audit.json")
    require(audit["passed"] is True, "independent localized audit failed")

    manifest = read_json("evidence/claim_summary.json")
    expected_statuses = {
        "C1": "VERIFIED_SCOPED",
        "C2": "PARTIAL_SOURCE_ARTIFACT_AUDIT",
        "C3": "PARTIAL_EXTERNAL_DATA_AUDIT",
        "C4": "VERIFIED_SCOPED",
        "C5_constructive": "VERIFIED_SCOPED",
        "C5_trained_localizer": "SIMULATION_CHECK_SCOPED",
        "full_paper_experiments": "NOT_REPRODUCED",
    }
    for claim, status in expected_statuses.items():
        require(manifest["claims"][claim]["status"] == status, f"scope status changed: {claim}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require("icml26-conformal-prediction-coverage-length" in readme, "final repository name missing")
    require("evidence/synthetic-claims-1-2-4" in readme, "clean synthetic branch missing")
    require("PARTIAL_SOURCE_ARTIFACT_AUDIT" in readme, "Table-1 limitation missing")
    logbook = read_json("logbook.json")
    for page in logbook["root"]["children"]:
        require((ROOT / page["file"]).is_file(), f"logbook page is missing: {page['file']}")
    runner = (ROOT / "repro/run_full_source_synthetic.py").read_text(encoding="utf-8")
    require("TemporaryDirectory" in runner, "source runner is not isolated")
    require("reference" in runner, "committed source path missing")
    require('ROOT / "upstream"' not in runner, "stale source path remains")
    require(not any(path.is_dir() for path in ROOT.rglob(".trackio")), "tracked/generated Trackio directory remains")
    require(not any(path.is_file() for path in (ROOT / "outputs").rglob("*.log")), "generated output log remains")

    print("PASS: scoped claim evidence, source equivalence, branch naming, and cleanup invariants")


if __name__ == "__main__":
    main()
