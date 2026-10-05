"""
AppShield - Enterprise Technical Security Platform
Senior UI/UX Redesign: High-Signal, Precision Cybersecurity Aesthetic.
"""

import streamlit as st
import pandas as pd
import joblib
import altair as alt
import time

st.set_page_config(
    page_title="AppShield,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================================
# ENTERPRISE CSS: NATIVE LIGHT/DARK MODE DUAL THEME
# =====================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* Dynamic Theme Variables */
:root {
    --bg-main: #F8FAFC;
    --bg-surface: #FFFFFF;
    --bg-surface-alt: #F1F5F9;
    --border-color: #E2E8F0;
    --text-primary: #0F172A;
    --text-secondary: #64748B;
    --text-muted: #94A3B8;
    
    --brand-navy: #1E3A8A;
    --brand-blue: #2563EB;
    --brand-cyan: #0EA5E9;
    
    --status-safe-bg: #F0FDF4;
    --status-safe-border: #86EFAC;
    --status-safe-text: #166534;
    
    --status-danger-bg: #FEF2F2;
    --status-danger-border: #FCA5A5;
    --status-danger-text: #991B1B;
    
    --shadow-sm: 0 1px 2px 0 rgba(15, 23, 42, 0.05);
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-main: #0B1120;
        --bg-surface: #172033;
        --bg-surface-alt: #1E293B;
        --border-color: #334155;
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --text-muted: #475569;
        
        --brand-navy: #3B82F6;
        --brand-blue: #3B82F6;
        --brand-cyan: #38BDF8;
        
        --status-safe-bg: rgba(22, 101, 52, 0.2);
        --status-safe-border: #14532D;
        --status-safe-text: #6EE7B7;
        
        --status-danger-bg: rgba(153, 27, 27, 0.2);
        --status-danger-border: #7F1D1D;
        --status-danger-text: #FCA5A5;
        
        --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
}

/* Nuke Default Streamlit UI */
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
.stDeployButton { display: none !important; }
div[data-testid="stSidebar"] { display: none !important; }

div[data-testid="stAppViewContainer"] > .main > div {
    padding: 2rem 4rem !important;
    max-width: 1400px !important;
}

/* Typography Hierarchy */
.text-mono { font-family: 'JetBrains Mono', monospace; }
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--brand-blue);
    margin-bottom: 8px;
}
.panel-heading {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 16px 0;
    letter-spacing: -0.3px;
}

/* Technical Header */
.tech-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-bottom: 24px;
    margin-bottom: 32px;
    border-bottom: 1px solid var(--border-color);
}
.brand-lockup { display: flex; align-items: center; gap: 12px; }
.brand-mark {
    width: 28px; height: 28px;
    background-color: var(--brand-blue);
    border-radius: 4px;
    display: flex; align-items: center; justify-content: center;
    color: #FFFFFF; font-weight: 800; font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
}
.brand-title {
    font-size: 20px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.5px; margin: 0; line-height: 1;
}
.brand-sub {
    font-size: 12px; color: var(--text-secondary); margin: 4px 0 0 0; font-weight: 500;
}
.system-status {
    display: flex; align-items: center; gap: 8px;
    font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 600;
    color: var(--text-secondary);
}
.status-indicator {
    width: 6px; height: 6px; border-radius: 50%; background-color: var(--brand-blue);
}

/* Seamless Metric Row */
.metric-row {
    display: flex; gap: 48px; margin-bottom: 40px;
}
.metric-item { display: flex; flex-direction: column; gap: 4px; }
.metric-val {
    font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 700; color: var(--text-primary); line-height: 1;
}
.metric-lbl {
    font-size: 12px; font-weight: 500; color: var(--text-secondary);
}

/* Technical Analysis Pipeline Diagram */
.pipeline-container {
    display: flex; justify-content: space-between; align-items: flex-start;
    position: relative; margin: 32px 0 48px 0; padding: 0 20px;
}
.pipeline-line {
    position: absolute; top: 12px; left: 40px; right: 40px; height: 2px;
    background-color: var(--border-color); z-index: 0;
}
.pipeline-step {
    display: flex; flex-direction: column; align-items: center; gap: 12px; z-index: 1; width: 120px; text-align: center;
}
.step-node {
    width: 26px; height: 26px; border-radius: 50%;
    background-color: var(--bg-surface); border: 2px solid var(--border-color);
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; color: var(--text-muted); font-weight: 700; transition: all 0.3s ease;
}
.step-label {
    font-size: 11px; font-weight: 600; color: var(--text-secondary); line-height: 1.3;
}
/* Active Pipeline State */
.pipeline-step.active .step-node {
    border-color: var(--brand-blue); background-color: var(--brand-blue); color: #FFFFFF;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
}
.pipeline-step.active .step-label { color: var(--text-primary); }

