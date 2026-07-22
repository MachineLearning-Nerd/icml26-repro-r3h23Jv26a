# Claim 5 — localized CP/PT equivalence and Interval Stability

## Source scope

- Paper: arXiv:2601.21455, *Questioning the Coverage-Length Metric in Conformal Prediction: When Shorter Intervals Are Not Better*.
- Primary source: `https://ar5iv.labs.arxiv.org/html/2601.21455`.
- Audited scope: Section 3.2, Proposition 1 and Equation 4; Section 4, Definition 1 and Equations 15–16.
- Proposition 1 states that, for the extreme two-point local scale estimator, localized-CP intervals are "equivalent in form to Equation (2)."

## Claim addressed

The proposed Interval Stability metric flags a localized conformal method that
implicitly uses PT-like retraining randomness to shrink average interval
length, while Proposition 1 identifies PT as an extreme localized-CP case.

## Deterministic clean-room verification

`verify_localized_pt_equivalence.py` implements the normalized-score interval
from Equation 4. For the same fixed input, each retraining emits local scale
`1e-12` (the paper's `0+`) with probability `1-p`, or scale `1` with probability
`p`. The corresponding interval is compared sample by sample with the two PT
branches. Definition 1's empirical conditional interval-size variance is then
compared with the exact Bernoulli variance
`p(1-p)(L_informative-L_minimal)^2`.

The grid contains five fixed seeds and `p={0.91,0.95,0.99}`, with 100,000
retrainings per condition. A deterministic `p=1` localizer is the negative
control.

## Results

| Check | Result |
|---|---:|
| Conditions passed | 15/15 |
| Total retrainings | 1,500,000 |
| Localized-CP/PT interval mismatches | 0 |
| Empirical Interval Stability range | 0.036985–0.329352 |
| Maximum relative error vs analytic stability | 2.4741% |
| Mean width reduced in stochastic conditions | 15/15 |
| Deterministic `p=1` control stability | exactly 0 |
| Independent audit | PASS |

```text
source=https://ar5iv.labs.arxiv.org/html/2601.21455
scope=Section 3.2 Proposition 1 and Equation 4; Section 4 Definition 1 and Equations 15-16
conditions=15/15 retrainings=1500000
samplewise_equivalence_mismatches=0
minimum_interval_stability=0.036985037016
maximum_relative_stability_error=0.024741
p1_deterministic_control=True
verdict=supports
results_sha256_without_hash=bbcc70450a6ba1be7d2470f02e10cd78d9063241e8399ad3361d589c047b5fae
```

Independent audit hash:
`52e8c9ab22819c9c24016207225c40f86a8bb3a4d6846cdf34d3fffe6c203863`.

## Reproduction commands

```bash
python3 repro/src/verify_localized_pt_equivalence.py
python3 repro/src/audit_localized_pt_equivalence.py
```

Both scripts use only the Python standard library and run on CPU in under one
second on the audited machine.

## Scope guardrail

This verifies the constructive extreme localized-CP case in Proposition 1 and
that Definition 1 flags its retraining randomness. It does not claim that every
localized conformal method is unstable, and it does not address the separate
real-dataset claim.
