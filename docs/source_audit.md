# Source and provenance audit

## Primary paper

- Title: *Questioning the Coverage-Length Metric in Conformal Prediction:
  When Shorter Intervals Are Not Better*
- Authors: Yizhou Min, Yizhou Lu, Lanqi Li, Zhen Zhang, and Jiaye Teng.
- arXiv: [2601.21455v2](https://arxiv.org/abs/2601.21455v2), revised 16 June
  2026.
- OpenReview: [r3h23Jv26a](https://openreview.net/forum?id=r3h23Jv26a).
- Full primary HTML: [arxiv.org/html/2601.21455](https://arxiv.org/html/2601.21455).

The paper defines PT as a randomized construction that returns a null or
minimal set on one branch and an adjusted conformal set on the other branch.
The adjustment preserves marginal coverage in expectation while potentially
reducing average length. The paper introduces Interval Stability to expose
run-to-run variation for the same input.

## Author source

- Repository: benben-cd/PT-Conformal-Prediction.
- Pinned source commit:
  09655d6c58be2a9b24aafb739c37397e0488e933.
- Referenced source file:
  ordinary_regression_task/simulation_subgaussian.py.
- Committed local snapshots:
  reference/upstream/simulation_subgaussian.py,
  reference/upstream/simulation_guassian.py,
  reference/upstream/table1_source_bias10.csv, and
  reference/upstream/table3_interval_stability.csv.

The clean-room implementation in repro/src/pt_core.py uses the same five-seed,
n=2,000, 80/20 split, four alpha, and five p-value protocol. The full-source
runner executes the committed author script in a temporary directory, so the
audit does not depend on an uncommitted checkout.

## Source-artifact drift

The current committed author snapshot sets bias to 20. The historical Table-1
CSV corresponds to bias 10. The clean-room/current-source maximum absolute
difference is 0.0. The bias-20 output differs from the historical Table-1 CSV
by 20.802883433998257. Running the same protocol at bias 10 matches the
historical CSV to 7.105427357601002e-15.

The paper's Table 1 reports 22.614 for PT-VCP at alpha 0.10 and p 0.96. The
committed protocol produces 22.514392464628397 for that cell and
22.714399886459027 at p 0.98, matching the paper's 22.714 cell. This is
reported as a discrepancy, not normalized away.

## Data and external inputs

- Synthetic data are generated deterministically by the committed producers.
- The real-data producer downloads obtainable UCI datasets at execution time.
- Six paper datasets and their trained checkpoints were not reliably available
  to this audit and are not represented by substitute reruns.
- The author-supplied Table-3 CSV is checked as a source artifact only.
- No author repository is vendored as a dependency and no author endorsement is
  implied.

## Audit date

The repository audit and primary-source reading were performed on 15 August
2026.
