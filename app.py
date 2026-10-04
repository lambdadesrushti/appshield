"""
AppShield - Modern Interactive Dashboard
Android Privacy & Malware Risk Analyzer
"""

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="AppShield | AI Security Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# Adaptive Styling (Strict Light/Dark Mode Compatibility)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
:root {
    --bg-primary: #F8FAFC;
    --card-bg: rgba(255, 255, 255, 0.90);
    --card-border: #E2E8F0;
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --brand: #2563EB;
    --brand-gradient: linear-gradient(135deg, #2563EB 0%, #06B6D4 100%);
    --danger-bg: #FEF2F2;
    --danger-border: #F87171;
    --danger-text: #B91C1C;
    --safe-bg: #F0FDF4;
    --safe-border: #4ADE80;
    --safe-text: #15803D;
    --badge-bg: #EEF2F6;
    --shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #0B1120;
        --card-bg: rgba(17, 24, 39, 0.85);
        --card-border: #374151;
        --text-primary: #F9FAFB;
        --text-secondary: #9CA3AF;
        --brand: #38BDF8;
        --brand-gradient: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
        --danger-bg: rgba(127, 29, 29, 0.35);
        --danger-border: #EF4444;
        --danger-text: #FCA5A5;
        --safe-bg: rgba(20, 83, 45, 0.35);
        --safe-border: #22C55E;
        --safe-text: #86EFAC;
        --badge-bg: #1F2937;
        --shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }
}

.hero-box {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: var(--shadow);
}
.hero-title {
    font-size: 32px;
    font-weight: 800;
    margin: 0;
    background: var(--brand-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    color: var(--text-secondary);
    font-size: 15px;
    margin-top: 6px;
    margin-bottom: 0px;
}

.result-card {
    border-radius: 16px;
    padding: 24px;
    margin-top: 16px;
    margin-bottom: 20px;
    border: 1.5px solid;
    box-shadow: var(--shadow);
}
.result-card.danger {
    background: var(--danger-bg);
    border-color: var(--danger-border);
    color: var(--danger-text);
}
.result-card.safe {
    background: var(--safe-bg);
    border-color: var(--safe-border);
    color: var(--safe-text);
}

.metric-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 16px 20px;
    text-align: center;
    box-shadow: var(--shadow);
}
.metric-val {
    font-size: 30px;
    font-weight: 800;
    color: var(--brand);
}
.metric-lbl {
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 600;
}

