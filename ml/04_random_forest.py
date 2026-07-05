"""
Week 2 - Day 1-2: Random Forest
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

df = pd.read_csv("data/merged_clean.csv", low_memory=False)
X = df.drop(columns=["Label"]).select_dtypes(include="number")
y = df["Label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train: {X_train.shape} | Test: {X_test.shape}")

print("\nTraining Random Forest (100 trees)...")
rf = RandomForestClassifier(
    n_estimators=100,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train, y_train)
print("Done.")

y_pred = rf.predict(X_test)
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, zero_division=0))

importances = pd.Series(rf.feature_importances_, index=X.columns)
top20 = importances.nlargest(20)
print("\n=== Top 20 Most Important Features ===")
print(top20)

plt.figure(figsize=(10, 7))
top20.sort_values().plot(kind="barh", color="#2a5d9f")
plt.title("Top 20 Feature Importances — Random Forest")
plt.xlabel("Importance score")
plt.tight_layout()
plt.savefig("rf_feature_importance.png")
print("Saved rf_feature_importance.png")

os.makedirs("models", exist_ok=True)
joblib.dump(rf, "models/random_forest.joblib")
print("Saved models/random_forest.joblib")
