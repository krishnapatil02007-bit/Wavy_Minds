import pickle
import pandas as pd

# -----------------------------
# Load trained model and scaler
# -----------------------------
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# -----------------------------
# Simulated multiple sensor data
# -----------------------------
sensor_data = [
    {
        "location": "Borewell Source",
        "ph": 7.3,
        "tds": 200,
        "turbidity": 1.8,
        "temperature": 27
    },
    {
        "location": "Upper Storage Tank",
        "ph": 6.5,
        "tds": 650,
        "turbidity": 8,
        "temperature": 34
    },
    {
        "location": "Drinking Tap",
        "ph": 6.3,
        "tds": 720,
        "turbidity": 10,
        "temperature": 36
    }
]

print("\n------ Water Quality Monitoring Report ------\n")

# -----------------------------
# Loop through each sensor
# -----------------------------
for sensor in sensor_data:
    
    location = sensor["location"]

    # Create dataframe for ML (without location)
    sample = pd.DataFrame([{
        "ph": sensor["ph"],
        "tds": sensor["tds"],
        "turbidity": sensor["turbidity"],
        "temperature": sensor["temperature"]
    }])

    # Scale
    scaled_sample = scaler.transform(sample)

    # Predict
    prediction = model.predict(scaled_sample)
    score = model.decision_function(scaled_sample)[0]

    # Severity logic
    if score > 0:
        severity = "Normal"
    elif score > -0.05:
        severity = "Low Risk"
    elif score > -0.15:
        severity = "Medium Risk"
    else:
        severity = "High Risk"

    # Water Quality Score
    quality_score = max(0, min(100, int((score + 0.2) * 250)))

    # Output
    print(f"Location: {location}")
    print(f"Anomaly Score: {score:.4f}")
    print(f"Severity: {severity}")
    print(f"Water Quality Score: {quality_score}/100")

    if prediction[0] == -1:
        print(f"⚠ Contamination detected at {location}")
    else:
        print(f"✅ Water safe at {location}")

    print("\n--------------------------------------------\n")
