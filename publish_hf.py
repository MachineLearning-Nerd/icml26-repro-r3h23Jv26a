#!/usr/bin/env python3
"""Publish the reproduction to the existing HF Space DineshAI/r3h23Jv26a.

Text-only API path. Builds an allowlist + SHA-256 manifest, scans for secrets,
verifies the old (judged) file set is a subset of the new one, then uploads.
"""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from huggingface_hub import HfApi, list_repo_files

REPO = Path(__file__).resolve().parent
SPACE = "DineshAI/r3h23Jv26a"
JUDGED_SHA = "66c41210d499d72ae1a8dbbb626be01d082740bd"

# Exact allowlist (repo-relative paths). Old Space files NOT in this list are preserved
# (we never delete), so the judged set stays a subset.
ALLOW = [
    "README.md", "logbook.json", "pyproject.toml", "uv.lock", "STATUS.md",
    "pages/index.md",
    "pages/claim-1/page.md", "pages/claim-2/page.md", "pages/claim-3/page.md",
    "pages/claim-4/page.md", "pages/claim-5/page.md", "pages/methods/page.md",
    "repro/__init__.py", "repro/suite.py", "repro/make_figures.py",
    "repro/src/__init__.py", "repro/src/pt_core.py", "repro/src/claims_synthetic.py",
    "repro/src/claim3_real_world.py", "repro/src/claim5_localized_cp.py",
    "repro/src/real_datasets.py", "repro/src/verify_localized_pt_equivalence.py",
    "repro/src/audit_localized_pt_equivalence.py",
    "repro/run_full_source_synthetic.py", "repro/tests/test_pt_core.py",
    "outputs/claims_synthetic.json", "outputs/claim3_real_world.json",
    "outputs/claim5_localized_cp.json", "outputs/suite_report.json",
    "outputs/full_synthetic_summary.json", "outputs/independent_verification.json",
    "reports/conformal-pt/report.md", "reports/conformal-pt/pt_conformal.py",
    "reports/conformal-pt/images/table1_match.png",
    "reports/conformal-pt/images/real_world.png",
    "reports/conformal-pt/images/stability.png",
    "reference/upstream/table1_source_bias10.csv",
    "reference/upstream/table3_interval_stability.csv",
    "reference/upstream/simulation_subgaussian.py",
    "docs/source_audit.md",
]

SECRET_PAT = re.compile(r"(sk-[A-Za-z0-9]{16,}|hf_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    api = HfApi()
    # 1. allowlist present + secret scan
    manifest = {}
    for rel in ALLOW:
        p = REPO / rel
        assert p.exists(), f"missing allowlist file: {rel}"
        txt = p.read_text(errors="ignore") if p.suffix in {".py", ".md", ".json", ".toml", ".txt", ".csv", ".lock"} else ""
        m = SECRET_PAT.search(txt)
        assert not m, f"SECRET in {rel}: {m.group(0)[:8]}…"
        manifest[rel] = sha256(p)
    (REPO / "outputs" / "upload_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True))
    print(f"allowlist: {len(manifest)} files, no secrets")

    # 2. old/judged subset check
    old = set(list_repo_files(SPACE, repo_type="space", revision=JUDGED_SHA))
    old_real = {f for f in old if not f.startswith(".cache/")}
    # we only ADD/OVERWRITE; nothing deleted -> old stays subset. Report non-cache old files.
    print(f"judged non-cache files: {len(old_real)}; all preserved (upload is additive)")

    # 3. upload each allowlisted file (text API path)
    for rel in ALLOW:
        api.upload_file(path_or_fileobj=str(REPO / rel), path_in_repo=rel,
                        repo_id=SPACE, repo_type="space")
    print("uploaded all allowlisted files")

    # 4. upload manifest itself
    api.upload_file(path_or_fileobj=str(REPO / "outputs" / "upload_manifest.json"),
                    path_in_repo="outputs/upload_manifest.json",
                    repo_id=SPACE, repo_type="space")

    new = set(list_repo_files(SPACE, repo_type="space"))
    new_real = {f for f in new if not f.startswith(".cache/")}
    subset_ok = old_real.issubset(new_real)
    print(f"old⊆new after upload: {subset_ok} (old={len(old_real)} new={len(new_real)})")
    info = api.space_info(SPACE)
    print(f"Space sha: {info.sha}")
    return 0 if subset_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
