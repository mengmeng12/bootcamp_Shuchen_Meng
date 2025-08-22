from __future__ import annotations
from pathlib import Path
from typing import Optional, Sequence
import pandas as pd

def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def write_df(df: pd.DataFrame, path: Path, index: bool = False) -> None:
    """Write by suffix (.csv / .parquet). Creates parent dirs. Clear error if parquet engine missing."""
    _ensure_parent(path)
    suf = path.suffix.lower()
    if suf == ".csv":
        df.to_csv(path, index=index)
    elif suf == ".parquet":
        try:
            df.to_parquet(path, index=index)  # auto-detect engine; prefers pyarrow
        except Exception as e:
            raise RuntimeError(
                "Failed to write Parquet. Install a Parquet engine, e.g. `pip install pyarrow`\n"
                f"Original error: {e}"
            ) from e
    else:
        raise ValueError(f"Unsupported suffix: {suf}. Use .csv or .parquet.")

def read_df(path: Path, parse_dates: Optional[Sequence[str]] = None) -> pd.DataFrame:
    """Read by suffix (.csv / .parquet)."""
    suf = path.suffix.lower()
    if suf == ".csv":
        return pd.read_csv(path, parse_dates=list(parse_dates) if parse_dates else None)
    elif suf == ".parquet":
        try:
            return pd.read_parquet(path)
        except Exception as e:
            raise RuntimeError(
                "Failed to read Parquet. Install `pyarrow`.\n"
                f"Original error: {e}"
            ) from e
    else:
        raise ValueError(f"Unsupported suffix: {suf}. Use .csv or .parquet.")
