# Conformal prediction coverage–length audit

Paper: *Questioning the Coverage-Length Metric in Conformal Prediction: When
Shorter Intervals Are Not Better*,
[arXiv:2601.21455v2](https://arxiv.org/abs/2601.21455v2).

## Finding

The paper's PT construction can make average intervals shorter while preserving
synthetic marginal coverage, but the same input can receive different
intervals across runs. This repository reproduces that mechanism and audits
the proposed Interval Stability diagnostic.

## Evidence summary

| Area | Result | Status |
|---|---|---|
| Synthetic PT mechanism | 16/16 nontrivial alpha/p conditions shorter at bias 20; maximum coverage error 0.013 | scoped verified |
| Table 1 | Current source and clean-room match exactly; bias-10 historical CSV matches to 7.1e-15 | partial artifact audit |
| Real regression | 7/7 obtainable datasets shorter; 3 paper datasets included; PT coverage 0.892–0.905 | partial external audit |
| PT stability | 80 stochastic rows positive, 20 p=1 controls deterministic | scoped verified |
| Localized-CP extreme case | 15/15 conditions pass; 1.5 million retrainings; zero interval mismatches | scoped verified |
| Trained localizer | Mean IS 0.05465 across three seeds; VCP IS 0; mean coverage 0.90625 | scoped simulation |

## Table-1 qualification

The current source uses bias 20; the paper's table corresponds to bias 10. At
bias 10, the clean-room output reproduces the checked-in historical CSV, not
every printed paper value: the p=0.96 PT length is 22.51439246 versus the
paper's 22.614, while the p=0.98 cell is 22.71439989 versus 22.714. The
repository therefore calls this a source-artifact audit rather than an exact
Table-1 reproduction.

## Production paths

- Claims 1, 2, and 4: repro/src/pt_core.py →
  repro/src/claims_synthetic.py → outputs/claims_synthetic.json.
- Current-source equivalence: repro/run_full_source_synthetic.py →
  outputs/full_synthetic_summary.json.
- Claim 3: repro/src/claim3_real_world.py →
  outputs/claim3_real_world.json.
- Claim 5: repro/src/verify_localized_pt_equivalence.py and
  repro/src/claim5_localized_cp.py →
  outputs/localized_pt_equivalence.json and
  outputs/claim5_localized_cp.json.

## Reproduction

~~~bash
uv run python repro/src/verify_final.py
uv run pytest -q
uv run python repro/run_full_source_synthetic.py
uv run python repro/src/verify_localized_pt_equivalence.py
uv run python repro/src/audit_localized_pt_equivalence.py
~~~

The real-world suite additionally requires network access to obtain public UCI
datasets:

~~~bash
uv run python -m repro.suite
~~~

The figures in this directory are explanatory views of the committed results;
the JSON artifacts and verifiers are the authoritative evidence.
