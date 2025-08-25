from typing import Dict, Tuple, Optional
import pandas as pd

def validate_df(original: pd.DataFrame, reloaded: pd.DataFrame, expected_dtypes: Optional[Dict[str, str]] = None):
    """Return dict: check_name -> (ok: bool, message: str)."""
    results = {}
    # shape
    same_shape = original.shape == reloaded.shape
    results["shape_match"] = (same_shape, f"original={original.shape}, reloaded={reloaded.shape}")
    # columns (order-sensitive for this HW)
    same_cols = list(original.columns) == list(reloaded.columns)
    results["columns_match_order"] = (same_cols, f"original={list(original.columns)}, reloaded={list(reloaded.columns)}")
    # dtype checks (allow CSV to degrade 'category' -> 'object'/'string')
    if expected_dtypes:
        dtype_ok = True
        msgs = []
        for col, exp in expected_dtypes.items():
            if col not in reloaded.columns:
                dtype_ok = False
                msgs.append(f"{col}: MISSING")
                continue
            got = str(reloaded[col].dtype)
            if exp == "category" and got in ("category","object","string"):
                msgs.append(f"{col}: OK (got {got}, expected {exp} acceptable)")
            elif got != exp:
                dtype_ok = False
                msgs.append(f"{col}: got {got}, expected {exp}")
            else:
                msgs.append(f"{col}: OK ({got})")
        results["dtypes_expected"] = (dtype_ok, "; ".join(msgs))
    return results
