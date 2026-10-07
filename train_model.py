"""
AppShield - Model Training Script
----------------------------------
Trains a Random Forest classifier on the TUANDROMD dataset, and also saves
two real example apps (one malware, one goodware) for reliable demo use
in the dashboard.
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
    df.columns = df.columns.str.strip()

    target_col = "Label" if "Label" in df.columns else df.columns[-1]
    df = df.dropna(subset=[target_col])

    X = df.drop(columns=[target_col])
    y = df[target_col]

    if not pd.api.types.is_numeric_dtype(y):
        y_clean = y.astype(str).str.strip().str.lower()
        y = y_clean.map({"malware": 1, "goodware": 0})

    mask = y.notna()
    X, y = X[mask], y[mask]
    y = y.astype(int)
    X = X.fillna(0)

    print(f"Final dataset shape: {X.shape[0]} apps, {X.shape[1]} features")
    print(f"Class balance:\n{y.value_counts()}\n")

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

    # --- Pick real example rows for reliable demo use ---
    test_probs = model.predict_proba(X_test)[:, 1]
    results = X_test.copy()
    results["actual"] = y_test.values
    results["prob"] = test_probs

    malware_candidates = results[(results["actual"] == 1) & (results["prob"] > 0.95)]
    goodware_candidates = results[(results["actual"] == 0) & (results["prob"] < 0.05)]

    def row_to_feature_list(row, feature_cols):
        return [f for f in feature_cols if row[f] == 1]

    sample_malware = row_to_feature_list(malware_candidates.iloc[0], X.columns) if len(malware_candidates) else []
    sample_goodware = row_to_feature_list(goodware_candidates.iloc[0], X.columns) if len(goodware_candidates) else []

    print(f"Sample malware example: {len(sample_malware)} permissions selected")
    print(f"Sample goodware example: {len(sample_goodware)} permissions selected")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({
        "model": model,
        "features": list(X.columns),
        "sample_malware": sample_malware,
        "sample_goodware": sample_goodware,
        "test_accuracy": acc,
    }, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
