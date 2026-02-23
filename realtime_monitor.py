import pickle
import pandas as pd
import time
from esp32_simulator import generate_sensor_data

# Load model
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

print("\n🚀 Real-Time Water Monitoring Started...\n")

while True:

    sensor_data = generate_sensor_data()

    print("\n=========== NEW SENSOR CYCLE ===========\n")

    for sensor in sensor_data:

        location = sensor["location"]

        sample = pd.DataFrame([{
            "ph": sensor["ph"],
            "tds": sensor["tds"],
            "turbidity": sensor["turbidity"],
            "temperature": sensor["temperature"]
        }])

        scaled_sample = scaler.transform(sample)

        prediction = model.predict(scaled_sample)
        score = model.decision_function(scaled_sample)[0]

        if score > 0:
            severity = "Normal"
        elif score > -0.05:
            severity = "Low Risk"
        elif score > -0.15:
            severity = "Medium Risk"
        else:
            severity = "High Risk"

        quality_score = max(0, min(100, int((score + 0.2) * 250)))

        print(f"📍 Location: {location}")
        print(f"pH: {sensor['ph']} | TDS: {sensor['tds']} | Turbidity: {sensor['turbidity']} | Temp: {sensor['temperature']}")
        print(f"Severity: {severity}")
        print(f"Water Quality Score: {quality_score}/100")

        if prediction[0] == -1:
            print("⚠ Contamination Detected!\n")
        else:
            print("✅ Water Safe\n")

    time.sleep(5)
