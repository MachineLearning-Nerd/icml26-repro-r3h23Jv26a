# Claim-to-evidence ledger

This file is the authoritative scope ledger for the repository. A status
describes only the evidence listed in the same row.

## Claim 1 — PT length and marginal coverage

Status: VERIFIED_SCOPED.

Production path:

1. repro/src/pt_core.py generates the five seeded synthetic datasets, fits the
   linear base model, computes VCP and PT conformal radii, and samples the PT
   branch.
2. repro/src/claims_synthetic.py runs bias 20 and aggregates 5 seeds × 4 alpha
   values × 5 p values.
3. repro/verify_full_synthetic.py recomputes aggregate length, coverage, and
   p=1 controls from the JSON rows.

Evidence:

- 100 recorded source-protocol rows.
- 16/16 p<1 aggregate conditions shorter at bias 20.
- Maximum aggregate coverage error 0.013.
- p=1 controls recover VCP length, coverage, and zero stability.

Boundary: this finite run does not prove the paper's theorem or its
exchangeability assumptions.

## Claim 2 — Table 1 values

Status: PARTIAL_SOURCE_ARTIFACT_AUDIT.

Production path:

1. repro/run_full_source_synthetic.py copies the committed author snapshot to
   a temporary directory and executes it without network access.
2. The clean-room layout from repro/src/pt_core.py is compared with the
   generated author CSV.
3. The bias-10 run is compared with
   reference/upstream/table1_source_bias10.csv.

Evidence:

| Measurement | Value |
|---|---:|
| Clean-room versus current author snapshot | 0.0 max absolute difference |
| Bias-10 clean-room versus historical CSV | 7.105427357601002e-15 |
| Bias-20 versus historical CSV | 20.802883433998257 |
| Paper VCP, alpha=.10 | 22.894 |
| Reproduction VCP, alpha=.10 | 22.89381453213531 |
| Paper PT-VCP, alpha=.10, p=.96 | 22.614 |
| Reproduction PT-VCP, alpha=.10, p=.96 | 22.514392464628397 |
| Paper PT-VCP, alpha=.10, p=.98 | 22.714 |
| Reproduction PT-VCP, alpha=.10, p=.98 | 22.714399886459027 |

Boundary: the historical artifact match is exact to numerical precision, but
the paper's p=.96 printed PT value is not reproduced exactly. The discrepancy
is retained rather than silently adjusted.

## Claim 3 — Real-world regression benchmarks

Status: PARTIAL_EXTERNAL_DATA_AUDIT.

Production path:

1. repro/src/real_datasets.py obtains public UCI datasets and records
   dataset-specific failures.
2. repro/src/claim3_real_world.py standardizes features, normalizes targets,
   trains a 64-64-1 ReLU Adam MLP for five seeds, adds the documented residual
   bias, and compares VCP with PT-VCP.
3. outputs/claim3_real_world.json stores per-seed and aggregate results.

Evidence:

- Seven datasets executed: concrete, bio, bike, airfoil, energy, wine, and
  realestate.
- PT-VCP is shorter in 7/7.
- Three paper datasets are included; all three are shorter.
- PT-VCP aggregate coverage ranges from 0.8922077922 to 0.9047.
- Large datasets are capped at 10,000 rows; max_iter is 200 with early
  stopping; the model does not use the paper's dropout.

Boundary: the full paper's 9/10 dataset claim is not rerun. Unavailable
datasets and trained checkpoints are not represented by substitute runs.

## Claim 4 — Interval Stability

Status: VERIFIED_SCOPED.

Production path:

1. repro/src/pt_core.py computes repeated interval lengths for the PT and VCP
   branches.
2. repro/src/claims_synthetic.py records stability for all synthetic rows.
3. repro/verify_full_synthetic.py independently checks a 1e-12 threshold and
   the p=1 negative control.

Evidence:

- 80 p<1 rows have positive stability and both singleton and informative
  outcomes.
- 20 p=1 rows are deterministic with zero stability.
- Independent check: 80 true positives, 20 true negatives, zero false
  positives, zero false negatives.
- The source-supplied Table-3 CSV has 10 rows, all VCP stability zero and all PT
  stability positive; this is an artifact check only.

## Claim 5 — localized CP and PT equivalence

### Constructive extreme case

Status: VERIFIED_SCOPED.

repro/src/verify_localized_pt_equivalence.py uses scale values 0+ and 1 to
construct the Proposition 1 limiting case. It compares each localized interval
with the corresponding PT branch, computes empirical and analytic stability,
and checks a deterministic p=1 control.

- 15/15 conditions pass.
- 1,500,000 total retrainings.
- Zero samplewise interval mismatches.
- Maximum relative stability error 0.024741.
- Independent audit passes.

Evidence files: outputs/localized_pt_equivalence.json and
outputs/localized_pt_equivalence_audit.json.

### Trained localizer

Status: SIMULATION_CHECK_SCOPED.

repro/src/claim5_localized_cp.py trains a finite local-scale estimator for
three seeds and twenty retrains per seed.

- Mean localized IS: 0.05465056857661733.
- VCP IS: 0.0.
- Mean localized coverage: 0.90625.
- All three runs have positive localized IS.
- One run does not show cherry-pick shrink, so this is not a universal
  instability or cherry-pick claim.

Evidence file: outputs/claim5_localized_cp.json.

## Non-claims

This repository does not claim theorem proofs, full paper-table reproduction,
all real datasets, classification experiments, unavailable checkpoints,
official benchmark scores, or author endorsement.
