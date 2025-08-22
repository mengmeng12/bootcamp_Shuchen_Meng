# Homework 05 — Data Storage

## Folder Structure
- `data/raw/` – first-touch CSV
- `data/processed/` – Parquet (columnar, compressed)
- `notebooks/` – this notebook
- `src/` – utilities for I/O and validation

## Environment
A local `.env` in *this* folder controls where data is written:
```
DATA_DIR_RAW=data/raw
DATA_DIR_PROCESSED=data/processed
```

## How to Run
Execute cells in the notebook. It will:
1) Create folders and `.env`
2) Save the sample DataFrame to CSV & Parquet
3) Reload both and validate shapes/dtypes
4) Use suffix-based utilities `write_df` / `read_df`

## Data Storage (Auto-Generated)

**Folders**
- `data/raw/` – first-touch CSV
- `data/processed/` – Parquet for analytics

**Formats & Why**
- **CSV**: simple, universal; larger on disk, slower for analytics.
- **Parquet**: columnar + compressed (via `pyarrow`); smaller & faster for analytics.  
  If `pyarrow` is missing, code shows a clear install hint.

**Env-Driven Paths**
Values come from `.env` in this folder:
```
DATA_DIR_RAW=data/raw
DATA_DIR_PROCESSED=data/processed
```

**Utilities**
Suffix-routed I/O:
```python
from src.storage.io_utils import write_df, read_df

write_df(df, DATA_DIR_RAW / "table.csv")
write_df(df, DATA_DIR_PROCESSED / "table.parquet")

df_csv = read_df(DATA_DIR_RAW / "table.csv", parse_dates=["date"])
df_parq = read_df(DATA_DIR_PROCESSED / "table.parquet")
```

**Validation**
The notebook prints checks for shape/columns/dtypes using `validate_df`.
