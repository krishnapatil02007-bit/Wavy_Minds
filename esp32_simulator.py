

import random
import time
import json
import os 

FLOW_ORDER = [
    "Borewell Source",
    "Upper Storage Tank",
    "Drinking Tap"
]

CONTAMINATION_PROBABILITY = 0.2  # 20% chance

def generate_clean_reading():
    return {
        "ph": round(random.uniform(6.8, 7.8), 2),
        "tds": round(random.uniform(150, 350), 2),
        "turbidity": round(random.uniform(1, 4), 2),
        "temperature": round(random.uniform(25, 30), 2)
    }

def generate_contaminated_reading():
    return {
        "ph": round(random.uniform(4, 10), 2),  # Extreme pH
        "tds": round(random.uniform(600, 1000), 2), # High TDS
        "turbidity": round(random.uniform(8, 25), 2), # High Turbidity
        "temperature": round(random.uniform(35, 50), 2) # High Temp
    }

def generate_sensor_data():
    sensor_payload = []

    force_danger_mode = os.path.exists("danger.txt")

    if force_danger_mode:
        print("⚠️ MANUAL TRIGGER DETECTED: Forcing Contamination!")
        
        contamination_event = True
        contamination_start_index = 1
    else:

        contamination_event = random.random() < CONTAMINATION_PROBABILITY
        contamination_start_index = None
        if contamination_event:
            contamination_start_index = random.randint(0, len(FLOW_ORDER) - 1)

    for i, location in enumerate(FLOW_ORDER):
        
        if contamination_event and i >= contamination_start_index:
            reading = generate_contaminated_reading()
        else:
            reading = generate_clean_reading()

        reading["location"] = location
        sensor_payload.append(reading)

    return sensor_payload

if __name__ == "__main__":

    SAMPLING_INTERVAL = 5 

    print("\nESP32 Simulation Started...")
    print("👉 Tip: Create a file named 'danger.txt' in this folder to trigger Red Alert!\n")

    while True:
        payload = generate_sensor_data()
        print(json.dumps(payload, indent=2))
        time.sleep(SAMPLING_INTERVAL)