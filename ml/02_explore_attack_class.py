import pandas as pd

df = pd.read_csv("data/merged.csv", low_memory=False)

ATTACK_LABEL = "DoS Hulk"

attack_df = df[df["Label"] == ATTACK_LABEL]
benign_df = df[df["Label"] == "BENIGN"]

print(f"Attack rows: {len(attack_df)} | Benign rows: {len(benign_df)}")

features_to_check = [
    "Flow Duration",
    "Total Fwd Packets",
    "Flow Bytes/s",
    "Flow Packets/s",
]

for feat in features_to_check:
    print(f"\n--- {feat} ---")
    print("Attack:\n", attack_df[feat].describe())
    print("Benign:\n", benign_df[feat].describe())
