"""Cumulative reproduction suite -- the single entry point for the fixed run
command ``uv run python -m repro.suite``.

Every experiment node inherits this command unchanged; each node's *code*
determines which claim verifiers are registered below. The suite runs every
registered verifier, writes a combined report to ``outputs/suite_report.json``,
and exits non-zero if any verifier fails (so a failing claim is never silent).
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "outputs" / "suite_report.json"

# Each entry: (label, module-callable). Children append their own verifiers.
VERIFIERS: list[tuple[str, str]] = [
    ("claim_1_2_4_synthetic", "repro.src.claims_synthetic:main"),
    ("claim_5_localized_cp", "repro.src.claim5_localized_cp:main"),
]


def _git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "unknown"


def _run(entry: str) -> dict:
    module, _, func = entry.partition(":")
    code = subprocess.call([sys.executable, "-m", module])
    return {"entry": entry, "exit_code": code, "pass": code == 0}


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    start = time.time()
    results = [_run(entry) for _, entry in VERIFIERS]
    duration = time.time() - start
    report = {
        "run_command": "uv run python -m repro.suite",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "git_sha": _git_sha(),
        "verifiers": dict(zip([n for n, _ in VERIFIERS], results)),
        "duration_seconds": round(duration, 2),
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["results_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    report["all_pass"] = all(r["pass"] for r in results)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v["pass"] for k, v in report["verifiers"].items()}, indent=2))
    print(f"all_pass={report['all_pass']}  duration={duration:.1f}s  sha={report['results_sha256'][:12]}")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
