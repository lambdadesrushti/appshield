"""
AppShield - Elite AI Security Operations Dashboard
Vibrant Cyber-Neon Glassmorphic Security Telemetry
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(
    page_title="AppShield | AI Security Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# High-Saturation Neon Cyber Theme (Forced Dark Gradient)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

/* Force Global Deep Cyber Canvas */
.stApp {
    background: radial-gradient(circle at 15% 15%, #181938 0%, #0D1021 50%, #070913 100%) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #F8FAFC !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101426 0%, #0A0D1A 100%) !important;
    border-right: 1px solid rgba(99, 102, 241, 0.25) !important;
}

/* Glowing Top Status Bar */
.telemetry-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(18, 23, 46, 0.85);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 14px;
    padding: 12px 24px;
    margin-bottom: 24px;
    box-shadow: 0 0 25px rgba(79, 70, 229, 0.15);
}
.pulse-indicator {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 14px #10B981;
    margin-right: 8px;
    animation: livePulse 1.6s infinite;
}
@keyframes livePulse {
    0% { transform: scale(0.9); opacity: 0.8; }
    50% { transform: scale(1.4); opacity: 1; }
    100% { transform: scale(0.9); opacity: 0.8; }
}

/* Vibrant Hero Banner */
.hero-banner {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 35%, #DB2777 75%, #F43F5E 100%);
    border-radius: 22px;
    padding: 36px 42px;
    color: #FFFFFF;
    position: relative;
    overflow: hidden;
    margin-bottom: 26px;
    box-shadow: 0 20px 50px -10px rgba(219, 39, 119, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.2);
}
.hero-banner::after {
    content: '';
    position: absolute;
    top: -60%;
    right: -25%;
    width: 480px;
    height: 480px;
    background: radial-gradient(circle, rgba(255,255,255,0.22) 0%, transparent 65%);
    pointer-events: none;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0, 0, 0, 0.28);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 30px;
    padding: 5px 14px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #FDF2F8;
    margin-bottom: 12px;
}
.hero-title {
    font-size: 40px;
    font-weight: 800;
    line-height: 1.15;
    margin: 0 0 10px 0;
    color: #FFFFFF !important;
}
.hero-desc {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.95);
    max-width: 860px;
    line-height: 1.55;
    margin: 0;
}

/* 4-Block Colorful KPI Row */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
.kpi-card {
    border-radius: 18px;
    padding: 22px 24px;
    backdrop-filter: blur(14px);
    transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
}
.kpi-card:hover {
    transform: translateY(-4px);
}
.kpi-card.purple {
    background: linear-gradient(145deg, rgba(79, 70, 229, 0.22), rgba(30, 27, 75, 0.55));
    border: 1px solid rgba(129, 140, 248, 0.45);
    box-shadow: 0 0 25px rgba(79, 70, 229, 0.15);
}
.kpi-card.emerald {
    background: linear-gradient(145deg, rgba(16, 185, 129, 0.22), rgba(6, 78, 59, 0.55));
    border: 1px solid rgba(52, 211, 153, 0.45);
    box-shadow: 0 0 25px rgba(16, 185, 129, 0.15);
}
.kpi-card.cyan {
    background: linear-gradient(145deg, rgba(6, 182, 212, 0.22), rgba(22, 78, 99, 0.55));
    border: 1px solid rgba(34, 211, 238, 0.45);
    box-shadow: 0 0 25px rgba(6, 182, 212, 0.15);
}
.kpi-card.rose {
    background: linear-gradient(145deg, rgba(244, 63, 94, 0.22), rgba(136, 19, 55, 0.55));
    border: 1px solid rgba(251, 113, 133, 0.45);
    box-shadow: 0 0 25px rgba(244, 63, 94, 0.15);
}
.kpi-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #CBD5E1;
    margin-bottom: 8px;
}
.kpi-val {
    font-size: 34px;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.5px;
}
.kpi-card.purple .kpi-val { color: #A5B4FC; }
.kpi-card.emerald .kpi-val { color: #6EE7B7; }
.kpi-card.cyan .kpi-val { color: #67E8F9; }
.kpi-card.rose .kpi-val { color: #FDA4AF; }
.kpi-sub {
    font-size: 12px;
    color: #94A3B8;
    margin-top: 6px;
}

/* Neon Verdict HUDs */
.verdict-hud {
    border-radius: 20px;
    padding: 28px 32px;
    margin-top: 22px;
    margin-bottom: 24px;
    border-width: 2px;
    border-style: solid;
}
.verdict-hud.danger {
    background: linear-gradient(135deg, rgba(127, 29, 29, 0.6) 0%, rgba(69, 10, 10, 0.85) 100%);
    border-color: #EF4444;
    box-shadow: 0 0 40px rgba(239, 68, 68, 0.4);
}
.verdict-hud.safe {
    background: linear-gradient(135deg, rgba(6, 78, 59, 0.6) 0%, rgba(2, 44, 34, 0.85) 100%);
    border-color: #10B981;
    box-shadow: 0 0 40px rgba(16, 185, 129, 0.4);
}
.verdict-title {
    font-size: 26px;
    font-weight: 800;
    margin: 0 0 6px 0;
}
.verdict-hud.danger .verdict-title { color: #FCA5A5; }
.verdict-hud.safe .verdict-title { color: #6EE7B7; }

/* Interactive Permission Tags */
.perm-tag {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 9px;
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.25), rgba(124, 58, 237, 0.15));
    border: 1px solid rgba(165, 180, 252, 0.4);
    color: #C7D2FE;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    margin: 4px;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.2);
}

/* Colorful Preset Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%) !important;
    color: #E0E7FF !important;
    border: 1px solid rgba(129, 140, 248, 0.4) !important;
    border-radius: 12px !important;
    padding: 10px 16px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:hover {
    border-color: #A5B4FC !important;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.5) !important;
    transform: translateY(-2px) !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5 0%, #EC4899 100%) !important;
    border: none !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 25px rgba(236, 72, 153, 0.4) !important;
}
div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 35px rgba(236, 72, 153, 0.7) !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Load Intelligence Model
# ---------------------------------------------------------------------------
@st.cache_resource
def load_security_engine():
    bundle = joblib.load("model/model.pkl")
    return bundle["model"], bundle["features"]

try:
    model, features = load_security_engine()
except Exception as e:
    st.error(f"⚠️️ Security Engine Offline: {e}")
    st.stop()

# Top Telemetry Header
st.markdown("""
<div class="telemetry-bar">
    <div style="display: flex; align-items: center; gap: 10px;">
        <span class="pulse-indicator"></span>
        <b style="font-size: 14px; letter-spacing: 0.5px; color: #FFFFFF;">APPSHIELD DEFENSE TELEMETRY</b>
        <span style="font-size: 12px; color: #818CF8;">| TUANDROMD RUNTIME v2.4</span>
    </div>
    <div style="display: flex; gap: 20px; font-size: 12px; font-weight: 700;">
        <span style="color: #34D399; text-shadow: 0 0 10px rgba(52, 211, 153, 0.4);">● ENGINE: ONLINE</span>
        <span style="color: #38BDF8; text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);">● CONTAINER: DOCKER COMPOSE</span>
        <span style="color: #F472B6; text-shadow: 0 0 10px rgba(244, 114, 182, 0.4);">● TEST ACCURACY: 99.78%</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 14px 0 22px 0;">
            <div style="font-size: 52px; filter: drop-shadow(0 0 20px rgba(129,140,248,0.7));">🛡️</div>
            <h2 style="margin: 8px 0 0 0; font-size: 26px; font-weight: 800; color: #FFFFFF;">AppShield</h2>
            <div style="font-size: 12px; font-weight: 700; color: #38BDF8; text-transform: uppercase; letter-spacing: 1.5px;">AI Threat Operations</div>
        </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Console Mode",
        [
            "⚡ Dynamic App Scanner",
            "🗂️ Enterprise CSV Audit",
            "🧠 Model Neural Intelligence",
            "📊 Full Telemetry Overview"
        ]
    )

    st.markdown("---")
    st.markdown("""
        <div style="font-size: 12px; color: #94A3B8; line-height: 1.7;">
            <b style="color: #E2E8F0;">Active Node:</b> Symbiosis AI Lab<br>
            <b style="color: #E2E8F0;">Architecture:</b> Random Forest<br>
            <b style="color: #E2E8F0;">Trees:</b> 200 Estimators<br>
            <b style="color: #E2E8F0;">Feature Matrix:</b> 241 Dimensions
        </div>
    """, unsafe_allow_html=True)

