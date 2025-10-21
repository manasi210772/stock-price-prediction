import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [ticker, setTicker] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    if (!ticker) {
      alert("Please enter a company ticker!");
      return;
    }
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", { ticker });
      setResult(response.data);
    } catch (error) {
      alert("Error fetching prediction! Make sure Flask backend is running.");
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>📈 Stock Price Predictor</h1>
      <input
        type="text"
        placeholder="Enter company ticker (e.g., AAPL, RELIANCE.NS)"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
      />
      <button onClick={handlePredict}>Predict</button>

      {loading && <p>Loading prediction...</p>}

      {result && (
        <div className="result">
          <h3>{result.ticker}</h3>
          <p><strong>Last Price:</strong> ${result.last_price}</p>
          <p><strong>Predicted Price:</strong> ${result.predicted_price}</p>
        </div>
      )}
    </div>
  );
}

export default App;
