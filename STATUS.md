# Status

## Current step

`publication_queued` — full reproduction and publication gate complete.

## Verified results

- Full source scale: 5 seeds × 4 alpha values × 5 PT probabilities at
  `n=2,000` (100 conditions).
- C1: all 16 nontrivial alpha/p aggregates shorten the observed mean interval;
  maximum aggregated marginal-coverage error is `0.013`.
- C2: all 80 `p < 1` rows emit both singleton and adjusted intervals for the
  same input across runs; VCP is deterministic in all 100 rows.
- C3: the source stability statistic detects all 80 PT rows with zero false
  negatives and has zero false positives on 20 `p=1` controls.
- The clean-room protocol matches the unmodified pinned author execution
  exactly (`max abs difference = 0`); six tests and independent raw-artifact
  verification pass.

## Source discrepancy and scope

The current pinned executable differs from the repository's checked-in
historical synthetic summary (`max abs difference = 20.8029`). This is preserved
in `outputs/full_synthetic_summary.json`, not hidden. The complete released
synthetic protocol is reproduced; unavailable external data/checkpoint studies
are not claimed as rerun evidence.

## Next action

Publish to `DineshAI/r3h23Jv26a` only after the daily Hugging Face Space quota
resets, then verify public tags and artifacts and change the coordination entry
to `under_verdict`.

## Scope

All three live challenge claims are evaluated on the full released synthetic
protocol. The unavailable external dataset/checkpoint experiments are not
substituted or claimed as rerun evidence.
