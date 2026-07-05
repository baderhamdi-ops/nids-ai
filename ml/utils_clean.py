import pandas as pd
import numpy as np


def load_clean(path="data/merged.csv"):
    df = pd.read_csv(path, low_memory=False)
    df.columns = df.columns.str.strip()

    before = len(df)
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    if "Flow Duration" in df.columns:
        df = df[df["Flow Duration"] >= 0]

    after = len(df)
    print(f"Cleaned: {before} -> {after} rows ({before - after} dropped)")
    return df


if __name__ == "__main__":
    df = load_clean()
    df.to_csv("data/merged_clean.csv", index=False)
    print("Saved data/merged_clean.csv")
