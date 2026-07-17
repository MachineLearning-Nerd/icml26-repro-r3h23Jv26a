# Source audit

- Paper: *Questioning the Coverage-Length Metric in Conformal Prediction: When Shorter Intervals Are Not Better* (arXiv:2601.21455; OpenReview `r3h23Jv26a`).
- Author source: `benben-cd/PT-Conformal-Prediction` pinned to `09655d6c58be2a9b24aafb739c37397e0488e933`.
- Full executable source protocol: `ordinary_regression_task/simulation_subgaussian.py` (Table 1): five fixed seeds, `n=2,000`, 80/20 split, four coverages, five PT probabilities — 100 source conditions.

The released construction changes a base conformal radius from `q_alpha` to
`q_alpha_prime`, where `alpha_prime = 1 - (1-alpha)/p`, and independently
returns the adjusted interval with probability `p` and a singleton interval
otherwise. Consequently `p * (1-alpha_prime) = 1-alpha`, while the randomized
length may be lower. The exact construction is what Claims 1–3 concern.

Scope boundary: the repository also supplies historical result CSVs for real
regression and ImageNet, but its README states that the corresponding raw data
and trained checkpoints are intentionally absent. This reproduction executes
the complete released synthetic protocol and independently verifies the
mechanism there. It only parses the supplied external Table-3 CSV as a source
artifact check; it never presents that parse as a rerun of unavailable data.

Reproducibility drift: the unmodified current `simulation_subgaussian.py`
output is compared byte-for-number against the clean-room implementation. Its
output is also compared with the checked-in historical summary. The latter
comparison is recorded in `outputs/full_synthetic_summary.json`; a nonzero
value is an author-source artifact discrepancy, not hidden or normalized away.
