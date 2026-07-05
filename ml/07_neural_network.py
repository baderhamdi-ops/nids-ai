"""
Week 3 - Day 1-2: Neural Network
Architecture from the project plan:
Input(78) -> 256 -> ReLU -> Dropout(0.3) -> 128 -> ReLU -> Dropout(0.3) -> Output(15)
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report
from tensorflow import keras
from tensorflow.keras import layers

df = pd.read_csv("data/merged_clean.csv", low_memory=False)
X = df.drop(columns=["Label"]).select_dtypes(include="number")
y = df["Label"]

# Neural networks need numeric labels AND scaled features
le = LabelEncoder()
y_encoded = le.fit_transform(y)
n_classes = len(le.classes_)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Compute class weights (same approach that won in Week 1)
from sklearn.utils.class_weight import compute_class_weight
cw = compute_class_weight("balanced", classes=np.unique(y_train), y=y_train)
class_weight_dict = dict(enumerate(cw))

# Build the model exactly as specified in the project plan
model = keras.Sequential([
    layers.Input(shape=(78,)),
    layers.Dense(256, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(n_classes, activation="softmax"),
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)
model.summary()

print("\nTraining neural network...")
history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=1024,
    validation_split=0.1,
    class_weight=class_weight_dict,
    verbose=1,
)

# Evaluate
y_pred = np.argmax(model.predict(X_test, verbose=0), axis=1)
print("\n=== Neural Network Classification Report ===")
print(classification_report(
    le.inverse_transform(y_test),
    le.inverse_transform(y_pred),
    zero_division=0
))

# Save
os.makedirs("models", exist_ok=True)
model.save("models/neural_network.keras")
joblib.dump(scaler, "models/scaler.joblib")
joblib.dump(le,     "models/label_encoder.joblib")
print("Saved models/neural_network.keras")
print("Saved models/scaler.joblib")
