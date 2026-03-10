// lovable_fetch_example.js
async function getPrediction(featureDict) {
  const resp = await fetch("http://localhost:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ features: featureDict })
  });
  const data = await resp.json();
  if (!resp.ok) {
    console.error("Prediction error", data);
    return null;
  }
  return data; // { prediction: "...", probability: 0.85 }
}

// Example usage:
const sample = { sepal_length: 5.1, sepal_width: 3.5, petal_length: 1.4, petal_width: 0.2 };
getPrediction(sample).then(console.log);
