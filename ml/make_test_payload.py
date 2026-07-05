import pandas as pd
import joblib
import json

features = joblib.load("models/feature_names.joblib")
df = pd.read_csv("data/merged_clean.csv")

def payload_for(label_filter):
    row = df[df["Label"] == label_filter].iloc[0]
    return {
        "features": [float(row[f]) for f in features],
        "src_ip": "10.0.0.1",
        "dst_ip": "10.0.0.2",
        "dst_port": int(row["Destination Port"]),
        "protocol": "TCP"
    }

benign  = payload_for("BENIGN")
hulk    = payload_for("DoS Hulk")

with open("test_benign.json", "w") as f:
    json.dump(benign, f)
with open("test_attack.json", "w") as f:
    json.dump(hulk, f)

print("Écrit test_benign.json et test_attack.json")
