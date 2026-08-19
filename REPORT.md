# Scoped reproduction report

## Final verdict

| Claim | Verdict | Meaning |
| --- | --- | --- |
| C1 | `VERIFIED_SCOPED` | The finite synthetic PT protocol has 16/16 nontrivial shorter conditions and maximum aggregate coverage error 0.013. |
| C2 | `PARTIAL_SOURCE_ARTIFACT_AUDIT` | The current author snapshot and bias-10 historical CSV match within numerical precision, but the paper's p=0.96 PT value is not exact. |
| C3 | `PARTIAL_EXTERNAL_DATA_AUDIT` | Seven obtainable UCI datasets ran and were shorter; unavailable datasets and checkpoints were not substituted. |
| C4 | `VERIFIED_SCOPED` | PT instability and deterministic p=1 controls pass the independent synthetic checks. |
| C5 | `VERIFIED_SCOPED` | The constructive localized-CP extreme case has 1,500,000 retrainings and zero samplewise mismatches; the trained localizer remains simulation-scoped. |
| C6 | `SIMULATION_CHECK_SCOPED` | The trained localizer diagnostic is recorded, but it is not a universal instability or cherry-pick claim. |

Overall status is `PARTIAL_REPRODUCTION`; `publication_allowed` is `false` for a complete
paper-level reproduction, theorem proof, or external score. The labels describe the finite
evidence that is actually committed.

## Claim production and evidence boundary

The authoritative claim paths are in [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md). Producers write
durable JSON under `outputs/`: synthetic PT rows and controls come from
`repro/src/claims_synthetic.py`, source/Table-1 comparison from
`repro/run_full_source_synthetic.py`, real-world regressions from
`repro/src/claim3_real_world.py`, and localized-CP checks from
`repro/src/verify_localized_pt_equivalence.py` and
`repro/src/claim5_localized_cp.py`.

The committed author snapshot is not silently treated as a full rerun: bias-20 drift and the
paper's p=0.96 discrepancy remain recorded. The seven-dataset real-world run is bounded by
available public data and the documented 10,000-row/200-epoch protocol. No theorem proof,
complete dataset/checkpoint suite, classification result, or author endorsement is claimed.

## Branch and publication policy

`main` is the publication surface. The three `evidence/*` branches preserve synthetic, real-world,
and localized-CP experiment snapshots and are documented in [BRANCH_AUDIT.md](BRANCH_AUDIT.md).
The top-level [verify_final.py](verify_final.py) checks the exact four-branch public set, canonical
MachineLearning-Nerd attribution, the shared claim records, evidence hashes, and the inner
artifact verifier without rerunning the expensive suite.

Thank you to Yizhou Min, Yizhou Lu, Lanqi Li, Zhen Zhang, and Jiaye Teng for releasing the paper
and source materials; [AUTHOR_THANK_YOU.md](AUTHOR_THANK_YOU.md) records the acknowledgement.
