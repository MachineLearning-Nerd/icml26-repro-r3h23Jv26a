# Claim 5 — Interval Stability flags localized CP (PT ⊂ localized CP)

## Exact claim contract

> The proposed Interval-Stability (IS) metric can flag methods, such as localized
> conformal prediction, that implicitly exploit PT-like randomness to shrink
> length, since Proposition 1 shows PT is a special case of localized CP when
> local scale estimators output extreme values (Definition 1, Proposition 1).

## Verdict: VERIFIED

Localized CP uses the normalized score `Ŝ_norm(x,y) = Ŝ(x,y)/σ̂(x)` (Eq. 4). Two
experiments confirm the claim:

### (A) Proposition 1 extreme case — localized CP ≡ PT

A σ̂ emitting only {0⁺, 1} (prob 1−p / p) makes the localized interval
`[ŷ ± q·σ̂(x)]` **sample-wise identical** to the PT interval (Eq. 2). The
interval-stability equals Proposition 2's closed form `p(1−p)(E[L])²`:

| | empirical IS (Monte Carlo n=2×10⁵) | Proposition 2 analytic |
|---|---|---|
| p=0.95 | **24.48** | 24.90 |

Relative error **1.7%** (< 2%); both branches present; IS > 0. ✓

### (B) Realistic trained localizer — IS detects retraining randomness

A **trained** MLP local-scale estimator σ̂ (Remark 3), retrained 20× with
independent seeds, on the Example-2 distribution (bias=10):

| | IS(localized CP) | IS(VCP) | localized coverage |
|---|---|---|---|
| 3 data seeds | **> 0** (mean 0.055) | **0** (deterministic) | 0.906 ≈ 0.90 |

IS flags the localized method (IS>0) while VCP is exactly 0; marginal coverage is
preserved. ✓ (Cherry-picking the shortest retrain is the paper's cautionary point;
it is rigorously realized in the Prop-1 two-point case above, and reported as an
observation for the continuous localizer.)

## Verifier + command

```bash
uv run python -m repro.src.claim5_localized_cp   # writes outputs/claim5_localized_cp.json; exit 0
```
Source: `repro/src/claim5_localized_cp.py`. Negative control: σ̂≡1 (VCP) ⇒ IS=0.
Git SHA: `272093b`.
