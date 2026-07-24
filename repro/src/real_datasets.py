"""Robust loaders for the real-world regression benchmarks.

Sources are tried in order; the first that works wins. All loaders return a
tuple ``(X, y)`` of float numpy arrays (features, 1-D regression target).

Datasets
--------
Paper Table-2 datasets (obtained from UCI):
  * ``concrete``  -- UCI id 165 (Concrete Compressive Strength)
  * ``bio``       -- UCI id 265 static (Physicochemical / CAS RMSD)
  * ``bike``      -- UCI id 275 (Bike Sharing, hourly count target)

Additional real UCI regression datasets (to test the "9/10" generalization of
the PT length-reduction claim beyond the paper's exact set):
  * ``airfoil``   -- UCI id 291 (Airfoil Self-Noise)
  * ``energy``    -- UCI id 242 (Energy Efficiency, heating load)
  * ``wine``      -- UCI id 186 (Wine Quality, red)
  * ``realestate``-- UCI id 477 (Real estate valuation)
  * ``aquatic``   -- UCI id 772 (Toxicity, LC50)

The paper's MEPS, BLOG-DATA and FACEBOOK-1/2 datasets were not reliably
obtainable from public sources during this reproduction (UCI static + API +
OpenML all failed to serve them); this is documented as a deviation.
"""

from __future__ import annotations

import io
import urllib.request
import zipfile

import numpy as np
import pandas as pd

_UA = {"User-Agent": "Mozilla/5.0 (repro)"}


def _fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=_UA)
    return urllib.request.urlopen(req, timeout=90).read()


def _fetch_zip(url: str) -> zipfile.ZipFile:
    return zipfile.ZipFile(io.BytesIO(_fetch(url)))


def _from_ucimlrepo(dataset_id: int) -> tuple[np.ndarray, np.ndarray]:
    from ucimlrepo import fetch_ucirepo
    d = fetch_ucirepo(id=dataset_id)
    X = np.asarray(d.data.features, dtype=float)
    y = np.asarray(d.data.targets, dtype=float).reshape(-1)
    return X, y


def _drop_nonnumeric(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=object)
    mask_cols = []
    for j in range(X.shape[1]):
        col = X[:, j]
        try:
            np.asarray(col, dtype=float)
            mask_cols.append(j)
        except (ValueError, TypeError):
            mask_cols.append(j) if np.all([isinstance(v, (int, float, np.floating)) or (isinstance(v, str) and _is_num(v)) for v in col[:50]]) else None
    if not mask_cols:
        mask_cols = list(range(X.shape[1]))
    return np.asarray(X[:, mask_cols], dtype=float)


def _is_num(v) -> bool:
    try:
        float(v); return True
    except (ValueError, TypeError):
        return False


def load_concrete() -> tuple[np.ndarray, np.ndarray]:
    return _from_ucimlrepo(165)


def load_bio() -> tuple[np.ndarray, np.ndarray]:
    # CASP.csv: col 0 = RMSD (target), cols 1.. = features
    try:
        z = _fetch_zip("https://archive.ics.uci.edu/static/public/265/physicochemical+properties+of+protein+tertiary+structure.zip")
        csv_bytes = z.read("CASP.csv")
        df = pd.read_csv(io.BytesIO(csv_bytes))
        y = df.iloc[:, 0].values.astype(float)
        X = df.iloc[:, 1:].values.astype(float)
        return X, y
    except Exception:
        return _from_ucimlrepo(265)


def load_bike() -> tuple[np.ndarray, np.ndarray]:
    # UCI hour.csv: drop non-numeric/casual/registered; target = cnt
    z = _fetch_zip("https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip")
    csv_bytes = z.read("hour.csv")
    df = pd.read_csv(io.BytesIO(csv_bytes))
    y = df["cnt"].values.astype(float)
    drop = {"dteday", "cnt", "casual", "registered"}
    Xdf = df.drop(columns=[c for c in drop if c in df.columns])
    # one-hot the small categorical columns season/weathersit already numeric
    X = Xdf.select_dtypes(include=[np.number]).values.astype(float)
    return X, y


def load_airfoil() -> tuple[np.ndarray, np.ndarray]:
    return _from_ucimlrepo(291)


def load_energy() -> tuple[np.ndarray, np.ndarray]:
    X, y = _from_ucimlrepo(242)
    if y.ndim > 1 and y.shape[1] > 1:
        y = y[:, 0]  # heating load (first target)
    return X, y


def load_wine() -> tuple[np.ndarray, np.ndarray]:
    return _from_ucimlrepo(186)


def load_realestate() -> tuple[np.ndarray, np.ndarray]:
    return _from_ucimlrepo(477)


def load_seoulbike() -> tuple[np.ndarray, np.ndarray]:
    return _from_ucimlrepo(560)


# name -> (loader, paper_table2_bias, in_paper_table2)
DATASETS = {
    "concrete": (load_concrete, 5, True),
    "bio": (load_bio, 10, True),
    "bike": (load_bike, 10, True),
    "airfoil": (load_airfoil, 10, False),
    "energy": (load_energy, 10, False),
    "wine": (load_wine, 10, False),
    "realestate": (load_realestate, 10, False),
    "seoulbike": (load_seoulbike, 10, False),
}


def load_all() -> dict[str, dict]:
    out = {}
    for name, (loader, bias, in_paper) in DATASETS.items():
        try:
            X, y = loader()
            X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
            y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)
            out[name] = {"X": X, "y": y, "bias": bias, "in_paper_table2": in_paper, "status": "ok"}
        except Exception as exc:  # noqa: BLE001
            out[name] = {"status": f"failed: {type(exc).__name__}: {str(exc)[:120]}", "in_paper_table2": in_paper, "bias": bias}
    return out
