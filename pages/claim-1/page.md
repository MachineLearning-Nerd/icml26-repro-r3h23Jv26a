# Claim 1 — PT reduces length while preserving marginal coverage

## Contract

The Prejudicial Trick returns a null or minimal interval with probability 1-p
and an adjusted conformal interval with probability p. The adjustment is
intended to preserve marginal coverage while lowering average length.

## Scoped verdict: VERIFIED_SCOPED

The committed bias-20 source protocol covers five seeds, four alpha values, and
five p values at n=2,000:

- 16/16 nontrivial alpha/p aggregates have PT-VCP length below VCP length.
- Maximum aggregate coverage error is 0.013.
- The 20 p=1 boundary rows exactly recover the VCP interval and stability.

The same calculation at bias 10 has 13/16 shorter cells. This is why the
bias-10 Table-1 path is documented separately as a source-artifact audit.

## Production path

repro/src/pt_core.py generates the source-compatible data, model, conformal
radius, and PT branches. repro/src/claims_synthetic.py aggregates the rows and
writes outputs/claims_synthetic.json. The independent artifact check is in
repro/verify_full_synthetic.py.

~~~bash
uv run python -m repro.src.claims_synthetic
uv run python repro/verify_full_synthetic.py
~~~

This finite experiment checks the mechanism; it does not prove the paper's
coverage theorem.
