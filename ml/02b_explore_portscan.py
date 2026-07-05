import pandas as pd

df = pd.read_csv("data/merged_clean.csv", low_memory=False)

ATTACK_LABEL = "PortScan"

attack_df = df[df["Label"] == ATTACK_LABEL]
benign_df = df[df["Label"] == "BENIGN"]

print(f"Attack rows: {len(attack_df)} | Benign rows: {len(benign_df)}")

features_to_check = [
    "Destination Port",
    "Flow Duration",
    "Flow IAT Mean",
    "Fwd Packets/s",
]

for feat in features_to_check:
    print(f"\n--- {feat} ---")
    print("Attack:\n", attack_df[feat].describe())
    print("Benign:\n", benign_df[feat].describe())
