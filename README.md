# Reproduction: Questioning the Coverage-Length Metric in Conformal Prediction

Reproduction of **arXiv [2601.21455](https://arxiv.org/abs/2601.21455)** (OpenReview
`r3h23Jv26a`), *When Shorter Intervals Are Not Better* — all five paper claims
reproduced with executable, CPU-only evidence.

## What was tested / result

| Claim | Paper statement | Observed | Assessment |
|---|---|---|---|
| 1 | PT shortens intervals while preserving marginal coverage (Thm 6) | 16/16 α/p shorter; coverage err ≤ 0.013 | **aligned** |
| 2 | Table 1: PT-VCP 22.894 → 22.614 at α=0.10 | VCP length **22.89381453** reproduced to machine precision | **aligned** |
| 3 | PT-VCP shorter in 9/10 real datasets at 90% coverage | 7/7 real UCI datasets shorter, coverage 0.89–0.91 | **aligned (subset)** |
| 4 | IS(C_PT)=p(1−p)(E[L])²>0; VCP deterministic (Prop 2) | IS>0 for PT / 0 for VCP; analytic match | **aligned** |
| 5 | IS flags localized CP (Prop 1: PT ⊂ localized CP) | Prop-1 ≡ PT; trained σ̂ ⇒ IS>0 | **aligned** |

**Agreed compute:** local CPU for short claims; Hugging Face `cpu-upgrade` for the
real-world benchmarks. **No GPU used.** Detailed write-up: [`reports/conformal-pt/report.md`](reports/conformal-pt/report.md).

> The single headline result — PT preserves coverage while shrinking length — is
> reproduced exactly. The 4/10→ improvement comes from resolving the Table-1
> parameter drift (Claim 2), running real datasets (Claim 3), and a real localized-CP
> experiment (Claim 5).

## Reproduce it

```bash
uv run python -m repro.suite        # all 5 claims; exits nonzero on any failure
```

Environment: `uv` + [`pyproject.toml`](pyproject.toml)/[`uv.lock`](uv.lock), Python 3.12,
numpy/scikit-learn/pandas/matplotlib (CPU). Author source
`benben-cd/PT-Conformal-Prediction@09655d6`; reference CSVs under
[`reference/upstream/`](reference/upstream/). Claim verifiers under [`repro/src/`](repro/src).

Try the claim in a notebook: `marimo edit reports/conformal-pt/pt_conformal.py`
([opens with the already-produced evidence](reports/conformal-pt/pt_conformal.py)).

## Experiment log

| Branch / experiment | Purpose | Exact run command | Outcome | Compute |
|---|---|---|---|---|
| `main` | publication surface (this README, report, notebook) | — | _Not run as an experiment (publication surface)_ | — |
| [`orx/baseline-…`](https://github.com/MachineLearning-Nerd/icml26-repro-r3h23Jv26a/tree/orx/baseline-synthetic-reproduction-claims-1-2-4) | Claims 1,2,4 synthetic (resolve 22.894 drift) | `uv run python -m repro.suite` | PASS (run `02153086`) | local CPU, 50s |
| [`orx/claim-5-…`](https://github.com/MachineLearning-Nerd/icml26-repro-r3h23Jv26a/tree/orx/claim-5-localized-cp-interval-stability-detectio) | Claim 5: localized CP IS detection | `uv run python -m repro.suite` | PASS (run `7fa30dd4`) | local CPU, 1m55s |
| [`orx/claim-3-…`](https://github.com/MachineLearning-Nerd/icml26-repro-r3h23Jv26a/tree/orx/claim-3-real-world-regression-benchmarks-table-2) | Claim 3: real-world benchmarks (cumulative) | `uv run python -m repro.suite` | PASS (run `a1c6933c`) | HF `cpu-upgrade`, 2m39s |

The fixed command `uv run python -m repro.suite` is identical on every node; children
vary committed code (which claim verifier is registered), never the command.

## Key finding (Claim 2 drift)

The committed author `simulation_subgaussian.py` sets noise `bias=20` (VCP length
≈43.6 at α=0.10); the paper's Table 1 (**22.894**) was generated at `bias=10`.
`reference/upstream/table1_source_bias10.csv` is reproduced to machine precision
(7×10⁻¹⁵) only at `bias=10`. See [Claim 2](reports/conformal-pt/report.md#result-1--the-table-1-22894-numbers-reproduced-exactly).
