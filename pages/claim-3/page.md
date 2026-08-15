# Claim 3 — Real-world regression benchmarks

## Contract

The paper reports that PT-VCP reduces interval length on 9 of 10 real
regression datasets while maintaining approximately 90% marginal coverage.

## Scoped verdict: PARTIAL_EXTERNAL_DATA_AUDIT

The committed run executes seven obtainable UCI datasets:

- concrete, bio, bike — the three paper datasets available to this run;
- airfoil, energy, wine, and realestate — additional regression diagnostics.

PT-VCP is shorter in all 7/7 runs. PT-VCP coverage ranges from 0.8922 to
0.9047 across the seven aggregate results. The three paper datasets are
included and all have shorter PT-VCP intervals.

This is not a full 9/10 reproduction. The unavailable paper datasets,
checkpoints, and author-supplied summary tables are not substituted for reruns.
The source-supplied Table-3 CSV is checked only as an artifact.

## Protocol and deviations

repro/src/claim3_real_world.py uses five seeds, alpha=0.10, p=0.95, feature
standardization, residual bias, and a 64-64-1 ReLU Adam MLP. For CPU
feasibility, the sklearn MLP uses max_iter=200 with early stopping and large
datasets are capped at 10,000 rows. Dropout is not used. These deviations are
recorded in the output and source manifest.

## Production path

repro/src/real_datasets.py loads the public datasets and records failures.
repro/src/claim3_real_world.py trains the models and writes
outputs/claim3_real_world.json.

~~~bash
uv run python -m repro.src.claim3_real_world
~~~

The command needs network access for dataset retrieval. The committed JSON
artifact is the evidence for the audited run.
