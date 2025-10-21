# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

app = Flask(__name__)
CORS(app)

# constants
MODEL_PATH = os.path.join("model", "DL_MINI_PROJECT.h5")
TIMESTEPS = 100   # change to match how you trained the model

# Load model once at startup
model = load_model(MODEL_PATH)

# We'll create new scaler each request to match training scale on Close column
@app.route('/')
def index():
    return jsonify({"message": "Stock prediction API up"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        payload = request.get_json(force=True)
        ticker = payload.get("ticker")
        if not ticker:
            return jsonify({"error": "Provide 'ticker' in JSON body"}), 400

        # fetch recent data (ensure you have at least TIMESTEPS + 1 rows)
        df = yf.download(ticker, period="200d", interval="1d")
        if df.empty or len(df) < TIMESTEPS:
            return jsonify({"error": f"Not enough data for {ticker}"}), 404

        close = df['Close'].values.reshape(-1, 1)

        # scale
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled = scaler.fit_transform(close)

        # build input: last TIMESTEPS
        X = np.array([scaled[-TIMESTEPS:]])
        # if model expects shape (1, TIMESTEPS, features) this matches

        y_pred_scaled = model.predict(X)
        y_pred = scaler.inverse_transform(y_pred_scaled)[0][0]

        response = {
            "ticker": ticker,
            "predicted_price": round(float(y_pred), 2),
            "last_price": round(float(close[-1][0]), 2)
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # For development only; use gunicorn in production
    app.run(host="0.0.0.0", port=5000, debug=True)
