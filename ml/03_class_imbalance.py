import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

df = pd.read_csv("data/merged_clean.csv", low_memory=False)

X = df.drop(columns=["Label"])
X = X.select_dtypes(include="number")
y = df["Label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("=== SMOTE (capped target, memory-safe) ===")
counts = y_train.value_counts()
TARGET = 5000
sampling_strategy = {
    cls: TARGET for cls, cnt in counts.items() if cnt < TARGET
}

smote = SMOTE(random_state=42, k_neighbors=2, sampling_strategy=sampling_strategy)
X_sm, y_sm = smote.fit_resample(X_train, y_train)
print("Resampled class counts:\n", y_sm.value_counts())

clf_sm = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
clf_sm.fit(X_sm, y_sm)
print(classification_report(y_test, clf_sm.predict(X_test), zero_division=0))

print("\n=== Random Undersampling (reduce majority class) ===")
rus = RandomUnderSampler(random_state=42)
X_rus, y_rus = rus.fit_resample(X_train, y_train)
clf_rus = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
clf_rus.fit(X_rus, y_rus)
print(classification_report(y_test, clf_rus.predict(X_test), zero_division=0))

print("\n=== Class Weights (penalize majority errors more) ===")
clf_cw = RandomForestClassifier(
    n_estimators=50, class_weight="balanced", random_state=42, n_jobs=-1
)
clf_cw.fit(X_train, y_train)
print(classification_report(y_test, clf_cw.predict(X_test), zero_division=0))
