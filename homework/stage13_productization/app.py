
from flask import Flask, request, jsonify, render_template_string
import joblib, io, base64
import matplotlib
matplotlib.use("Agg")  # non-GUI backend for servers
import matplotlib.pyplot as plt

# Load model (will raise early if missing)
try:
    model = joblib.load("model/model.pkl")
    model_loaded = True
    load_err = None
except Exception as e:
    model = None
    model_loaded = False
    load_err = str(e)

app = Flask(__name__)

def predict_core(features):
    if model is None:
        raise RuntimeError(f"model not loaded: {load_err}")
    return float(model.predict([features])[0])

@app.get("/ping")
def ping():
    return jsonify({"ok": True, "model_loaded": model_loaded, "load_err": load_err})

@app.post("/predict")
def predict_post():
    data = request.get_json(silent=True, force=True)
    if not data or "features" not in data:
        return jsonify({"error": "JSON body must include 'features' list"}), 400
    feats = data["features"]
    if not isinstance(feats, (list, tuple)) or not len(feats):
        return jsonify({"error": "'features' must be a non-empty list"}), 400
    try:
        feats = [float(x) for x in feats]
    except Exception:
        return jsonify({"error": "'features' must be numeric"}), 400
    try:
        pred = predict_core(feats)
        return jsonify({"prediction": pred})
    except Exception as e:
        return jsonify({"error": f"prediction failed: {e}"}), 500

@app.get("/predict/<float:input1>")
def predict_get_single(input1):
    try:
        pred = predict_core([float(input1)])
        return jsonify({"prediction": pred})
    except Exception as e:
        return jsonify({"error": f"prediction failed: {e}"}), 500

@app.get("/predict/<float:input1>/<float:input2>")
def predict_get_double(input1, input2):
    try:
        pred = predict_core([float(input1), float(input2)])
        return jsonify({"prediction": pred})
    except Exception as e:
        return jsonify({"error": f"prediction failed: {e}"}), 500

@app.get("/plot")
def plot_page():
    fig, ax = plt.subplots()
    ax.plot([0,1,2,3], [10,20,15,30])
    ax.set_title("Demo Plot")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img64 = base64.b64encode(buf.read()).decode("utf-8")
    html = f"<html><body><h1>Model Output Plot</h1><img src='data:image/png;base64,{img64}'></body></html>"
    return render_template_string(html)

if __name__ == "__main__":
    # Keep 5000 to match original client code
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
