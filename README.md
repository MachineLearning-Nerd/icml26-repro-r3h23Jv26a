# PT-Conformal metric reproduction

Reproduction of `r3h23Jv26a`, *Questioning the Coverage-Length Metric in
Conformal Prediction: When Shorter Intervals Are Not Better*.

This artifact executes the entire released Table-1 synthetic protocol from
the pinned author code (100 conditions: 5 seeds × 4 coverages × 5 PT
probabilities, each with `n=2,000`) and independently rechecks all three
challenge claims:

1. PT can lower average interval length while preserving marginal coverage.
2. PT gives the same input two interval outcomes across repeated runs.
3. The proposed stability statistic detects the randomized shortcut, while
   the `p=1` no-PT control is not flagged.

Run from this directory:

```bash
git clone https://github.com/benben-cd/PT-Conformal-Prediction.git upstream
git -C upstream checkout 09655d6c58be2a9b24aafb739c37397e0488e933
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements-repro.txt
python repro/run_full_source_synthetic.py --output outputs/full_synthetic_summary.json
python repro/verify_full_synthetic.py --input outputs/full_synthetic_summary.json
pytest -q
```

`docs/source_audit.md` describes the pinned source, exact scope, and the
source-artifact drift check. The artifact does not claim to rerun real-data or
ImageNet experiments whose inputs/checkpoints were not released.
