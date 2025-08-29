# Stage 13 Productization

**Data**: Randomly generated for learning API/model workflow; the same pattern will be applied to the real project.

## How to Run (Fresh Environment)
```bash
conda create -n bootcamp_env python=3.10 -y
conda activate bootcamp_env
pip install -r requirements.txt
python app.py   # Running on http://127.0.0.1:5000
```

## API Usage
```bash
curl http://127.0.0.1:5000/ping
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"features":[0.1,0.2]}'
curl http://127.0.0.1:5000/predict/0.1
curl http://127.0.0.1:5000/predict/0.1/0.2
```

## Assumptions & Risks
- Random data; numbers are illustrative only.
- In real project, ensure feature scaling, data validation, and model monitoring.

## Dashboard (Optional)
```bash
streamlit run app_streamlit.py
```
Then input features and the app will call your local Flask API.

## Files
- `model/model.pkl` — pickled demo model
- `app.py` — Flask API with error handling
- `requirements.txt` — minimal reproducible env
- `reports/api_test_log.txt` — test evidence from this notebook
- `app_streamlit.py` — optional Streamlit dashboard
