# Claim 5 — Interval Stability and localized conformal prediction

## Contract

The paper identifies PT as an extreme localized-conformal construction and
proposes Interval Stability as a way to detect PT-like run-to-run variation.

## Constructive verdict: VERIFIED_SCOPED

repro/src/verify_localized_pt_equivalence.py uses a two-point local-scale
estimator that emits 1 or 0+ with the paper's p probability. Across 15 fixed
conditions and 1,500,000 retrainings:

- samplewise localized-CP/PT interval mismatches: 0;
- minimum empirical stability: 0.036985;
- maximum relative error against analytic stability: 0.024741;
- p=1 deterministic control: exactly zero stability;
- independent audit: PASS.

## Trained-localizer verdict: SIMULATION_CHECK_SCOPED

repro/src/claim5_localized_cp.py trains a finite local-scale diagnostic for
three data seeds and twenty retrains per seed. All three runs have positive
localized IS, VCP IS exactly 0, and mean localized coverage 0.90625. The mean
localized IS is 0.0546505686. One run does not show a cherry-pick shrink, so
the trained experiment is reported as a diagnostic rather than a universal
claim.

## Production paths

~~~bash
uv run python repro/src/verify_localized_pt_equivalence.py
uv run python repro/src/audit_localized_pt_equivalence.py
uv run python -m repro.src.claim5_localized_cp
~~~

The constructive audit is standard-library-only. The trained-localizer
diagnostic uses the pinned scientific Python environment.
