import random
import time
import json

# Water flow order (very important)
FLOW_ORDER = [
    "Borewell Source",
    "Upper Storage Tank",
    "Drinking Tap"
]

# Probability that contamination starts at any cycle
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
        "ph": round(random.uniform(4, 10), 2),
        "tds": round(random.uniform(600, 1000), 2),
        "turbidity": round(random.uniform(8, 25), 2),
        "temperature": round(random.uniform(35, 50), 2)
    }

def generate_sensor_data():
    sensor_payload = []

    # Decide randomly if contamination event happens
    contamination_event = random.random() < CONTAMINATION_PROBABILITY

    contamination_start_index = None

    if contamination_event:
        contamination_start_index = random.randint(0, len(FLOW_ORDER) - 1)

    for i, location in enumerate(FLOW_ORDER):

        # If contamination started and this location is downstream
        if contamination_event and i >= contamination_start_index:
            reading = generate_contaminated_reading()
        else:
            reading = generate_clean_reading()

        reading["location"] = location
        sensor_payload.append(reading)

    return sensor_payload


# Standalone testing mode
if __name__ == "__main__":

    SAMPLING_INTERVAL = 10  # seconds

    print("\n🚀 ESP32 Simulation Started...\n")

    while True:
        payload = generate_sensor_data()
        print(json.dumps(payload, indent=2))
        time.sleep(SAMPLING_INTERVAL)