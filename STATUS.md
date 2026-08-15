# Reproduction status

## Repository

- Intended final name: MachineLearning-Nerd/icml26-conformal-prediction-coverage-length
- Original name: MachineLearning-Nerd/icml26-repro-r3h23Jv26a
- Publication branch: main
- Paper: [Questioning the Coverage-Length Metric in Conformal Prediction](https://arxiv.org/abs/2601.21455v2)
- OpenReview: [r3h23Jv26a](https://openreview.net/forum?id=r3h23Jv26a)

## Current audit state

scoped_audit_ready — documentation and committed evidence are being published
with explicit limitations.

- Synthetic PT mechanism: VERIFIED_SCOPED.
- Synthetic Table 1: PARTIAL_SOURCE_ARTIFACT_AUDIT; the bias-10 historical
  CSV matches, but the paper's p=0.96 PT length is not exact.
- Real-world regression: PARTIAL_EXTERNAL_DATA_AUDIT; 7 obtainable datasets
  ran, while unavailable datasets/checkpoints are not claimed as rerun.
- PT instability and the constructive localized-CP equivalence: VERIFIED_SCOPED.
- Trained localizer: SIMULATION_CHECK_SCOPED.

## Verification

- uv run python repro/src/verify_final.py — committed evidence and scope
  invariants.
- uv run python repro/run_full_source_synthetic.py — clean-room/current
  source equivalence and historical artifact comparison.
- uv run python repro/verify_full_synthetic.py — independent synthetic and
  Table-3 artifact checks.
- uv run python repro/src/audit_localized_pt_equivalence.py — independent
  localized-CP audit.
- uv run pytest -q — 6 focused tests.

## Attribution

All publication commits and rewritten reachable history use:

MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>

No author endorsement or external score is implied.
