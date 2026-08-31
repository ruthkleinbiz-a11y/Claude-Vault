"""Reads manually exported CSVs for Medium and Substack."""

import glob
import os
from datetime import datetime

import pandas as pd


IMPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "manual-imports")


def _latest_file(pattern: str) -> str | None:
    files = glob.glob(os.path.join(IMPORT_DIR, pattern))
    return max(files, key=os.path.getmtime) if files else None


def fetch_medium(metrics: list[str]) -> dict:
    path = _latest_file("medium_stats_*.csv")
    if not path:
        return {"data": None, "error": "No Medium CSV found in manual-imports/. Export from medium.com/me/stats and drop it there."}
    try:
        df = pd.read_csv(path)
        totals = {col: int(df[col].sum()) for col in metrics if col in df.columns}
        totals["_source_file"] = os.path.basename(path)
        totals["_imported_at"] = datetime.utcnow().isoformat()
        return {"data": totals, "error": None}
    except Exception as exc:
        return {"data": None, "error": str(exc)}


def fetch_substack(metrics: list[str]) -> dict:
    path = _latest_file("substack_*.csv")
    if not path:
        return {"data": None, "error": "No Substack CSV found in manual-imports/. Export from your Substack dashboard > Settings > Exports."}
    try:
        df = pd.read_csv(path)
        totals = {}
        for col in metrics:
            if col not in df.columns:
                continue
            # Rates are averaged, counts are summed
            if "rate" in col or "ratio" in col:
                totals[col] = round(float(df[col].mean()), 4)
            else:
                totals[col] = int(df[col].sum())
        totals["_source_file"] = os.path.basename(path)
        totals["_imported_at"] = datetime.utcnow().isoformat()
        return {"data": totals, "error": None}
    except Exception as exc:
        return {"data": None, "error": str(exc)}
