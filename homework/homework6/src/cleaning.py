from __future__ import annotations
from typing import Iterable, Optional, Tuple, Dict
import pandas as pd
import numpy as np

__all__ = ["fill_missing_median","drop_missing","normalize_data"]

def _ensure_columns(df: pd.DataFrame, columns: Optional[Iterable[str]]) -> list[str]:
    if columns is None:
        return list(df.columns)
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise KeyError(f"Columns not in DataFrame: {missing}")
    return list(columns)

def fill_missing_median(df: pd.DataFrame, columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """Fill NaNs using the median of each column. If columns=None, apply to numeric columns only."""
    out = df.copy()
    cols = out.select_dtypes(include=[np.number]).columns.tolist() if columns is None else _ensure_columns(out, columns)
    for c in cols:
        out[c] = out[c].fillna(out[c].median(skipna=True))
    return out

def drop_missing(
    df: pd.DataFrame,
    how: str = "any",
    subset: Optional[Iterable[str]] = None,
    thresh: Optional[int] = None,
) -> pd.DataFrame:
    """
    Drop rows with missing values.
    NOTE: Pandas does not allow setting both `how` and `thresh` at once.
    We therefore pass **either** `how` or `thresh`, not both.
    """
    kwargs = {}
    if subset is not None:
        kwargs["subset"] = subset
    if thresh is not None:
        # Use threshold of non-NA values; do NOT pass `how` concurrently
        kwargs["thresh"] = thresh
    else:
        # No threshold provided -> use how ("any" or "all")
        kwargs["how"] = how
        return df.dropna(axis=0, **kwargs)
    

def normalize_data(df: pd.DataFrame, columns: Optional[Iterable[str]] = None, method: str = "zscore"
) -> Tuple[pd.DataFrame, Dict[str, Tuple[float, float]]]:
    """Normalize numeric columns with z-score or min-max. Returns (normalized_df, params)."""
    out = df.copy()
    cols = out.select_dtypes(include=[np.number]).columns.tolist() if columns is None else _ensure_columns(out, columns)
    params: Dict[str, Tuple[float, float]] = {}
    if method not in {"zscore", "minmax"}:
        raise ValueError("method must be 'zscore' or 'minmax'")
    for c in cols:
        s = out[c].astype(float)
        if method == "zscore":
            mu, sigma = s.mean(), s.std(ddof=0)
            sigma = sigma if sigma != 0 else 1.0
            out[c] = (s - mu) / sigma
            params[c] = (float(mu), float(sigma))
        else:
            mn, mx = s.min(), s.max()
            rng = (mx - mn) if (mx - mn) != 0 else 1.0
            out[c] = (s - mn) / rng
            params[c] = (float(mn), float(mx))
    return out, params