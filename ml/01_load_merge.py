import pandas as pd

CSV_PATH = "data/raw/combinenew.csv"

df = pd.read_csv(CSV_PATH, low_memory=False)
df.columns = df.columns.str.strip()

print("Shape:", df.shape)
print("\nColumns:")
print(list(df.columns))

print("\n--- df.head() ---")
print(df.head())

print("\n--- df['Label'].value_counts() ---")
print(df["Label"].value_counts())

df.to_csv("data/merged.csv", index=False)
print("\nSaved cleaned copy to data/merged.csv")
