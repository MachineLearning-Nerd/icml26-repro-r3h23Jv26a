# Methods and source audit

## Paper

*Questioning the Coverage-Length Metric in Conformal Prediction: When Shorter
Intervals Are Not Better*, [arXiv:2601.21455v2](https://arxiv.org/abs/2601.21455v2),
OpenReview r3h23Jv26a.

## Environment

- Python 3.12.
- CPU-only PyTorch wheel where PyTorch is used.
- Locked dependencies in pyproject.toml and uv.lock.
- Six focused tests in repro/tests.

## Producers

| Producer | Purpose |
|---|---|
| repro/src/pt_core.py | Clean-room VCP/PT synthetic protocol |
| repro/src/claims_synthetic.py | C1, C2, and C4 aggregate evidence |
| repro/run_full_source_synthetic.py | Current author snapshot versus clean-room equivalence |
| repro/src/claim3_real_world.py | Five-seed real regression comparison |
| repro/src/verify_localized_pt_equivalence.py | Proposition 1 and IS constructive audit |
| repro/src/claim5_localized_cp.py | Trained-localizer simulation |

## Deviations

- The committed author code uses bias 20; Table 1 corresponds to bias 10.
- The bias-10 historical CSV matches the clean-room output, but the paper's
  p=.96 PT value is not exact.
- Claim 3 runs seven obtainable UCI datasets. Large datasets are capped at
  10,000 rows and the sklearn MLP uses max_iter=200 with early stopping.
- The paper's unavailable datasets and trained checkpoints are not substituted.
- The real-world model is a sklearn 64-64-1 MLP without the paper's dropout;
  this is documented as a protocol deviation.
- The trained localizer result is a finite diagnostic, not a claim about every
  localized conformal method.

## Reproducibility commands

~~~bash
uv run python repro/src/verify_final.py
uv run pytest -q
uv run python repro/run_full_source_synthetic.py
uv run python repro/verify_full_synthetic.py
uv run python repro/src/verify_localized_pt_equivalence.py
uv run python repro/src/audit_localized_pt_equivalence.py
~~~
