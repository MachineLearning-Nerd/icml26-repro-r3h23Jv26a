# Claim 4 — PT creates interval instability

## Contract

The paper's Interval Stability metric is positive for the randomized PT
construction and zero for deterministic VCP. Proposition 2 gives the
two-branch variance expression.

## Scoped verdict: VERIFIED_SCOPED

The full synthetic artifact contains 100 rows:

- 80 p<1 PT rows have positive stability and both singleton and informative
  outcomes for the same input.
- 20 p=1 negative-control rows are deterministic with zero stability.
- The independent verifier reports zero false positives and zero false
  negatives at its 1e-12 stability threshold.
- The source-supplied Table-3 CSV has 10 rows, zero VCP stability, and positive
  PT stability; this is an artifact check, not a rerun of unavailable data.

## Production path

repro/src/pt_core.py computes repeated interval lengths.
repro/src/claims_synthetic.py records the synthetic result, and
repro/verify_full_synthetic.py independently checks the output.

~~~bash
uv run python -m repro.src.claims_synthetic
uv run python repro/verify_full_synthetic.py
~~~
