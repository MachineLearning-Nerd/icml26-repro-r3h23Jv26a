# Conformal Prediction Coverage–Length Audit — ICML 2026

Independent audit of *Questioning the Coverage-Length Metric in Conformal
Prediction: When Shorter Intervals Are Not Better* by Yizhou Min, Yizhou Lu,
Lanqi Li, Zhen Zhang, and Jiaye Teng.

- Paper: [arXiv:2601.21455v2](https://arxiv.org/abs/2601.21455v2)
- OpenReview: [r3h23Jv26a](https://openreview.net/forum?id=r3h23Jv26a)
- Intended repository: [MachineLearning-Nerd/icml26-conformal-prediction-coverage-length](https://github.com/MachineLearning-Nerd/icml26-conformal-prediction-coverage-length)
- Original repository name: icml26-repro-r3h23Jv26a

The paper shows that the Prejudicial Trick (PT) can preserve marginal coverage
while making average prediction intervals shorter by returning a null or
minimal interval on one branch and an adjusted conformal interval on the other.
The paper argues that this improvement is practically misleading because the
same input can receive different intervals across runs, and proposes Interval
Stability (IS) as a complementary diagnostic.

This repository is a clean-room audit of the released synthetic protocol,
selected real-data experiments, and the PT/localized-conformal connection. It
is not the authors' repository and it does not claim to reproduce every
theorem, dataset, checkpoint, classification result, or table in the paper.

## Audit scorecard

| Claim or mechanism | Evidence produced here | Status |
|---|---|---|
| PT shortens intervals while retaining synthetic marginal coverage | 100 deterministic source-protocol rows; 16/16 nontrivial alpha/probability conditions shorter; maximum aggregate coverage error 0.013 | VERIFIED_SCOPED |
| Table 1 synthetic values | Current author snapshot matches the clean-room implementation exactly; the bias-10 clean-room output matches the checked-in historical CSV to 7.1e-15 | PARTIAL_SOURCE_ARTIFACT_AUDIT |
| Real-world regression comparison | 7 obtainable UCI datasets run, all 7 shorter, 3/3 paper datasets included; unavailable datasets and checkpoints are not rerun | PARTIAL_EXTERNAL_DATA_AUDIT |
| PT interval instability and VCP negative control | 80 stochastic PT rows have positive stability and two outcomes; 20 p=1 controls are deterministic | VERIFIED_SCOPED |
| Proposition 1 localized-CP extreme case | 15 conditions, 1,500,000 retrainings, zero samplewise mismatches, p=1 control | VERIFIED_SCOPED |
| Trained local-scale estimator diagnostic | Three seeds and twenty retrains per seed; mean localized IS 0.05465, VCP IS 0, mean coverage 0.90625 | SIMULATION_CHECK_SCOPED |

The status labels are deliberately narrow. A passing script means that the
recorded check passed its stated finite experiment; it does not prove the
paper's theorem or establish the full paper-wide claim.

## Important qualifications

### Table 1 has two different discrepancies

The committed author snapshot uses noise bias 20, while the paper's Table 1
numbers are generated at bias 10. The clean-room implementation matches the
current snapshot exactly and differs from the historical Table-1 CSV by
20.8029 at bias 20. At bias 10 it matches that historical CSV to machine
precision.

The paper reports PT-VCP length 22.614 at alpha 0.10 and p 0.96. The committed
protocol produces 22.51439246 for that cell; it produces 22.71439989 at p 0.98,
matching the paper's 22.714 value. Therefore this repository records a source
artifact audit and does not call the entire Table 1 an exact reproduction.

### Real-world scope is partial

The executed real-data artifact covers concrete, bio, bike, airfoil, energy,
wine, and realestate. The paper's unavailable external datasets and trained
checkpoints are not silently replaced with the author-supplied CSVs. Those CSVs
are checked only as source artifacts, not as rerun evidence.

### What is not claimed

- A proof of any theorem.
- The complete Section 4/5 experiment suite.
- Full reproduction of all paper datasets, classification tasks, ablations, or
  author checkpoints.
- An endorsement by the paper authors.
- That every localized conformal method is unstable.

## How claims are produced

| Claim | Producer | Durable evidence |
|---|---|---|
| C1 | repro/src/pt_core.py recreates the synthetic VCP/PT protocol; repro/src/claims_synthetic.py aggregates five seeds, four alpha values, and five p values | outputs/claims_synthetic.json, outputs/full_synthetic_summary.json |
| C2 | repro/run_full_source_synthetic.py executes the committed author snapshot in isolation, compares its 100-condition layout to the clean-room output, and records the bias-10 historical-CSV comparison | outputs/full_synthetic_summary.json, outputs/claims_synthetic.json |
| C3 | repro/src/claim3_real_world.py loads obtainable UCI regressions, trains the documented 64-64-1 sklearn MLP protocol for five seeds, then compares VCP and PT-VCP | outputs/claim3_real_world.json |
| C4 | repro/src/claims_synthetic.py computes repeated interval stability; repro/verify_full_synthetic.py independently checks positive PT rows, deterministic p=1 controls, and the source-supplied Table-3 artifact | outputs/independent_verification.json |
| C5 | repro/src/verify_localized_pt_equivalence.py implements the two-point local-scale construction; repro/src/claim5_localized_cp.py runs the trained-localizer diagnostic | outputs/localized_pt_equivalence.json, outputs/localized_pt_equivalence_audit.json, outputs/claim5_localized_cp.json |

## Branch map

The original experiment branches are retained as evidence branches with clean
names:

| Final branch | Original branch | Purpose |
|---|---|---|
| main | main | Final publication surface and combined snapshot |
| evidence/synthetic-claims-1-2-4 | orx/baseline-synthetic-reproduction-claims-1-2-4 | Synthetic PT length, Table-1 drift, and stability |
| evidence/claim-3-real-world | orx/claim-3-real-world-regression-benchmarks-table-2 | Real-world regression benchmarks |
| evidence/claim-5-localized-cp | orx/claim-5-localized-cp-interval-stability-detectio | Localized-CP equivalence and IS |

See BRANCH_AUDIT.md for the exact pre-rename tips and publication-branch
policy.

## Reproduce or verify

The pinned environment requires Python 3.12 and CPU-only PyTorch wheels.

~~~bash
uv sync
uv run python repro/src/verify_final.py
uv run pytest -q
~~~

The fast verifier checks the committed JSON evidence and scope invariants. To
regenerate the synthetic artifacts and execute the committed author snapshot:

~~~bash
uv run python repro/run_full_source_synthetic.py
uv run python repro/verify_full_synthetic.py
~~~

To run the full suite, including network-backed UCI loading:

~~~bash
uv run python -m repro.suite
~~~

The localized-CP audit is standard-library-only:

~~~bash
uv run python repro/src/verify_localized_pt_equivalence.py
uv run python repro/src/audit_localized_pt_equivalence.py
~~~

## Repository layout

- repro/src/pt_core.py — clean-room synthetic PT/VCP implementation.
- repro/src/claims_synthetic.py — Claims 1, 2, and 4 producer.
- repro/src/claim3_real_world.py and repro/src/real_datasets.py — Claim 3.
- repro/src/claim5_localized_cp.py — trained-localizer diagnostic.
- repro/src/verify_localized_pt_equivalence.py — constructive Proposition 1 audit.
- outputs/ — committed result artifacts.
- reference/upstream/ — small pinned source snapshots and historical CSVs.
- CLAIM_EVIDENCE.md — claim-by-claim evidence ledger.
- SOURCE_MANIFEST.md — provenance and input inventory.
- CITATION.cff — software and paper citation metadata.

## Citation

~~~bibtex
@article{min2026questioning,
  title   = {Questioning the Coverage-Length Metric in Conformal Prediction: When Shorter Intervals Are Not Better},
  author  = {Min, Yizhou and Lu, Yizhou and Li, Lanqi and Zhang, Zhen and Teng, Jiaye},
  journal = {arXiv preprint arXiv:2601.21455},
  year    = {2026},
  doi     = {10.48550/arXiv.2601.21455},
  url     = {https://arxiv.org/abs/2601.21455}
}
~~~

## Thank you

Thank you to Yizhou Min, Yizhou Lu, Lanqi Li, Zhen Zhang, and Jiaye Teng for
making the paper and source repository available. The paper's deliberately
counter-intuitive construction is useful as a reproducibility and evaluation
case study, and the clear distinction between coverage, length, and stability
made this audit possible.
