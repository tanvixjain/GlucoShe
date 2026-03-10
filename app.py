# app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import joblib
import io
import json

app = Flask(__name__)
CORS(app)

MODEL_PATH = "rf_model.joblib"

# In-memory storage for last metrics / column order
model = None
last_metrics = {}
feature_columns = []

def train_from_dataframe(df, target_col, test_size=0.2, random_state=42):
    global model, last_metrics, feature_columns
    # Basic preprocessing: drop rows with NA, separate X/y
    df = df.dropna().reset_index(drop=True)
    if target_col not in df.columns:
        raise ValueError(f"target_col '{target_col}' not found in dataframe")
    X = df.drop(columns=[target_col])
    y = df[target_col]
    feature_columns = X.columns.tolist()

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y if len(np.unique(y))>1 else None
    )

    rf = RandomForestClassifier(n_estimators=100, random_state=random_state)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    # If binary classification, get probability for class 1; else return probabilities for first class
    try:
        y_proba = rf.predict_proba(X_test)[:, 1] if rf.n_classes_ == 2 else rf.predict_proba(X_test)[:, 0]
    except Exception:
        # fallback if predict_proba not available or single-class
        y_proba = np.zeros_like(y_test)

    # Store metrics
    cls_report = classification_report(y_test, y_pred, output_dict=True)
    roc = None
    try:
        roc = roc_auc_score(y_test, y_proba)
    except Exception:
        roc = None

    last_metrics = {
        "classification_report": cls_report,
        "roc_auc": roc,
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
    }

    model = rf
    joblib.dump({"model": model, "features": feature_columns}, MODEL_PATH)
    return last_metrics

@app.route("/train", methods=["POST"])
def train():
    """
    Accepts multipart/form-data with a CSV file (key: file) OR
    JSON body { "csv_text": "<csv string>", "target_col": "label" }
    Returns computed metrics JSON.
    """
    try:
        if "file" in request.files:
            file = request.files["file"]
            df = pd.read_csv(file)
            target_col = request.form.get("target_col")
        else:
            payload = request.get_json(force=True)
            csv_text = payload.get("csv_text")
            target_col = payload.get("target_col")
            if not csv_text:
                return jsonify({"error": "no csv_text provided"}), 400
            df = pd.read_csv(io.StringIO(csv_text))

        if not target_col:
            return jsonify({"error": "target_col not provided"}), 400

        metrics = train_from_dataframe(df, target_col)
        return jsonify({"status": "trained", "metrics": metrics})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict", methods=["POST"])
def predict():
    """
    Accepts JSON: {"features": {"col1": value1, "col2": value2, ...}}
    Returns: {"prediction": <label>, "probability": <prob>}
    """
    global model, feature_columns
    try:
        if model is None:
            # try to load model from disk
            data = joblib.load(MODEL_PATH)
            model = data["model"]
            feature_columns = data.get("features", [])

        payload = request.get_json(force=True)
        features = payload.get("features")
        if not features:
            return jsonify({"error": "no features provided"}), 400

        # Build DataFrame in the proper column order
        x = pd.DataFrame([features], columns=feature_columns)
        pred = model.predict(x)[0]
        proba = None
        try:
            proba = float(model.predict_proba(x)[0, 1]) if model.n_classes_ == 2 else float(np.max(model.predict_proba(x)))
        except Exception:
            proba = None

        return jsonify({"prediction": str(pred), "probability": proba})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/feature_importance", methods=["GET"])
def feature_importance():
    global model, feature_columns
    try:
        if model is None:
            data = joblib.load(MODEL_PATH)
            model = data["model"]
            feature_columns = data.get("features", [])
        importances = dict(zip(feature_columns, model.feature_importances_.tolist()))
        # return sorted by importance desc
        sorted_items = sorted(importances.items(), key=lambda t: t[1], reverse=True)
        return jsonify({"feature_importances": sorted_items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/metrics", methods=["GET"])
def metrics():
    global last_metrics
    return jsonify(last_metrics or {"message": "no metrics yet"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

