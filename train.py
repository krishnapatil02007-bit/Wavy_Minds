import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle

# Fix randomness
np.random.seed(42)

# -----------------------
# Generate NORMAL data
# -----------------------
normal_samples = 500

normal_data = pd.DataFrame({
    "ph": np.random.normal(7.2, 0.2, normal_samples),
    "tds": np.random.normal(220, 30, normal_samples),
    "turbidity": np.random.normal(2, 0.8, normal_samples),
    "temperature": np.random.normal(28, 1.5, normal_samples)
})

# -----------------------
# Generate ABNORMAL data
# -----------------------
abnormal_samples = 50

abnormal_data = pd.DataFrame({
    "ph": np.random.uniform(4, 10, abnormal_samples),
    "tds": np.random.uniform(400, 900, abnormal_samples),
    "turbidity": np.random.uniform(6, 20, abnormal_samples),
    "temperature": np.random.uniform(35, 50, abnormal_samples)
})

# Combine both
data = pd.concat([normal_data, abnormal_data], ignore_index=True)

# -----------------------
# Scale features
# -----------------------
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# -----------------------
# Train Isolation Forest
# -----------------------
model = IsolationForest(
    contamination=0.1,
    n_estimators=100,
    random_state=42
)

model.fit(scaled_data)

# -----------------------
# Save model and scaler
# -----------------------
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Model and scaler saved successfully!")
