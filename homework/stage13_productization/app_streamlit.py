
import streamlit as st
import requests

st.title("Model Prediction Dashboard")
st.caption("Calls local Flask API at http://127.0.0.1:5000")

f1 = st.number_input("Feature 1", value=0.1)
f2 = st.number_input("Feature 2", value=0.2)

if st.button("Predict"):
    try:
        r = requests.post("http://127.0.0.1:5000/predict",
                          json={"features":[f1, f2]}, timeout=5)
        if r.ok and "application/json" in (r.headers.get("content-type") or "").lower():
            st.success(r.json())
        else:
            st.error(f"Bad response: {r.status_code} {r.text[:200]}")
    except Exception as e:
        st.error(f"Request failed: {e}")
