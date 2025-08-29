

NOTE 
This script is part of the Momentum project and depends on the project layout
(data/, reports/checkpoints/, src/). Run it FROM THE PROJECT ROOT, e.g.:

  conda activate bootcamp_env
  python -m src.pipelines.fetch --tickers SPY QQQ EEM AGG --start 2005-01-01

Running it standalone (e.g., copied into a homework folder) will NOT work unless
you recreate the same folders or override paths via --out and --checkpoint.
It also requires internet access for yfinance.

# Orchestration plan

## Pipeline Decomposition

- fetch_data → data/raw/adj_close_daily.csv → Nan → daily/weekly
- prep_monthly→ data/processed/prices_monthly.parquet → fetch_data
- build_features（12–1 & signal）→ data/processed/signals.parquet → prep_monthly
- fit_cov（60m LW COV）→ data/processed/cov_YYYYMM.pkl → prep_monthly
- optimize_weights→ data/processed/weights.parquet → build_features + fit_cov
- backtest（walk-forward/80-20）→ reports/nav.parquet, reports/perf.csv → optimize_weights
- persist_model → model/final_model.pkl → fit_cov
- serve_api（Flask）→ processinh → model/final_model.pkl


## How to run it 
1) conda activate bootcamp_env && pip install -r requirements.txt
2) Fetch data (robust downloader): python -m src.pipelines.fetch --tickers SPY QQQ EEM AGG --start 2005-01-01 --out data/raw/adj_close_daily.csv
3) Launch Jupyter: jupyter lab  (open notebooks/momentum_project.ipynb and Run All)
4) Parameters (tickers, WMAX, costs, lookbacks) are set near the top of the notebook.
5) Model persistence: run section “Model Persistence” to save model/final_model.pkl and test reload.
6) Start API (optional): export FLASK_APP=api/app.py && flask run  # http://127.0.0.1:5000
7) Test API: curl http://127.0.0.1:5000/predict/101  or  POST {"signals":{"SPY":1,"QQQ":0,"EEM":1},"wmax":0.33}
8) Streamlit UI (optional): streamlit run app/streamlit_app.py
9) Check outputs in reports/ (NAV plots, perf table) and logs/checkpoints in reports/checkpoints/.