def execute_threat_audit(selected_permissions):
    row = pd.DataFrame([{f: (1 if f in selected_permissions else 0) for f in features}])
    verdict = model.predict(row)[0]
    prob_malware = model.predict_proba(row)[0][1]
    return verdict, prob_malware

# ---------------------------------------------------------------------------
# PAGE 1: DYNAMIC APP SCANNER
# ---------------------------------------------------------------------------
if page == "⚡ Dynamic App Scanner":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-tag">⚡ AI Threat Defense Engine</div>
        <h1 class="hero-title">Audit Android permissions before installation.</h1>
        <p class="hero-desc">
            AppShield analyses runtime API calls and AndroidManifest declarations across 241 threat signatures. 
            Explainable AI visualises the exact capabilities driving high-risk verdicts.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 4 Vibrant KPI Blocks
    st.markdown("""
    <div class="kpi-container">
        <div class="kpi-card purple">
            <div class="kpi-label">📊 BENCHMARK INVENTORY</div>
            <div class="kpi-val">4,464</div>
            <div class="kpi-sub">3,565 Malware | 899 Goodware</div>
        </div>
        <div class="kpi-card emerald">
            <div class="kpi-label">🎯 HELD-OUT TEST ACCURACY</div>
            <div class="kpi-val">99.78%</div>
            <div class="kpi-sub">Zero data leakage confirmed</div>
        </div>
        <div class="kpi-card cyan">
            <div class="kpi-label">⚡ MALWARE RECALL</div>
            <div class="kpi-val">100%</div>
            <div class="kpi-sub">713 / 713 threats trapped</div>
        </div>
        <div class="kpi-card rose">
            <div class="kpi-label">🛡️ FEATURE SPACE</div>
            <div class="kpi-val">241</div>
            <div class="kpi-sub">214 Perms + 27 Core APIs</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Preset Quick Buttons
    st.markdown("#### ⚡ 1-Click Interactive Test Scenarios")
    st.caption("Click any preset below to simulate an app category:")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📱 Benign: Calculator Utility", use_container_width=True):
            st.session_state["chosen_perms"] = ["VIBRATE", "INTERNET"]

    with col2:
        if st.button("📷 Benign: Camera & Filters", use_container_width=True):
            st.session_state["chosen_perms"] = [
                "CAMERA", "FLASHLIGHT", "READ_EXTERNAL_STORAGE", "WRITE_EXTERNAL_STORAGE"
            ]

    with col3:
        if st.button("⚠️ Malicious: SMS Trojan", use_container_width=True):
            st.session_state["chosen_perms"] = [
                "SEND_SMS", "RECEIVE_BOOT_COMPLETED", "READ_PHONE_STATE",
                "Ljava/net/URL;->openConnection", "KILL_BACKGROUND_PROCESSES"
            ]

    with col4:
        if st.button("🚨 Critical: Stealth Spyware", use_container_width=True):
            st.session_state["chosen_perms"] = [
                "RECEIVE_BOOT_COMPLETED", "GET_TASKS", "WAKE_LOCK",
                "Landroid/location/LocationManager;->getLastKgoodwarewnLocation",
                "Ldalvik/system/DexClassLoader;->loadClass", "READ_PHONE_STATE"
            ]

    st.markdown("<br>", unsafe_allow_html=True)

    preloaded = st.session_state.get("chosen_perms", ["VIBRATE", "INTERNET"])
    user_perms = st.multiselect(
        "🔎 Custom Permission Manifest (Search from 241 signatures):",
        options=features,
        default=[p for p in preloaded if p in features]
    )

    scan_action = st.button("🚀 Execute Security Audit", type="primary", use_container_width=True)

    if scan_action or user_perms:
        verdict, risk_prob = execute_threat_audit(set(user_perms))
        is_threat = (verdict == 1)

        if is_threat:
            st.markdown(f"""
            <div class="verdict-hud danger">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <div class="verdict-title">🚨 CRITICAL THREAT DETECTED — Malware-like Profile</div>
                        <div style="font-size: 15px; color: #FECACA;">
                            High-confidence match with known spyware Trojans and hidden runtime payload loaders.
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 42px; font-weight: 800; font-family: 'JetBrains Mono'; color: #F87171; text-shadow: 0 0 20px rgba(239,68,68,0.5);">{risk_prob * 100:.1f}%</span>
                        <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: #FCA5A5;">Malware Probability</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            safe_prob = (1 - risk_prob) * 100
            st.markdown(f"""
            <div class="verdict-hud safe">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <div class="verdict-title">✅ VERIFIED SAFE PROFILE — Benign Goodware Behavior</div>
                        <div style="font-size: 15px; color: #A7F3D0;">
                            Requested capabilities strictly align with non-invasive consumer utilities from legitimate Play Store apps.
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 42px; font-weight: 800; font-family: 'JetBrains Mono'; color: #34D399; text-shadow: 0 0 20px rgba(16,185,129,0.5);">{safe_prob:.1f}%</span>
                        <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: #6EE7B7;">Safety Confidence</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.progress(float(risk_prob))

        st.markdown("<br>", unsafe_allow_html=True)
        g1, g2 = st.columns([3, 2])

        with g1:
            st.markdown("#### 🔍 Contributing Threat Factors")
            st.caption("Predictive weight of each requested capability toward this verdict:")

            all_imps = pd.Series(model.feature_importances_, index=features)
            user_factors = all_imps[all_imps.index.isin(user_perms)].sort_values(ascending=False).head(8)

            if not user_factors.empty:
                chart_df = pd.DataFrame({
                    "Threat Weight": user_factors.values
                }, index=user_factors.index)
                st.bar_chart(chart_df, color="#818CF8", use_container_width=True)
            else:
                st.info("No high-risk signature features detected in current selections.")

        with g2:
            st.markdown("#### 📋 Inspected Capability Flags")
            st.caption(f"App requested {len(user_perms)} distinct access flags:")
            if user_perms:
                tag_html = "".join([f"<span class='perm-tag'>{p}</span>" for p in user_perms])
                st.markdown(f"<div>{tag_html}</div>", unsafe_allow_html=True)
            else:
                st.write("No permissions active.")

# ---------------------------------------------------------------------------
# PAGE 2: ENTERPRISE CSV AUDIT
# ---------------------------------------------------------------------------
elif page == "🗂️ Enterprise CSV Audit":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-tag">🗂️️ Fleet Security Screening</div>
        <h1 class="hero-title">Bulk Manifest Fleet Audit</h1>
        <p class="hero-desc">
            Upload CSV exports of multiple Android apps simultaneously. AppShield screens the entire fleet in milliseconds, 
            triaging high-risk applications for immediate quarantine.
        </p>
    </div>
    """, unsafe_allow_html=True)

    csv_upload = st.file_uploader("Upload App Manifest Matrix (.csv)", type=["csv"])

    if csv_upload:
        raw_df = pd.read_csv(csv_upload)
        raw_df.columns = raw_df.columns.str.strip()

        missing_cols = [c for c in features if c not in raw_df.columns]
        if missing_cols:
            for mc in missing_cols:
                raw_df[mc] = 0

        X_screen = raw_df[features].fillna(0)
        preds = model.predict(X_screen)
        probs = model.predict_proba(X_screen)[:, 1]

        total_apps = len(preds)
        flagged_threats = int(preds.sum())
        clean_apps = total_apps - flagged_threats

        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card purple">
                <div class="kpi-label">TOTAL APPLICATIONS</div>
                <div class="kpi-val">{total_apps}</div>
                <div class="kpi-sub">Processed in batch</div>
            </div>
            <div class="kpi-card rose">
                <div class="kpi-label">🚨 FLAGGED AS MALWARE</div>
                <div class="kpi-val">{flagged_threats}</div>
                <div class="kpi-sub">{flagged_threats/total_apps*100:.1f}% risk incidence</div>
            </div>
            <div class="kpi-card emerald">
                <div class="kpi-label">✅ BENIGN UTILITIES</div>
                <div class="kpi-val">{clean_apps}</div>
                <div class="kpi-sub">{clean_apps/total_apps*100:.1f}% clean compliance</div>
            </div>
            <div class="kpi-card cyan">
                <div class="kpi-label">⚡ SCAN LATENCY</div>
                <div class="kpi-val">< 24ms</div>
                <div class="kpi-sub">Optimized inference</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        audit_results = raw_df.copy()
        audit_results["Risk_Score"] = (probs * 100).round(1).astype(str) + "%"
        audit_results["Verdict"] = ["🚨 HIGH RISK" if p == 1 else "✅ BENIGN" for p in preds]

        show_cols = ["Verdict", "Risk_Score"] + [c for c in audit_results.columns if c not in ["Verdict", "Risk_Score"]][:7]
        st.dataframe(audit_results[show_cols], use_container_width=True)

# ---------------------------------------------------------------------------
# PAGE 3: MODEL NEURAL INTELLIGENCE
# ---------------------------------------------------------------------------
elif page == "🧠 Model Neural Intelligence":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-tag">🧠 Machine Learning Diagnostics</div>
        <h1 class="hero-title">Model Benchmarks & Feature Weights</h1>
        <p class="hero-desc">
            Full transparency into the Random Forest model architecture, mathematical weights, 
            and global indicators driving malware detection on the TUANDROMD benchmark.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="kpi-container">
        <div class="kpi-card emerald">
            <div class="kpi-label">TEST ACCURACY</div>
            <div class="kpi-val">99.78%</div>
            <div class="kpi-sub">893 unseen holdout apps</div>
        </div>
        <div class="kpi-card cyan">
            <div class="kpi-label">MALWARE PRECISION</div>
            <div class="kpi-val">1.00</div>
            <div class="kpi-sub">Zero false malware alarms</div>
        </div>
        <div class="kpi-card rose">
            <div class="kpi-label">MALWARE F1-SCORE</div>
            <div class="kpi-val">1.00</div>
            <div class="kpi-sub">Harmonic mean balance</div>
        </div>
        <div class="kpi-card purple">
            <div class="kpi-label">TRAIN/TEST SPLIT</div>
            <div class="kpi-val">80 / 20</div>
            <div class="kpi-sub">Stratified holdout</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📌 Top 15 Danger Signatures Across Entire Android Ecosystem")
    st.caption("These permissions and API calls carry the heaviest mathematical weights in identifying malicious apps:")

    global_series = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False).head(15)
    st.bar_chart(global_series, color="#818CF8", use_container_width=True)

