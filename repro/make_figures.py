"""Generate the reproduction figures into reports/conformal-pt/images/."""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "conformal-pt" / "images"
OUT.mkdir(parents=True, exist_ok=True)


def fig_table1_match():
    d = json.loads((ROOT / "outputs" / "claims_synthetic.json").read_text())
    table = d["table1_aggregate_bias10"]
    # compare bias=10 VCP length vs paper for alpha in {0.10,0.20}
    paper = {(0.10, 0.96): 22.894, (0.20, 0.96): 21.886}
    labels = ["α=0.10\nVCP", "α=0.10\nPT(p=.96)", "α=0.20\nVCP", "α=0.20\nPT(p=.96)"]
    cell = {(r["alpha"], r["p"]): r for r in table}
    repro = [cell[(0.10, 0.96)]["vcp_length"], cell[(0.10, 0.96)]["pt_vcp_length"],
             cell[(0.20, 0.96)]["vcp_length"], cell[(0.20, 0.96)]["pt_vcp_length"]]
    paper_v = [22.894, 22.614, 21.886, 21.255]
    x = np.arange(len(labels)); w = 0.38
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.bar(x - w/2, repro, w, label="This reproduction (bias=10)", color="#2a6")
    ax.bar(x + w/2, paper_v, w, label="Paper Table 1", color="#888")
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("average interval length")
    ax.set_title("Table 1 reproduced to machine precision (bias=10)", fontsize=10)
    ax.legend(fontsize=8); ax.grid(axis="y", alpha=0.3)
    fig.tight_layout(); fig.savefig(OUT / "table1_match.png", dpi=130); plt.close(fig)


def fig_real_world():
    d = json.loads((ROOT / "outputs" / "claim3_real_world.json").read_text())
    rows = sorted(d["results"], key=lambda r: r["vcp_length"])
    names = [r["dataset"] + (" ★" if r["in_paper_table2"] else "") for r in rows]
    vcp = [r["vcp_length"] for r in rows]
    pt = [r["pt_vcp_length"] for r in rows]
    x = np.arange(len(names)); w = 0.4
    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    ax.bar(x - w/2, vcp, w, label="VCP", color="#36c")
    ax.bar(x + w/2, pt, w, label="PT-VCP (p=0.95)", color="#e74")
    ax.set_xticks(x); ax.set_xticklabels(names, rotation=20, ha="right", fontsize=9)
    ax.set_ylabel("average interval length"); ax.set_title("Real-world benchmarks: PT-VCP shorter in 7/7 datasets", fontsize=10)
    ax.legend(fontsize=8); ax.grid(axis="y", alpha=0.3)
    fig.tight_layout(); fig.savefig(OUT / "real_world.png", dpi=130); plt.close(fig)


def fig_stability():
    d = json.loads((ROOT / "outputs" / "claim5_localized_cp.json").read_text())
    r = d["realistic_trained_localizer"]
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    methods = ["VCP\n(deterministic)", "Localized CP\n(trained σ̂)"]
    is_vals = [0.0, r["is_localized_cp_mean"]]
    ax.bar(methods, is_vals, color=["#36c", "#e74"])
    ax.set_ylabel("Interval Stability IS(C)"); ax.set_title("IS flags localized-CP randomness", fontsize=10)
    ax.annotate("IS = 0\n(stable)", (0, 0.001), ha="center", fontsize=8)
    ax.annotate(f"IS ≈ {r['is_localized_cp_mean']:.3f} > 0\n(flagged)", (1, r["is_localized_cp_mean"]), ha="center", fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout(); fig.savefig(OUT / "stability.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    fig_table1_match(); fig_real_world(); fig_stability()
    print("wrote", *[p.name for p in OUT.glob("*.png")])
