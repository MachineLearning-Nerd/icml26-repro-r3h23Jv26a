# Source manifest

## Paper

| Field | Value |
|---|---|
| Title | Questioning the Coverage-Length Metric in Conformal Prediction: When Shorter Intervals Are Not Better |
| Authors | Yizhou Min; Yizhou Lu; Lanqi Li; Zhen Zhang; Jiaye Teng |
| arXiv | https://arxiv.org/abs/2601.21455v2 |
| OpenReview | https://openreview.net/forum?id=r3h23Jv26a |
| Version read | v2, revised 16 June 2026 |
| Audit date | 2026-08-15 |

## Upstream source

| Path | Provenance | Use |
|---|---|---|
| reference/upstream/simulation_subgaussian.py | benben-cd/PT-Conformal-Prediction at 09655d6c58be2a9b24aafb739c37397e0488e933 | Current synthetic author snapshot |
| reference/upstream/table1_source_bias10.csv | checked-in historical source artifact | Bias-10 Table-1 comparison |
| reference/upstream/table3_interval_stability.csv | checked-in historical source artifact | Table-3 artifact-only check |
| reference/upstream/simulation_guassian.py | checked-in source snapshot | Historical Gaussian ablation context |

## Generated evidence

| Producer | Output |
|---|---|
| repro/src/claims_synthetic.py | outputs/claims_synthetic.json |
| repro/run_full_source_synthetic.py | outputs/full_synthetic_summary.json |
| repro/verify_full_synthetic.py | outputs/independent_verification.json |
| repro/src/claim3_real_world.py | outputs/claim3_real_world.json |
| repro/src/claim5_localized_cp.py | outputs/claim5_localized_cp.json |
| repro/src/verify_localized_pt_equivalence.py | outputs/localized_pt_equivalence.json |
| repro/src/audit_localized_pt_equivalence.py | outputs/localized_pt_equivalence_audit.json |

## Input boundaries

- Synthetic inputs are generated from fixed seeds.
- Real-world inputs are public UCI datasets downloaded at execution time.
- No private data, trained author checkpoints, or author repository clone is
  committed.
- The source-supplied CSVs are not represented as fresh reruns.

## Thank-you note

The audit thanks Yizhou Min, Yizhou Lu, Lanqi Li, Zhen Zhang, and Jiaye Teng
for releasing the paper and source materials. Their PT construction provides a
useful, concrete test of whether coverage and average length are sufficient
to characterize a prediction interval.
