# Reproduction — Questioning the Coverage-Length Metric

Paper: *Questioning the Coverage-Length Metric in Conformal Prediction: When
Shorter Intervals Are Not Better* ([arXiv:2601.21455v2](https://arxiv.org/abs/2601.21455v2),
OpenReview r3h23Jv26a).

This audit reproduces the PT mechanism and its instability signal, while
separating exact source-artifact matches from partial real-world reruns.

## Claim scorecard

| # | Contract | Evidence | Status |
|---|---|---|---|
| 1 | PT can shorten synthetic intervals while preserving marginal coverage | 16/16 nontrivial bias-20 conditions shorter; error ≤ 0.013 | VERIFIED_SCOPED |
| 2 | Table-1 synthetic values | Current source matches clean-room; bias-10 historical CSV matches, but p=.96 PT is 22.5144 rather than paper's 22.614 | PARTIAL_SOURCE_ARTIFACT_AUDIT |
| 3 | PT-VCP is shorter on real regressions | 7 obtainable datasets, including all 3 obtainable paper datasets; unavailable datasets are not rerun | PARTIAL_EXTERNAL_DATA_AUDIT |
| 4 | PT creates interval instability; VCP is deterministic | 80 stochastic rows positive and two-outcome; 20 p=1 controls deterministic | VERIFIED_SCOPED |
| 5 | IS catches the localized-CP extreme case | 15/15 conditions, 1.5M retrainings, zero mismatches; trained localizer is a separate simulation | VERIFIED_SCOPED plus SIMULATION_CHECK_SCOPED |

## Start here

- Claim 1 — synthetic length and coverage.
- Claim 2 — Table-1 source drift and historical CSV comparison.
- Claim 3 — obtainable real-world regressions and deviations.
- Claim 4 — PT instability and the p=1 negative control.
- Claim 5 — trained localizer and Interval Stability.
- Localized-CP equivalence — constructive Proposition 1 audit.
- Methods and source audit — provenance, environment, and scope.

## Fast verification

~~~bash
uv run python repro/src/verify_final.py
uv run pytest -q
~~~

The full suite is uv run python -m repro.suite; real-world data loading
requires network access.
