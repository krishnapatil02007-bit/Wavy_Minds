import pickle
import pandas as pd
import time
import json
import os
from esp32_simulator import generate_sensor_data

print(" Loading ML Models...")
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
print(" Models Loaded.")

FLOW_ORDER = ["Borewell Source", "Upper Storage Tank", "Drinking Tap"]
SAMPLING_INTERVAL = 52  # Faster updates for demo
OUTPUT_FILE = "system_state.json"

print("\n Real-Time Water Monitoring Engine Started...")
print(f" Writing live data to: {OUTPUT_FILE}\n")

while True:

    sensor_data = generate_sensor_data()
    
    results = {}
    processed_data = []
    
    print(f"🔄 Processing Cycle: {time.strftime('%H:%M:%S')}")

    for sensor in sensor_data:
        location = sensor["location"]


        sample = pd.DataFrame([{
            "ph": sensor["ph"], "tds": sensor["tds"], 
            "turbidity": sensor["turbidity"], "temperature": sensor["temperature"]
        }])


        scaled_sample = scaler.transform(sample)
        score = model.decision_function(scaled_sample)[0]
        prediction = model.predict(scaled_sample)


        if score > 0: severity = "Normal"
        elif score > -0.05: severity = "Low Risk"
        elif score > -0.15: severity = "Medium Risk"
        else: severity = "High Risk"

        quality_score = max(0, min(100, int((score + 0.2) * 250)))
        status = "Contaminated" if prediction[0] == -1 else "Safe"
        
        results[location] = status


        processed_data.append({
            "location": location,
            "ph": sensor["ph"],
            "tds": sensor["tds"],
            "turbidity": sensor["turbidity"],
            "temperature": sensor["temperature"],
            "severity": severity,
            "quality_score": quality_score,
            "status": status
        })


    probable_source = "None"
    for location in FLOW_ORDER:
        if results.get(location) == "Contaminated":
            probable_source = location
            break


    system_state = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "results": processed_data,
        "probable_source": probable_source
    }

    temp_file = OUTPUT_FILE + ".tmp"
    with open(temp_file, "w") as f:
        json.dump(system_state, f, indent=4)
    os.replace(temp_file, OUTPUT_FILE)

    print(f"✅ Data written to {OUTPUT_FILE}")
    if probable_source != "None":
        print(f"🚨 ALERT: Contamination at {probable_source}")
    
    time.sleep(SAMPLING_INTERVAL)
