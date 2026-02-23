import pickle
import pandas as pd

model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))


# New water sample (change values to test)

new_sample = pd.DataFrame([{
    "ph": 7.1,
    "tds": 210,
    "turbidity": 2.2,
    "temperature": 27
}])


# Scale input

scaled_sample = scaler.transform(new_sample)

#
# Get prediction and score
# -----------------------------
prediction = model.predict(scaled_sample)
score = model.decision_function(scaled_sample)[0]

print(f"\nAnomaly Score: {score:.4f}")

# -----------------------------
# Binary result
# -----------------------------
if prediction[0] == -1:
    print("⚠ Anomaly detected!")
else:
    print("✅ Water quality normal.")

# -----------------------------
# Severity classification
# -----------------------------
if score > 0:
    severity = "Normal"
elif score > -0.05:
    severity = "Low Risk"
elif score > -0.15:
    severity = "Medium Risk"
else:
    severity = "High Risk"

print("Severity Level:", severity)

# -----------------------------
# Water Quality Index (0–100)
# -----------------------------
quality_score = max(0, min(100, int((score + 0.2) * 250)))

print("Water Quality Score:", quality_score, "/ 100")
