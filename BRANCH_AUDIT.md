# Branch audit

## Final branch policy

- main is the only publication branch.
- Evidence branches retain the three claim-focused snapshots with descriptive
  names.
- No branch named or prefixed orx remains in the final remote state.
- Evidence branches are historical experiment snapshots, not additional
  publication defaults.

## Mapping

| Final name | Original name | Original tip before audit | Scope |
|---|---|---|---|
| main | main | f077370941db005f1b3ee8dc3ab4950092b084e9 | Combined publication surface |
| evidence/synthetic-claims-1-2-4 | orx/baseline-synthetic-reproduction-claims-1-2-4 | 611500f56c8007115bc305b119ddaf88b6f2286c | Claims 1, 2, and 4 synthetic |
| evidence/claim-3-real-world | orx/claim-3-real-world-regression-benchmarks-table-2 | 272093b0c83ff479a38e102be817040169b8c2e2 | Claim 3 real-world regressions |
| evidence/claim-5-localized-cp | orx/claim-5-localized-cp-interval-stability-detectio | b3d9838c83b0d27b6f3c7ec3acde5f14a65f87e9 | Claim 5 localized CP and IS |

The branch links in README.md use the final names. The original names are
recorded here so the provenance of each experiment remains inspectable.

## Tips at branch rename

These immutable tip IDs were recorded immediately after the branch rename.
The main branch later received documentation-only commits; the evidence
branches remain at the listed tips.

| Final branch | Published tip |
|---|---|
| main | 1870d005e6ee7e52d59a9ddca2688f0a14367c58 |
| evidence/synthetic-claims-1-2-4 | 362422b0adcc5986a9c82b0a5822f70a9a0c74b7 |
| evidence/claim-3-real-world | 036fe96e5e26aaee6264d9f5509658a39c481e0d |
| evidence/claim-5-localized-cp | 64a4a75aad0695fcf2cccecfeca4c4652b010a96 |

## Branch contents

- main contains the combined source, outputs, report, scope ledger, citation,
  provenance manifest, and final verifier.
- evidence/synthetic-claims-1-2-4 contains the pinned synthetic environment,
  clean-room protocol, and independent synthetic checks.
- evidence/claim-3-real-world contains the cumulative real-world benchmark
  producer and its output.
- evidence/claim-5-localized-cp contains the localized-CP producer and its
  constructive equivalence page.
