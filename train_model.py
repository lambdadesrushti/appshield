"""
AppShield - Model Training Script
----------------------------------
Trains a Random Forest classifier on the TUANDROMD dataset to detect
malware-like Android apps based on their permission/API usage patterns.

Run this BEFORE starting the dashboard - it creates model/model.pkl,
which the dashboard loads to make predictions.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

DATA_PATH = "data/TUANDROMD.csv"
MODEL_PATH = "model/model.pkl"


def main():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    # The dataset's label column is usually named "Label" (Malware / Goodware)
    target_col = "Label" if "Label" in df.columns else df.columns[-1]

    # Drop any rows with missing values, just to be safe
    df = df.dropna()

    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Convert text labels (Malware/Goodware) to 1/0 if needed
    if y.dtype == object:
        y = y.map({"Malware": 1, "Goodware": 0})

    print(f"Dataset shape: {X.shape[0]} apps, {X.shape[1]} features")
    print(f"Class balance:\n{y.value_counts()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"\nTest accuracy: {acc:.4f}\n")
    print(classification_report(y_test, preds, target_names=["Goodware", "Malware"]))

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({"model": model, "features": list(X.columns)}, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
