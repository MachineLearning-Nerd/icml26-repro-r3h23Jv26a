# Methods & source audit

## Paper
*Questioning the Coverage-Length Metric in Conformal Prediction: When Shorter
Intervals Are Not Better*, arXiv:2601.21455, OpenReview `r3h23Jv26a`.
Primary HTML source: `https://ar5iv.labs.arxiv.org/html/2601.21455` (retrieved 2026-07-24).

## Author source
`benben-cd/PT-Conformal-Prediction` pinned to `09655d6c58be2a9b24aafb739c37397e0488e933`.
Committed reference scripts/CSVs mirrored under `reference/upstream/`.

## Fixed command & pinned environment
- **Command (identical on every node):** `uv run python -m repro.suite`
- **Env:** `uv` + `pyproject.toml` / `uv.lock`; Python 3.12; numpy 2.5.1,
  scikit-learn 1.9.0, scipy 1.18, pandas 3.0.5, matplotlib 3.x, ucimlrepo 0.0.7.
- **CPU only** — no GPU used at any point.

## Compute & runtime
| Experiment | Backend | Runtime | Run id |
|---|---|---|---|
| Baseline (Claims 1,2,4 synthetic) | local CPU | 50s | `02153086` |
| Claim 5 (localized CP) | local CPU | 1m55s | `7fa30dd4` |
| Claim 3 (real-world, full suite) | HF `cpu-upgrade` | 2m39s | `a1c6933c` |

CPU estimate ≤1 core for local short tasks; Claim 3 (uncertain runtime) routed to
Hugging Face `cpu-upgrade` per the compute policy.

## Source-artifact drift (Claim 2)
The committed `simulation_subgaussian.py` sets noise `bias=20` (VCP length ≈43.6 at
α=0.10). The paper's Table 1 (22.894) was generated at `bias=10`. The checked-in
historical CSV `reference/upstream/table1_source_bias10.csv` is reproduced to
machine precision only at `bias=10` (max diff 7×10⁻¹⁵); at `bias=20` it differs by
20.8. Both are reported; nothing is normalized away.

## Deviations (honest, per claim)
- **Claim 3 datasets:** MEPS-19/20/21, BLOG-DATA, FACEBOOK-1/2 not reliably
  obtainable from public sources → not claimed as rerun; authors' reference CSVs
  corroborate 9/10. 4 extra real UCI datasets added for generalization.
- **Claim 3 base model:** sklearn `MLPRegressor` (64-64-1 ReLU, Adam, early stop)
  instead of a torch MLP — identical architecture/protocol, C-optimized for CPU;
  no dropout (documented).
- **Claim 3 size:** datasets >10k rows subsampled to 10k; `max_iter` 200 with
  early stopping — for CPU feasibility; does not change PT<VCP.
- **Claim 5 localizer:** sklearn MLPRegressor σ̂ (identical role to a torch
  localizer); cherry-pick shrink reported as observation (rigorously shown in the
  Prop-1 two-point case).

## Reproducibility
All verifiers are deterministic (fixed seeds) and exit nonzero on failure.
Raw JSON outputs: `outputs/{claims_synthetic,claim3_real_world,claim5_localized_cp}.json`.
