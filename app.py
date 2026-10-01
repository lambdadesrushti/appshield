"""
AppShield - Dashboard
----------------------
A multi-section Streamlit app for assessing Android app risk based on
permission/API usage patterns.

Sections:
1. Single App Check   - tick the permissions an app uses, get a risk result
2. Batch Check        - upload a CSV of many apps, get a sorted risk table
3. Model Insights      - see which features the model relies on most
"""

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="AppShield", page_icon="🛡️", layout="wide")


@st.cache_resource
def load_model():
    bundle = joblib.load("model/model.pkl")
    return bundle["model"], bundle["features"]


model, features = load_model()

st.sidebar.title("🛡️ AppShield")
st.sidebar.caption("Android Privacy & Malware Risk Analyzer")
page = st.sidebar.radio("Navigate", ["Single App Check", "Batch Check", "Model Insights"])


def predict_one(selected_features):
    row = pd.DataFrame([{f: (1 if f in selected_features else 0) for f in features}])
    pred = model.predict(row)[0]
    prob = model.predict_proba(row)[0][1]
    return pred, prob


# ---------------- SECTION 1: Single App Check ----------------
if page == "Single App Check":
    st.header("Check a Single App")
    st.write(
        "Tick the permissions / API features this app requests, "
        "then analyze its risk."
    )

    selected = st.multiselect("Permissions / features used by the app:", options=features)

    if st.button("Analyze Risk", type="primary"):
        pred, prob = predict_one(selected)
        if pred == 1:
            st.error(f"🔴 High Risk — Malware-like pattern detected ({prob:.1%} confidence)")
        else:
            st.success(f"🟢 Low Risk — Goodware-like pattern ({(1 - prob):.1%} confidence)")

        importances = pd.Series(model.feature_importances_, index=features)
        relevant = importances[importances.index.isin(selected)].sort_values(ascending=False).head(5)
        if not relevant.empty:
            st.subheader("Top contributing factors in this app")
            st.bar_chart(relevant)
        st.caption(
            "This is an educational risk assessment, not a guarantee of safety. "
            "Verify the app's source before installing."
        )

# ---------------- SECTION 2: Batch Check ----------------
elif page == "Batch Check":
    st.header("Batch Check Multiple Apps")
    st.write("Upload a CSV with the same feature columns as the training data.")

    uploaded = st.file_uploader("Upload CSV", type="csv")
    if uploaded:
        batch_df = pd.read_csv(uploaded)
        missing = [f for f in features if f not in batch_df.columns]
        if missing:
            st.warning(f"Missing {len(missing)} expected columns — they'll be treated as 0.")
            for m in missing:
                batch_df[m] = 0

        X_batch = batch_df[features].fillna(0)
        preds = model.predict(X_batch)
        probs = model.predict_proba(X_batch)[:, 1]

        result_df = batch_df.copy()
        result_df["Risk_Label"] = ["High Risk" if p == 1 else "Low Risk" for p in preds]
        result_df["Risk_Probability"] = probs.round(3)

        st.dataframe(
            result_df.sort_values("Risk_Probability", ascending=False),
            use_container_width=True,
        )
        st.caption(f"{int(preds.sum())} of {len(preds)} apps flagged as high risk.")

# ---------------- SECTION 3: Model Insights ----------------
elif page == "Model Insights":
    st.header("What Drives the Model's Decisions")
    importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False).head(15)
    st.bar_chart(importances)
    st.caption(
        "The 15 permission/API features the model relies on most heavily, "
        "learned from the training data as a whole."
    )