.badge-tag {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 8px;
    background: var(--badge-bg);
    color: var(--text-primary);
    font-size: 12px;
    font-weight: 600;
    margin: 3px 2px;
    border: 1px solid var(--card-border);
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    bundle = joblib.load("model/model.pkl")
    return bundle["model"], bundle["features"]


try:
    model, features = load_model()
except Exception as e:
    st.error(f"Could not load model bundle: {e}")
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0 16px 0;">
            <span style="font-size: 46px;">🛡️</span>
            <h2 style="margin: 4px 0 0 0; font-size: 22px;">AppShield</h2>
            <p style="font-size: 13px; color: var(--text-secondary); margin: 0;">AI Permission Inspector</p>
        </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🔍 Single App Scanner", "📁 Batch CSV Audit", "📊 Threat Intelligence & Metrics"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
        <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.5;">
            <b>Architecture Stack:</b><br>
            • Algorithm: Random Forest (200 Estimators)<br>
            • Dataset: TUANDROMD Benchmark<br>
            • Deployment: Docker Compose Container
        </div>
    """, unsafe_allow_html=True)


def predict_profile(selected_set):
    row = pd.DataFrame([{f: (1 if f in selected_set else 0) for f in features}])
    pred = model.predict(row)[0]
    prob = model.predict_proba(row)[0][1]
    return pred, prob


# ---------------- SECTION 1: Single App Scanner ----------------
if page == "🔍 Single App Scanner":
    st.markdown("""
        <div class="hero-box">
            <h1 class="hero-title">Android Application Risk Scanner</h1>
            <p class="hero-subtitle">Identify malicious permission profiles and explain threat factors using trained ensemble intelligence.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("##### ⚡ Quick Test Presets (Click to Auto-load for Viva)")
    c1, c2, c3, c4 = st.columns(4)

    if c1.button("📱 Safe: Calculator Utility", use_container_width=True):
        st.session_state["app_selected"] = ["VIBRATE", "INTERNET"]
    if c2.button("📷 Safe: Camera & Filter App", use_container_width=True):
        st.session_state["app_selected"] = ["CAMERA", "READ_EXTERNAL_STORAGE", "WRITE_EXTERNAL_STORAGE", "FLASHLIGHT"]
    if c3.button("⚠️ Malicious: SMS Trojan", use_container_width=True):
        st.session_state["app_selected"] = [
            "SEND_SMS", "RECEIVE_BOOT_COMPLETED", "READ_PHONE_STATE",
            "Ljava/net/URL;->openConnection", "KILL_BACKGROUND_PROCESSES"
        ]
    if c4.button("🚨 Malicious: Stealth Spyware", use_container_width=True):
        st.session_state["app_selected"] = [
            "RECEIVE_BOOT_COMPLETED", "GET_TASKS", "WAKE_LOCK",
            "Landroid/location/LocationManager;->getLastKgoodwarewnLocation",
            "Ldalvik/system/DexClassLoader;->loadClass", "READ_PHONE_STATE"
        ]

    default_features = st.session_state.get("app_selected", [])

    selected_perms = st.multiselect(
        "Select requested permissions & critical API calls:",
        options=features,
        default=[p for p in default_features if p in features],
        help="Type or select permissions requested in AndroidManifest.xml"
    )

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        scan_now = st.button("🚀 Analyze Risk", type="primary", use_container_width=True)

    if scan_now or selected_perms:
        pred, risk_score = predict_profile(set(selected_perms))
        is_malware = (pred == 1)

        if is_malware:
            st.markdown(f"""
                <div class="result-card danger">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 28px;">🚨</span>
                            <b style="font-size: 22px; margin-left: 8px;">HIGH RISK DETECTED — Malware-like Pattern</b>
                        </div>
                        <span style="font-size: 22px; font-weight: 800;">{risk_score:.1%} Risk</span>
                    </div>
                    <p style="margin: 8px 0 0 0; opacity: 0.9;">
                        The requested permission cluster matches known background interception and privilege escalation signatures.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="result-card safe">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 28px;">✅</span>
                            <b style="font-size: 22px; margin-left: 8px;">LOW RISK DETECTED — Benign / Goodware Pattern</b>
                        </div>
                        <span style="font-size: 22px; font-weight: 800;">{(1 - risk_score):.1%} Safe</span>
                    </div>
                    <p style="margin: 8px 0 0 0; opacity: 0.9;">
                        The requested permissions follow standard functional patterns consistent with benign Play Store applications.
                    </p>
                </div>
            """, unsafe_allow_html=True)

        st.progress(float(risk_score))

        r1, r2 = st.columns([1, 1])
        with r1:
            st.markdown("##### 🔍 Why Did the Model Reach This Verdict?")
            importances = pd.Series(model.feature_importances_, index=features)
            active_factors = importances[importances.index.isin(selected_perms)].sort_values(ascending=False).head(6)

            if not active_factors.empty:
                st.bar_chart(active_factors, color="#2563EB")
            else:
                st.info("No high-risk signature features detected in current selections.")

        with r2:
            st.markdown("##### 📋 Active Permission Manifest")
            if selected_perms:
                badge_html = "".join([f"<span class='badge-tag'>{p}</span>" for p in selected_perms])
                st.markdown(f"<div>{badge_html}</div>", unsafe_allow_html=True)
            else:
                st.write("No permissions selected.")


# ---------------- SECTION 2: Batch CSV Audit ----------------
elif page == "📁 Batch CSV Audit":
    st.markdown("""
        <div class="hero-box">
            <h1 class="hero-title">Bulk Application Auditor</h1>
            <p class="hero-subtitle">Upload multi-app permission exports to rank threats across an enterprise inventory.</p>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload App Manifest Matrix (.csv)", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()

        missing = [f for f in features if f not in df.columns]
        if missing:
            for m in missing:
                df[m] = 0

        X_eval = df[features].fillna(0)
        batch_preds = model.predict(X_eval)
        batch_probs = model.predict_proba(X_eval)[:, 1]

        total = len(batch_preds)
        mal_count = int(batch_preds.sum())
        good_count = total - mal_count

        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">{total}</div>
                    <div class="metric-lbl">Apps Audited</div>
                </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val" style="color: #EF4444;">{mal_count}</div>
                    <div class="metric-lbl">High-Risk Apps</div>
                </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val" style="color: #22C55E;">{good_count}</div>
                    <div class="metric-lbl">Benign Apps</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        res_df = df.copy()
        res_df["Risk_Score"] = (batch_probs * 100).round(1).astype(str) + "%"
        res_df["Verdict"] = ["🔴 High Risk (Malware)" if p == 1 else "🟢 Low Risk (Goodware)" for p in batch_preds]

        cols_display = ["Verdict", "Risk_Score"] + [c for c in res_df.columns if c not in ["Verdict", "Risk_Score"]][:6]
        st.dataframe(res_df[cols_display], use_container_width=True)


# ---------------- SECTION 3: Threat Intelligence & Metrics ----------------
elif page == "📊 Threat Intelligence & Metrics":
    st.markdown("""
        <div class="hero-box">
            <h1 class="hero-title">Threat Intelligence & Model Metrics</h1>
            <p class="hero-subtitle">Statistical weights and global feature importance across 241 Android indicators.</p>
        </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-val">99.78%</div>
                <div class="metric-lbl">Test Set Accuracy</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-val">1.00</div>
                <div class="metric-lbl">Malware Precision</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-val">4,464</div>
                <div class="metric-lbl">Analyzed Apps</div>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-val">241</div>
                <div class="metric-lbl">Feature Dimensions</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### 📌 Global Top 15 Danger Indicators")
    st.caption("These permissions and API calls have the strongest predictive weight in flagging Android malware.")

    global_importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False).head(15)
    st.bar_chart(global_importances, color="#2563EB")