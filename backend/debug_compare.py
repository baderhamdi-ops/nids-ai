import sys
sys.path.insert(0, "/home/b4der/nids-ai/backend")
import pandas as pd
import joblib
from feature_mapper import FEATURE_NAMES

# Real PortScan example from training data
df = pd.read_csv("/home/b4der/nids-ai/ml/data/merged_clean.csv")
real_row = df[df["Label"] == "PortScan"].iloc[0]

print(f"{'Feature':<28} {'Real PortScan (CSV)':>20} {'Notes'}")
print("-" * 70)
for f in FEATURE_NAMES:
    val = real_row[f]
    print(f"{f:<28} {val:>20}")