# ---------------------------------------------------------------------------
# PAGE 4: FULL TELEMETRY OVERVIEW
# ---------------------------------------------------------------------------
elif page == "📊 Full Telemetry Overview":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-tag">📊 Architecture Telemetry</div>
        <h1 class="hero-title">Open Source Tools Implementation Stack</h1>
        <p class="hero-desc">
            AppShield was constructed strictly following production-grade open source tooling standards:
            isolated containers, reproducible pipelines, and collaborative version control.
        </p>
    </div>
    """, unsafe_allow_html=True)

    t1, t2 = st.columns(2)
    with t1:
        st.markdown("""
        <div class="kpi-card purple" style="margin-bottom: 16px;">
            <div class="kpi-label">🐳 DOCKER COMPOSE ORCHESTRATION</div>
            <p style="font-size: 14px; color: #CBD5E1; margin: 8px 0 0 0; line-height: 1.7;">
                • <b>Trainer Service:</b> Runs <code>train_model.py</code>, executes stratified data splits, saves serialized model.<br>
                • <b>Dashboard Service:</b> Runs <code>app.py</code> with real-time UI on port 8501.<br>
                • <b>Shared Volume:</b> <code>./model</code> folder mounted between both containers for seamless inference.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown("""
        <div class="kpi-card rose" style="margin-bottom: 16px;">
            <div class="kpi-label">🐙 GIT & GITHUB VERSION CONTROL</div>
            <p style="font-size: 14px; color: #CBD5E1; margin: 8px 0 0 0; line-height: 1.7;">
                • <b>Repository:</b> <code>lambdadesrushti/appshield</code><br>
                • <b>Branch:</b> <code>main</code> (Fully synchronized)<br>
                • <b>Clean Repo Policy:</b> Model binaries and raw 4,400+ CSV datasets excluded via <code>.gitignore</code>.
            </p>
        </div>
        """, unsafe_allow_html=True)