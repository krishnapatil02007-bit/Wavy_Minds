import random
import json
import time

locations = [
    "Borewell Source",
    "Upper Storage Tank",
    "Drinking Tap"
]

def generate_sensor_data():
    sensor_payload = []

    for location in locations:
        data = {
            "location": location,
            "ph": round(random.uniform(6.5, 8.5), 2),
            "tds": round(random.uniform(150, 900), 2),
            "turbidity": round(random.uniform(1, 20), 2),
            "temperature": round(random.uniform(25, 45), 2)
        }
        sensor_payload.append(data)

    return sensor_payload


if __name__ == "__main__":
    while True:
        payload = generate_sensor_data()
        print(json.dumps(payload, indent=2))
        SAMPLING_INTERVAL = 10  # seconds (for demo)
        time.sleep(SAMPLING_INTERVAL)