/* Diagnostic HUDs */
.diagnostic-hud {
    padding: 24px 32px; border-radius: 8px; border: 1px solid;
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 32px; box-shadow: var(--shadow-sm); background-color: var(--bg-surface);
}
.diagnostic-hud.danger { border-left: 6px solid var(--status-danger-border); border-color: var(--border-color); }
.diagnostic-hud.safe { border-left: 6px solid var(--status-safe-border); border-color: var(--border-color); }

.hud-title { font-size: 18px; font-weight: 700; margin: 0 0 8px 0; }
.diagnostic-hud.danger .hud-title { color: var(--status-danger-text); }
.diagnostic-hud.safe .hud-title { color: var(--status-safe-text); }
.hud-desc { font-size: 14px; color: var(--text-secondary); margin: 0; max-width: 80%; line-height: 1.5; }

.hud-score-block { text-align: right; }
.hud-score { font-family: 'JetBrains Mono', monospace; font-size: 36px; font-weight: 800; line-height: 1; }
.diagnostic-hud.danger .hud-score { color: var(--status-danger-text); }
.diagnostic-hud.safe .hud-score { color: var(--status-safe-text); }
.hud-score-lbl { font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--text-secondary); margin-top: 6px; letter-spacing: 0.5px; }

/* Form Controls & Overrides */
div[data-testid="stButton"] > button {
    border-radius: 6px !important; font-weight: 600 !important; font-size: 13px !important;
    border: 1px solid var(--border-color) !important; background-color: var(--bg-surface) !important;
    color: var(--text-primary) !important; padding: 12px 24px !important; transition: all 0.2s !important;
}
div[data-testid="stButton"] > button:hover { background-color: var(--bg-surface-alt) !important; }
div[data-testid="stButton"] > button[kind="primary"] {
    background-color: var(--brand-blue) !important; color: #FFFFFF !important; border: none !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover { opacity: 0.9 !important; }

/* Multiselect dark/light adaptability */
div[data-baseweb="select"] > div {
    background-color: var(--bg-surface) !important; border-color: var(--border-color) !important;
}

hr { border-color: var(--border-color); margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# BACKEND: MODEL & DATA INITIALIZATION
# =====================================================================
@st.cache_resource(show_spinner=False)
def load_security_engine():
    try:
        return joblib.load("model/model.pkl")
    except Exception:
        return None

bundle = load_security_engine()
if not bundle:
    st.error("System Error: model/model.pkl payload not found. Execute trainer container first.")
    st.stop()

model = bundle["model"]
features = bundle["features"]
sample_malware = bundle.get("sample_malware", ["SEND_SMS", "RECEIVE_BOOT_COMPLETED", "READ_PHONE_STATE", "Ljava/net/URL;->openConnection", "KILL_BACKGROUND_PROCESSES"])
sample_goodware = bundle.get("sample_goodware", ["VIBRATE", "INTERNET", "ACCESS_NETWORK_STATE"])

# =====================================================================
# UI: TECHNICAL HEADER & METRICS
# =====================================================================
st.markdown("""
<div class="tech-header">
    <div class="brand-lockup">
        <div class="brand-mark">AS</div>
        <div>
            <h1 class="brand-title">AppShield Intelligence</h1>
            <p class="brand-sub">AI-Powered Android Security & Malware Analysis Platform</p>
        </div>
    </div>
    <div class="system-status">
        <span class="status-indicator"></span> ENGINE ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="metric-row">
    <div class="metric-item">
        <div class="metric-val">99.78%</div>
        <div class="metric-lbl">Model Accuracy</div>
    </div>
    <div class="metric-item">
        <div class="metric-val">4,464</div>
        <div class="metric-lbl">Targets Analyzed</div>
    </div>
    <div class="metric-item">
        <div class="metric-val">241</div>
        <div class="metric-lbl">Extracted Features</div>
    </div>
    <div class="metric-item">
        <div class="metric-val">Random Forest</div>
        <div class="metric-lbl">Architecture Type</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# UI: SPLIT PANE ANALYSIS ARCHITECTURE
# =====================================================================
input_col, output_col = st.columns([1, 1.4], gap="large")

with input_col:
    st.markdown('<div class="section-label">Target Config</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="panel-heading">Manifest & API Extraction</h2>', unsafe_allow_html=True)
    
    st.caption("Load a standard behavioral profile or configure custom permission vectors.")
    c1, c2 = st.columns(2)
    if c1.button("Load Safe Utility", use_container_width=True):
        st.session_state["active_payload"] = sample_goodware
    if c2.button("Load SMS Trojan", use_container_width=True):
        st.session_state["active_payload"] = sample_malware
        
    default_payload = st.session_state.get("active_payload", sample_goodware)
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    user_payload = st.multiselect(
        "Feature Vectors (Search 241 indices)",
        options=features,
        default=[p for p in default_payload if p in features]
    )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    execute_btn = st.button("Execute Technical Analysis", type="primary", use_container_width=True)

with output_col:
    st.markdown('<div class="section-label">Analysis Output</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="panel-heading">Security Diagnostic Result</h2>', unsafe_allow_html=True)
    
    # State tracking for the Pipeline Animation
    is_scanned = execute_btn or len(user_payload) > 0
    
    # -----------------------------------------------------------------
    # VISUAL COMPONENT: TECHNICAL ANALYSIS FLOW
    # -----------------------------------------------------------------
    pipeline_active = "active" if is_scanned else ""
    st.markdown(f"""
    <div class="pipeline-container">
        <div class="pipeline-line"></div>
        <div class="pipeline-step {pipeline_active}">
            <div class="step-node">1</div>
            <div class="step-label">Manifest<br>Input</div>
        </div>
        <div class="pipeline-step {pipeline_active}">
            <div class="step-node">2</div>
            <div class="step-label">Vector<br>Extraction</div>
        </div>
        <div class="pipeline-step {pipeline_active}">
            <div class="step-node">3</div>
            <div class="step-label">ML<br>Processing</div>
        </div>
        <div class="pipeline-step {pipeline_active}">
            <div class="step-node">4</div>
            <div class="step-label">Threat<br>Classification</div>
        </div>
        <div class="pipeline-step {pipeline_active}">
            <div class="step-node">5</div>
            <div class="step-label">Final<br>Diagnostic</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if execute_btn:
        with st.spinner("Processing vector extraction and ensemble classification..."):
            time.sleep(0.6) # Simulated processing time for UX weight
            
    if is_scanned:
        # Machine Learning Inference
        df_target = pd.DataFrame([{f: (1 if f in user_payload else 0) for f in features}])
        pred = model.predict(df_target)[0]
        prob = model.predict_proba(df_target)[0][1]

        # -------------------------------------------------------------
        # VISUAL COMPONENT: RESULT HUD
        # -------------------------------------------------------------
        if pred == 1:
            st.markdown(f"""
            <div class="diagnostic-hud danger">
                <div>
                    <h3 class="hud-title">Critical Threat Detected</h3>
                    <p class="hud-desc">The extracted permission vectors strongly correlate with known malware behaviors, privilege escalation, or unauthorized data exfiltration.</p>
                </div>
                <div class="hud-score-block">
                    <div class="hud-score">{prob*100:.1f}%</div>
                    <div class="hud-score-lbl">Threat Probability</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="diagnostic-hud safe">
                <div>
                    <h3 class="hud-title">Safe Profile Verified</h3>
                    <p class="hud-desc">The requested application capabilities align with standard, benign utility parameters. No anomalous signatures detected.</p>
                </div>
                <div class="hud-score-block">
                    <div class="hud-score">{(1-prob)*100:.1f}%</div>
                    <div class="hud-score-lbl">Safety Confidence</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # -------------------------------------------------------------
        # VISUAL COMPONENT: DATA VISUALIZATION
        # -------------------------------------------------------------
        st.markdown('<div class="section-label" style="margin-top: 24px;">Interpretability</div>', unsafe_allow_html=True)
        st.markdown('<h2 class="panel-heading" style="font-size:14px; color:var(--text-secondary);">Predictive Feature Contributions</h2>', unsafe_allow_html=True)
        
        all_importances = pd.Series(model.feature_importances_, index=features)
        target_factors = all_importances[all_importances.index.isin(user_payload)].sort_values(ascending=False).head(5)

        if not target_factors.empty:
            df_chart = pd.DataFrame({
                "Vector": target_factors.index, 
                "Severity Weight": target_factors.values
            })
            
            # Professionally styled Altair Bar Chart
            # Uses variable color mapping to adapt to Light/Dark mode via Streamlit's native rendering
            chart = alt.Chart(df_chart).mark_bar(
                color="#3B82F6" if pred == 0 else "#EF4444", 
                height=20,
                cornerRadiusEnd=2
            ).encode(
                x=alt.X("Severity Weight:Q", axis=None),
                y=alt.Y("Vector:N", sort="-x", title=None, 
                        axis=alt.Axis(labelFont="JetBrains Mono", labelFontSize=11, tickColor="transparent", domainColor="transparent")),
                tooltip=["Vector", "Severity Weight"]
            ).properties(
                height=220
            ).configure_view(
                strokeOpacity=0
            )
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.markdown("<p style='font-size: 13px; color: var(--text-muted);'>No high-severity vectors present in the current payload.</p>", unsafe_allow_html=True)

    else:
        # Professional Empty State
        st.markdown("""
        <div style="border: 1px dashed var(--border-color); border-radius: 8px; padding: 48px 24px; text-align: center; background-color: var(--bg-surface);">
            <div style="font-size: 24px; color: var(--text-muted); margin-bottom: 12px;">⌖</div>
            <div style="font-size: 14px; font-weight: 600; color: var(--text-secondary); margin-bottom: 4px;">AWAITING MANIFEST INPUT</div>
            <p style="font-size: 13px; color: var(--text-muted); margin: 0;">Configure target features and execute analysis to view diagnostic pipeline.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)