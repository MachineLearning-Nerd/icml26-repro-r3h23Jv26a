# Claim 5 — localized-CP/PT equivalence and Interval Stability

## Source scope

- Paper: [arXiv:2601.21455v2](https://arxiv.org/abs/2601.21455v2).
- Audited sections: Proposition 3.2, Equation 4, Definition 1, and
  Equations 15–16.
- Primary HTML source: [arxiv.org/html/2601.21455](https://arxiv.org/html/2601.21455).

## Deterministic clean-room verification

The verifier implements the normalized-score interval from Equation 4. For a
fixed input, each retraining emits local scale 0+ with probability 1-p or scale
1 with probability p. The resulting localized-CP interval is compared
sample-by-sample with the two PT branches.

The committed result covers five seeds and p values 0.91, 0.95, and 0.99, with
100,000 retrainings per condition:

| Check | Result |
|---|---:|
| Conditions passed | 15/15 |
| Total retrainings | 1,500,000 |
| Samplewise mismatches | 0 |
| Maximum relative stability error | 2.4741% |
| p=1 deterministic control | zero |
| Independent audit | PASS |

## Reproduction commands

~~~bash
uv run python repro/src/verify_localized_pt_equivalence.py
uv run python repro/src/audit_localized_pt_equivalence.py
~~~

The output files are outputs/localized_pt_equivalence.json and
outputs/localized_pt_equivalence_audit.json.

## Scope guardrail

This verifies the constructive extreme localized-CP case and that the metric
flags its retraining randomness. It does not claim that every localized
conformal method is unstable or replace the separate real-data audit.
