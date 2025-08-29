# src/pipelines/fetch.py
import argparse, logging, sys, json, os
from pathlib import Path
import pandas as pd, yfinance as yf
from datetime import datetime as dt

def download_adj_close(tickers, start, end=None):
    tickers = list(dict.fromkeys(tickers))
    df = yf.download(tickers, start=start, end=end, interval="1d",
                     auto_adjust=True, actions=False, group_by="ticker",
                     threads=False, progress=False)
    out = pd.DataFrame()
    if isinstance(df.columns, pd.MultiIndex):
        cols = {}
        for t in tickers:
            sub = df.get(t)
            if sub is not None and not sub.empty:
                if "Close" in sub.columns: cols[t] = sub["Close"]
                elif "close" in sub.columns: cols[t] = sub["close"]
        if cols: out = pd.DataFrame(cols)
    else:
        if "Close" in df.columns: out = df[["Close"]].rename(columns={"Close": tickers[0]})
        elif "close" in df.columns: out = df[["close"]].rename(columns={"close": tickers[0]})
    # fallback: per-ticker
    if out.empty or any(t not in out.columns for t in tickers):
        frames = []
        for t in tickers:
            x = yf.download(t, start=start, end=end, interval="1d",
                            auto_adjust=True, actions=False, progress=False, threads=False)
            if not x.empty:
                col = "Close" if "Close" in x.columns else ("close" if "close" in x.columns else None)
                if col: frames.append(x[col].rename(t))
        if frames: out = pd.concat(frames, axis=1)
    out.index = pd.to_datetime(out.index, errors="coerce")
    out = out[~out.index.isna()].sort_index().ffill().bfill()
    return out

def main():
    p = argparse.ArgumentParser("fetch_data")
    p.add_argument("--tickers", nargs="+", required=True)
    p.add_argument("--start", required=True)
    p.add_argument("--end", default=None)
    p.add_argument("--out", default="data/raw/adj_close_daily.csv")
    p.add_argument("--checkpoint", default="reports/checkpoints/fetch.json")
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    out = Path(args.out); ckpt = Path(args.checkpoint)
    out.parent.mkdir(parents=True, exist_ok=True); ckpt.parent.mkdir(parents=True, exist_ok=True)

    if out.exists() and ckpt.exists() and not args.force:
        logging.info("Output exists and --force not set; skipping.")
        return 0

    logging.info("Downloading: %s from %s to %s", args.tickers, args.start, args.end or "today")
    df = download_adj_close(args.tickers, args.start, args.end)
    if df.empty:
        logging.error("No data downloaded."); return 2

    df.to_csv(out)
    meta = {
        "tickers": args.tickers, "start": args.start, "end": args.end,
        "rows": int(df.shape[0]), "cols": int(df.shape[1]),
        "out": str(out), "timestamp": dt.utcnow().isoformat()+"Z"
    }
    ckpt.write_text(json.dumps(meta, indent=2))
    logging.info("Wrote %s (%d rows, %d cols)", out, df.shape[0], df.shape[1])
    logging.info("Checkpoint -> %s", ckpt)
    return 0

if __name__ == "__main__":
    sys.exit(main())
