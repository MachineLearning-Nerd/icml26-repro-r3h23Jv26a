# Claim 2 — Table 1 source-artifact audit

## Paper contract

The paper's Table 1 reports, at alpha=0.10, VCP length 22.894 and PT-VCP
length 22.614 for p=0.96. It reports PT-VCP length 22.714 for p=0.98.

## Scoped verdict: PARTIAL_SOURCE_ARTIFACT_AUDIT

The current committed author snapshot uses bias 20. The paper table and the
checked-in historical CSV correspond to bias 10.

| Cell | Paper | Clean-room at bias 10 | Assessment |
|---|---:|---:|---|
| VCP, p=.96 | 22.894 | 22.89381453 | matches to rounding |
| PT-VCP, p=.96 | 22.614 | 22.51439246 | 0.0996 lower; not exact |
| PT-VCP, p=.98 | 22.714 | 22.71439989 | matches to rounding |

The full 32-row bias-10 clean-room layout matches
reference/upstream/table1_source_bias10.csv with maximum absolute difference
7.105427357601002e-15. The bias-20 layout differs from that historical artifact
by 20.802883433998257. Both facts are retained.

## Production path

repro/src/pt_core.py implements the source protocol. The
repro/run_full_source_synthetic.py runner executes the committed author
snapshot in a temporary directory and compares the resulting 100-condition
layout with the clean-room implementation. repro/src/claims_synthetic.py
records the Table-1 cells and drift checks.

~~~bash
uv run python repro/run_full_source_synthetic.py
uv run python -m repro.src.claims_synthetic
~~~

The historical CSV match is strong evidence about the source artifact; it is
not evidence that every printed paper number is reproduced exactly.
