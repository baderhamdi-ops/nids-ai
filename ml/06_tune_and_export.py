"""
Week 2 - Day 5: Hyperparameter tuning + export final model.
Strategy: RandomizedSearchCV on a 20% sample (fast),
then retrain best params on full training data (accurate).
"""

import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import numpy as np

df = pd.read_csv("data/merged_clean.csv", low_memory=False)
X = df.drop(columns=["Label"]).select_dtypes(include="number")
y = df["Label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Step 1: tune on 20% sample ────────────────────────────────────
print("Step 1: Tuning on 20% sample...")
X_sample, _, y_sample, _ = train_test_split(
    X_train, y_train, test_size=0.8, random_state=42, stratify=y_train
)

param_dist = {
    "n_estimators": [100, 200],
    "max_depth": [None, 20, 30],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "max_features": ["sqrt", "log2"],
}

search = RandomizedSearchCV(
    RandomForestClassifier(class_weight="balanced", random_state=42, n_jobs=-1),
    param_distributions=param_dist,
    n_iter=10,
    scoring="f1_macro",
    cv=3,
    random_state=42,
    verbose=1,
    n_jobs=-1,
)
search.fit(X_sample, y_sample)
print(f"\nBest params: {search.best_params_}")
print(f"Best CV macro F1 on sample: {search.best_score_:.4f}")

# ── Step 2: retrain best config on full training data ─────────────
print("\nStep 2: Retraining best config on full training data...")
best_rf = RandomForestClassifier(
    **search.best_params_,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
best_rf.fit(X_train, y_train)
print("Done.")

# ── Step 3: evaluate on held-out test set ─────────────────────────
y_pred = best_rf.predict(X_test)
print("\n=== Final Tuned RF — Classification Report ===")
print(classification_report(y_test, y_pred, zero_division=0))

# ── Step 4: save as the production model ─────────────────────────
os.makedirs("models", exist_ok=True)
joblib.dump(best_rf, "models/best_model.joblib")
joblib.dump(list(X.columns), "models/feature_names.joblib")
print("\nSaved models/best_model.joblib  ← this is what the API will load")
print("Saved models/feature_names.joblib  ← feature order the model expects")
