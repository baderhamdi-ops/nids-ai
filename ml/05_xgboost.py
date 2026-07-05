"""
Week 2 - Day 3-4: XGBoost
Key difference from RF: sequential trees, each corrects the previous one's errors.
"""

import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

df = pd.read_csv("data/merged_clean.csv", low_memory=False)
X = df.drop(columns=["Label"]).select_dtypes(include="number")
y = df["Label"]

# XGBoost needs numeric labels, not strings
le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print("Training XGBoost...")
xgb = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    use_label_encoder=False,
    eval_metric="mlogloss",
    random_state=42,
    n_jobs=-1,
    tree_method="hist",   # fast histogram method, handles large datasets well
)
xgb.fit(X_train, y_train)
print("Done.")

y_pred = xgb.predict(X_test)

# Decode back to original label names for the report
print("\n=== XGBoost Classification Report ===")
print(classification_report(
    le.inverse_transform(y_test),
    le.inverse_transform(y_pred),
    zero_division=0
))

os.makedirs("models", exist_ok=True)
joblib.dump(xgb, "models/xgboost.joblib")
joblib.dump(le, "models/label_encoder.joblib")
print("Saved models/xgboost.joblib")
print("Saved models/label_encoder.joblib")
