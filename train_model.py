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
    df.columns = df.columns.str.strip()  # remove any hidden whitespace in column names

    target_col = "Label" if "Label" in df.columns else df.columns[-1]
    print(f"Using target column: '{target_col}'")

    # Drop rows where the label itself is missing (can't train on those)
    df = df.dropna(subset=[target_col])

    X = df.drop(columns=[target_col])
    y = df[target_col]

    print(f"Unique values after dropping missing labels: {sorted(y.astype(str).str.strip().str.lower().unique())}")

    # Convert text labels to 1/0 whenever the column isn't already numeric.
    # (Checking dtype == object alone misses pandas' newer string/Arrow dtypes,
    # which is what caused the earlier crash.)
    if not pd.api.types.is_numeric_dtype(y):
        y_clean = y.astype(str).str.strip().str.lower()
        y = y_clean.map({"malware": 1, "goodware": 0})

    # Drop any rows where mapping still failed (unexpected label text)
    before = len(y)
    mask = y.notna()
    X, y = X[mask], y[mask]
    dropped = before - len(y)
    if dropped > 0:
        print(f"Warning: dropped {dropped} rows with unrecognized labels.")

    y = y.astype(int)

    # Fill any missing feature values with 0 (permission/API features are binary flags)
    X = X.fillna(0)

    print(f"\nFinal dataset shape: {X.shape[0]} apps, {X.shape[1]} features")
    print(f"Class balance:\n{y.value_counts()}\n")

    if y.nunique() < 2:
        raise ValueError(
            "Only one class remains after cleaning - check the printed "
            "unique values above and adjust the label mapping."
        )

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
