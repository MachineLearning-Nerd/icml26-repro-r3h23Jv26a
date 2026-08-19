# Environment and execution boundary

- Python: 3.12, with dependencies pinned by `uv.lock`.
- Execution: CPU-only for the committed audit surface.
- Synthetic evidence: fixed seeds and committed source snapshots.
- Real-world evidence: seven obtainable UCI datasets, with network-backed loading during the historical run; unavailable datasets and author checkpoints are not vendored.
- Final verification: `python3 verify_final.py` checks committed JSON, branch names, commit identities, hashes, and the inner verifier without rerunning the expensive suite.

The committed evidence is the source of truth for this dossier. A clean final-state check must not
be described as a rerun of the full paper experiment suite.
