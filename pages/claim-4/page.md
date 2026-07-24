# Claim 4 — PT is unstable; IS(C_PT) = p(1−p)(E[L])² > 0

## Exact claim contract

> Despite valid marginal coverage, PT yields highly unstable predictions:
> Proposition 2 proves IS(C_PT) = p(1−p)(E[L])² > 0 (Definition 1), so the same
> input can receive completely different intervals across repeated runs.

## Verdict: VERIFIED

Three independent checks, all on the full synthetic grid (bias=10, 5 seeds):

1. **Two outcomes for the same input.** In **all 80** p<1 rows, both the singleton
   (null) and the adjusted interval occur for the same test point across runs;
   all 100 base-VCP rows are deterministic (0 singletons).
2. **IS > 0 for PT, IS = 0 for VCP.** Every p<1 row has `pt_stability > 0`
   (≈0.34–1.19); every base row is exactly 0.0. A separate 500-run experiment
   gives VCP std = 0.0 vs PT-VCP std ≈ 0.22.
3. **Proposition 2 analytic match.** For the two-point length law, the empirical
   interval-stability matches the closed form `p(1−p)(E[L])²` (see Claim 5's
   Prop-1 extreme case: 24.48 empirical vs 24.90 analytic, 1.7%).

## Verifier + command

```bash
uv run python -m repro.src.claims_synthetic   # verify_claim4; exit 0
```
Source: `repro/src/claims_synthetic.py::verify_claim4`. Negative control: p=1 gives
IS = 0 and zero singletons. Git SHA: `272093b`.
