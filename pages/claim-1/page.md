# Claim 1 — PT reduces length while preserving marginal coverage

## Exact claim contract

> The Prejudicial Trick (Algorithm 1) returns a null/minimal interval with
> probability 1−p and an adjusted conformal interval with probability p,
> provably preserving valid marginal coverage (Theorem 6) while shrinking the
> average interval length.

## Verdict: VERIFIED

Across the full released synthetic grid (**5 seeds × 4 α × 5 p, n=2000**) at both
the committed `bias=20` and the Table-1 `bias=10`:

- **16/16** nontrivial (p<1) α/p aggregates have PT-VCP mean length **<** VCP length.
- Maximum aggregate coverage error from nominal: **≤ 0.013** (bias=20) / ≤ 0.015 (bias=10).
- The `p=1` boundary **exactly** recovers the base VCP interval (negative control).

## Why it holds

PT sets α′ = 1 − (1−α)/p, so `p·(1−α′) = 1−α`: marginal coverage is preserved by
construction (Theorem 6). Length shrinks because the adjusted interval is only
slightly wider than the base, but a (1−p) fraction of points get a null/minimal
interval, lowering the average.

## Verifier + command

```bash
uv run python -m repro.src.claims_synthetic   # verify_claim1; exit 0
```
Source: `repro/src/claims_synthetic.py::verify_claim1`. Deterministic seeds `[0..4]`.
Negative control: p=1 row length/coverage identical to VCP. Git SHA: `272093b`.
