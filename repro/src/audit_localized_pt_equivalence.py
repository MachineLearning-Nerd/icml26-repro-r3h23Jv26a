#!/usr/bin/env python3
"""Independent audit of localized-CP/PT equivalence verifier output."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


DEFAULT_INPUT = Path(__file__).resolve().parents[2] / "outputs" / "localized_pt_equivalence.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[2] / "outputs" / "localized_pt_equivalence_audit.json"


def main() -> int:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT
    payload = json.loads(input_path.read_text())

    stored_hash = payload.pop("results_sha256_without_hash")
    verdict = payload.pop("verdict")
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    recomputed_hash = hashlib.sha256(canonical.encode()).hexdigest()
    conditions = payload["conditions"]
    checks = {
        "source_is_ar5iv": payload["source_url"] == "https://ar5iv.labs.arxiv.org/html/2601.21455",
        "judged_parent_recorded": payload["judged_space_sha"] == "09b41e11615d25da127c7953458f988225150732",
        "stdlib_only": payload["stdlib_only"] is True,
        "fifteen_conditions": len(conditions) == 15,
        "all_conditions_pass": all(item["passed"] for item in conditions),
        "zero_equivalence_mismatches": all(item["equivalence_mismatches"] == 0 for item in conditions),
        "all_stochastic_is_positive": all(item["empirical_interval_stability"] > 0 for item in conditions),
        "all_analytic_matches": all(item["relative_stability_error"] <= 0.05 for item in conditions),
        "all_mean_widths_shrink": all(item["average_width"] < item["informative_width"] for item in conditions),
        "p1_control_zero": payload["deterministic_p1_control"]["interval_stability"] == 0.0,
        "payload_hash_matches": stored_hash == recomputed_hash,
        "verifier_verdict_supports": verdict == "supports",
    }
    audit = {
        "input": str(input_path),
        "checks": checks,
        "passed": all(checks.values()),
        "verified_results_sha256_without_hash": recomputed_hash,
    }
    canonical_audit = json.dumps(audit, sort_keys=True, separators=(",", ":"))
    audit["audit_sha256_without_hash"] = hashlib.sha256(canonical_audit.encode()).hexdigest()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print(json.dumps(audit, sort_keys=True))
    return 0 if audit["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
