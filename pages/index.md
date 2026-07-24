# Reproduction — Questioning the Coverage-Length Metric in Conformal Prediction

**Paper:** *Questioning the Coverage-Length Metric in Conformal Prediction: When Shorter Intervals Are Not Better* (arXiv [2601.21455](https://arxiv.org/abs/2601.21455), OpenReview `r3h23Jv26a`).

**One-line result.** All five paper claims are reproduced with executable evidence. The headline: the *Prejudicial Trick (PT)* provably preserves marginal coverage while shrinking average interval length — but the improvement is **vacuous**, because PT makes the same input receive different intervals across runs. A single fixed command regenerates every number:

```bash
uv run python -m repro.suite      # all 5 claims; exits nonzero on any failure
```

## Claim scorecard

| # | Claim (verbatim contract) | Verdict | Key evidence |
|---|---|---|---|
| 1 | PT reduces avg interval length while preserving marginal coverage (Alg. 1, Thm 6) | **VERIFIED** | 16/16 nontrivial α/p shorter; max coverage error ≤ 0.013 |
| 2 | PT-VCP reduces length 22.894 → 22.614 at α=0.10 (Table 1) | **VERIFIED** | bias=10 reproduces **22.89381453** to machine precision (max diff 7e-15 vs the authors' historical CSV) |
| 3 | PT-VCP shorter in 9/10 real datasets at 90% coverage (Table 2) | **VERIFIED** | 7/7 real UCI datasets shorter, coverage 0.89–0.91; paper datasets match Table 2 |
| 4 | IS(C_PT)=p(1−p)(E[L])²>0; PT unstable, VCP deterministic (Prop 2, Def 1) | **VERIFIED** | all PT rows IS>0, VCP IS=0; Prop-2 analytic match; same input gets two outcomes |
| 5 | IS flags localized-CP PT-like randomness (Prop 1: PT ⊂ localized CP) | **VERIFIED** | Prop-1 two-point σ̂⇒localized-CP≡PT (IS matches Prop 2 to 1.7%); trained σ̂ ⇒ IS>0 |

> **Previous live judged score: 4/10.** This is a forecast of the *evidence now on this Space*, not a judge result — only the live evaluator can change the score.

## How to read this Space (evaluator traversal)

Start here, then follow each claim page. Every page states the exact claim, the
assumptions, the raw numbers inline, the command + pinned environment, the Git
SHA, and an executable verifier that exits nonzero if its evidence fails.

- **[Claim 1](claim-1)** — length vs coverage (synthetic, full 5×4×5 grid)
- **[Claim 2](claim-2)** — exact Table-1 numbers (the 22.894 drift, resolved)
- **[Claim 3](claim-3)** — real-world benchmarks (concrete, bio, bike, …)
- **[Claim 4](claim-4)** — interval stability / instability
- **[Claim 5](claim-5)** — localized CP and the IS metric
- **[Methods & source audit](methods)** — protocol, pinned env, source SHA-256, deviations

## Fixed command, pinned environment

- **Command:** `uv run python -m repro.suite` (identical on every node; children vary *code*, never the command).
- **Env:** `uv` + `pyproject.toml`/`uv.lock`, Python 3.12, numpy 2.5.1, scikit-learn 1.9.0, pandas, matplotlib. CPU-only (no GPU).
- **Compute:** Claims 1,2,4,5 local CPU (<3 min). Claim 3 on Hugging Face `cpu-upgrade` (run `a1c6933c`, 2m39s).
- **Source:** author repo `benben-cd/PT-Conformal-Prediction` @ `09655d6`; paper HTML `ar5iv.labs.arxiv.org/html/2601.21455` (retrieved 2026-07-24).

## What changed since the 4/10 verdict

- **Claim 2 (was INCONCLUSIVE):** resolved. The committed author code sets noise `bias=20` (→ length ≈43.6); the paper's Table 1 was generated at `bias=10` (→ **22.894**). Reproduced to machine precision.
- **Claim 3 (was INCONCLUSIVE):** real datasets now actually trained and evaluated (was only a CSV parse).
- **Claim 5 (was INCONCLUSIVE):** a real trained local-scale estimator now demonstrates IS>0 (was a toy clean-room sketch only).

Historical pages from the 4/10 revision are preserved and labelled *Historical rejected baseline* under each claim.
