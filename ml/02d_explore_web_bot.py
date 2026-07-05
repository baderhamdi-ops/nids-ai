import pandas as pd

df = pd.read_csv("data/merged_clean.csv", low_memory=False)

benign_df = df[df["Label"] == "BENIGN"]

features_to_check = [
    "Total Length of Fwd Packets",
    "Fwd Packet Length Mean",
    "Flow Duration",
]

for label in ["Web Attack_Brute Force", "Web Attack_XSS", "Bot"]:
    attack_df = df[df["Label"] == label]
    print(f"\n========== {label} ==========")
    print(f"Attack rows: {len(attack_df)} | Benign rows: {len(benign_df)}")
    for feat in features_to_check:
        print(f"\n--- {feat} ---")
        print("Attack:\n", attack_df[feat].describe())
        print("Benign:\n", benign_df[feat].describe())
