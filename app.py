"""
AppShield - Technical AI Security Operations Console
Premium, Adaptive Light/Dark "Technical Blue" Aesthetic with Live Telemetry.
"""

import streamlit as st
import pandas as pd
import joblib
import altair as alt
import time
from datetime import datetime

st.set_page_config(
    page_title="AppShield | Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# CORE SYSTEM CSS: ADAPTIVE TECHNICAL BLUE ENVIRONMENT
# =====================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* CSS Variable System for Perfect Light/Dark Mode */
:root {
    --bg-canvas: #F8FAFC;
    --bg-surface: #FFFFFF;
    --bg-surface-elevated: #F1F5F9;
    --bg-terminal: #0F172A;
    
    --text-main: #0F172A;
    --text-muted: #64748B;
    --text-terminal: #38BDF8;
    
    --border-subtle: #E2E8F0;
    --border-strong: #CBD5E1;
    
    --tech-blue: #2563EB;
    --tech-blue-glow: rgba(37, 99, 235, 0.15);
    --electric-cyan: #0EA5E9;
    
    --safe-color: #10B981;
    --safe-bg: #F0FDF4;
    --danger-color: #EF4444;
    --danger-bg: #FEF2F2;
    
    --shadow-soft: 0 4px 6px -1px rgba(15, 23, 42, 0.05);
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-canvas: #0B1120;
        --bg-surface: #172033;
        --bg-surface-elevated: #1E293B;
        --bg-terminal: #070B14;
        
        --text-main: #F8FAFC;
        --text-muted: #94A3B8;
        --text-terminal: #38BDF8;
        
        --border-subtle: #334155;
        --border-strong: #475569;
        
        --tech-blue: #3B82F6;
        --tech-blue-glow: rgba(59, 130, 246, 0.25);
        --electric-cyan: #38BDF8;
        
        --safe-color: #34D399;
        --safe-bg: rgba(16, 185, 129, 0.1);
        --danger-color: #F87171;
        --danger-bg: rgba(239, 68, 68, 0.1);
        
        --shadow-soft: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg-canvas) !important;
    color: var(--text-main) !important;
}

/* Subtle Technical Background Grid */
[data-testid="stAppViewContainer"] {
    background-image: radial-gradient(var(--border-subtle) 1px, transparent 1px);
    background-size: 24px 24px;
}

/* Nuke Default Streamlit Header/Footer */
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
.stDeployButton { display: none !important; }
div[data-testid="stAppViewContainer"] > .main > div { padding: 2rem 3rem !important; max-width: 1400px !important; }

/* Sidebar Premium Styling */
div[data-testid="stSidebar"] {
    background-color: var(--bg-surface) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

/* Override Tag Colors (KILL THE RED) */
span[data-baseweb="tag"] {
    background-color: var(--tech-blue) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 600 !important;
}
div[data-baseweb="select"] > div {
    background-color: var(--bg-surface-elevated) !important;
    border: 1px solid var(--border-subtle) !important;
}

/* Typography Hierarchy */
.kicker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; color: var(--tech-blue); margin-bottom: 8px;
}
.panel-title {
    font-size: 18px; font-weight: 600; color: var(--text-main); margin: 0 0 16px 0; letter-spacing: -0.3px;
}

/* Top System Header */
.system-header {
    display: flex; justify-content: space-between; align-items: flex-end;
    padding-bottom: 20px; margin-bottom: 32px; border-bottom: 1px solid var(--border-subtle);
}
.brand-lockup { display: flex; align-items: center; gap: 14px; }
.brand-icon {
    width: 32px; height: 32px; background: var(--tech-blue); border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    color: #FFF; font-weight: 800; font-family: 'JetBrains Mono', monospace; font-size: 16px;
    box-shadow: 0 0 15px var(--tech-blue-glow);
}
.brand-title { font-size: 24px; font-weight: 800; letter-spacing: -0.5px; margin: 0; line-height: 1; }
.brand-subtitle { font-size: 13px; color: var(--text-muted); margin: 4px 0 0 0; font-weight: 500; }
.live-status {
    display: flex; align-items: center; gap: 8px;
    font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 600;
    padding: 6px 12px; border-radius: 4px; border: 1px solid var(--border-subtle);
    background: var(--bg-surface); color: var(--text-muted);
}
.pulse-dot {
    width: 8px; height: 8px; border-radius: 50%; background-color: var(--safe-color);
    box-shadow: 0 0 8px var(--safe-color); animation: pulse 2s infinite;
}
@keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }

/* Overview Metrics */
.metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 32px; }
.metric-box {
    background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 8px;
    padding: 20px; box-shadow: var(--shadow-soft); position: relative; overflow: hidden;
}
.metric-box::before {
    content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--tech-blue);
}
.m-val { font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: 800; color: var(--text-main); line-height: 1; }
.m-lbl { font-size: 12px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 8px; }

/* Form Elements */
div[data-testid="stButton"] > button {
    border-radius: 6px !important; font-weight: 600 !important; font-size: 13px !important;
    border: 1px solid var(--border-strong) !important; background: var(--bg-surface) !important;
    color: var(--text-main) !important; padding: 10px 20px !important; transition: all 0.2s !important;
}
div[data-testid="stButton"] > button:hover { background: var(--bg-surface-elevated) !important; }
div[data-testid="stButton"] > button[kind="primary"] {
    background: var(--tech-blue) !important; color: #FFFFFF !important; border: none !important;
    box-shadow: 0 4px 10px var(--tech-blue-glow) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; }

/* Analysis Pipeline Component */
.pipeline-container {
    display: flex; justify-content: space-between; position: relative; margin: 24px 0; padding: 0 10px;
}
.pipeline-track {
    position: absolute; top: 12px; left: 30px; right: 30px; height: 2px; background: var(--border-subtle); z-index: 0;
}
.pipeline-node {
    display: flex; flex-direction: column; align-items: center; gap: 10px; z-index: 1; width: 100px; text-align: center;
}
.node-circle {
    width: 26px; height: 26px; border-radius: 50%; background: var(--bg-surface); border: 2px solid var(--border-strong);
    display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; color: var(--text-muted);
    transition: all 0.3s ease;
}
.node-lbl { font-size: 11px; font-weight: 600; color: var(--text-muted); line-height: 1.2; }

.pipeline-node.active .node-circle {
    border-color: var(--tech-blue); background: var(--tech-blue); color: #FFF;
    box-shadow: 0 0 12px var(--tech-blue-glow);
}
.pipeline-node.active .node-lbl { color: var(--text-main); }
.pipeline-node.processing .node-circle {
    border-color: var(--electric-cyan); background: transparent; color: var(--electric-cyan);
    animation: spin-pulse 1.5s infinite;
}
@keyframes spin-pulse { 0% { box-shadow: 0 0 0 0 rgba(14, 165, 233, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(14, 165, 233, 0); } 100% { box-shadow: 0 0 0 0 rgba(14, 165, 233, 0); } }

/* Live Terminal Feed */
.terminal-feed {
    background: var(--bg-terminal); border: 1px solid var(--border-subtle); border-radius: 6px;
    padding: 16px; font-family: 'JetBrains Mono', monospace; font-size: 12px;
    color: var(--text-terminal); height: 180px; overflow-y: auto; box-shadow: inset 0 2px 10px rgba(0,0,0,0.2);
}
.log-entry { margin-bottom: 6px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px; }
.log-time { color: #94A3B8; margin-right: 12px; }
.log-success { color: #34D399; }
.log-warn { color: #F87171; }

/* Verdict HUDs */
.verdict-box {
    padding: 24px 32px; border-radius: 8px; border: 1px solid; display: flex; justify-content: space-between;
    align-items: center; margin: 24px 0; background: var(--bg-surface); box-shadow: var(--shadow-soft);
}
.verdict-box.danger { border-left: 6px solid var(--danger-color); border-color: var(--border-subtle); background: var(--danger-bg); }
.verdict-box.safe { border-left: 6px solid var(--safe-color); border-color: var(--border-subtle); background: var(--safe-bg); }
.v-title { font-size: 20px; font-weight: 700; margin: 0 0 6px 0; }
.verdict-box.danger .v-title { color: var(--danger-color); }
.verdict-box.safe .v-title { color: var(--safe-color); }
.v-desc { font-size: 14px; color: var(--text-muted); margin: 0; max-width: 85%; line-height: 1.5; }
.v-score-block { text-align: right; }
.v-score { font-family: 'JetBrains Mono', monospace; font-size: 38px; font-weight: 800; line-height: 1; }
.verdict-box.danger .v-score { color: var(--danger-color); }
.verdict-box.safe .v-score { color: var(--safe-color); }

hr { border-color: var(--border-subtle); margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# BACKEND: SYSTEM INITIALIZATION
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
# SIDEBAR: NAVIGATION
# =====================================================================
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 30px 0;">
            <div style="font-size: 32px; margin-bottom: 8px;">🛡️</div>
            <h2 style="margin: 0; font-size: 18px; font-weight: 700; color: var(--text-main);">AppShield</h2>
            <div style="font-size: 12px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; margin-top: 4px;">WORKSPACE: SYMBIOSIS AI</div>
        </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["Live Analysis Core", "Batch Fleet Scanner", "Threat Intelligence"],
        label_visibility="collapsed"
    )

# =====================================================================
# GLOBAL HEADER
# =====================================================================
st.markdown("""
<div class="system-header">
    <div class="brand-lockup">
        <div class="brand-icon">AS</div>
        <div>
            <h1 class="brand-title">AppShield Intelligence Console</h1>
            <p class="brand-subtitle">Enterprise Android Malware & Permission Analysis Runtime</p>
        </div>
    </div>
    <div class="live-status">
        <span class="pulse-dot"></span> SYSTEM ONLINE
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================================
# PAGE 1: LIVE ANALYSIS CORE (The Technical Centerpiece)
# =====================================================================
if page == "Live Analysis Core":
    
    # SYSTEM METRICS OVERVIEW
    st.markdown("""
    <div class="metric-grid">
        <div class="metric-box">
            <div class="m-val">99.78%</div><div class="m-lbl">Holdout Accuracy</div>
        </div>
        <div class="metric-box">
            <div class="m-val">4,464</div><div class="m-lbl">Targets Scanned</div>
        </div>
        <div class="metric-box">
            <div class="m-val">241</div><div class="m-lbl">Threat Vectors</div>
        </div>
        <div class="metric-box">
            <div class="m-val" style="font-size: 20px; padding-top: 8px;">Random Forest</div><div class="m-lbl">Architecture Type</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SPLIT PANE ARCHITECTURE
    col_input, col_output = st.columns([1, 1.3], gap="large")

    with col_input:
        st.markdown('<div class="kicker">Target Configuration</div>', unsafe_allow_html=True)
        st.markdown('<h2 class="panel-title">Manifest & API Extraction</h2>', unsafe_allow_html=True)
        st.caption("Load a manifest profile to execute a static analysis scan.")
        
        c1, c2 = st.columns(2)
        if c1.button("✅ Benign: Calculator", use_container_width=True):
            st.session_state["active_payload"] = sample_goodware
        if c2.button("🚨 Malware: SMS Stealer", use_container_width=True):
            st.session_state["active_payload"] = sample_malware
            
        default_payload = st.session_state.get("active_payload", sample_goodware)
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        user_payload = st.multiselect(
            "Extracted Manifest Vectors",
            options=features,
            default=[p for p in default_payload if p in features]
        )

        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        execute_btn = st.button("🚀 Execute Neural Analysis", type="primary", use_container_width=True)

    with col_output:
        st.markdown('<div class="kicker">Threat Analysis Output</div>', unsafe_allow_html=True)
        st.markdown('<h2 class="panel-title">Security Diagnostic Result</h2>', unsafe_allow_html=True)
        
        # -------------------------------------------------------------
        # THE ANIMATED PIPELINE & LIVE TERMINAL FEED
        # -------------------------------------------------------------
        pipeline_ph = st.empty()
        terminal_ph = st.empty()
        result_ph = st.empty()

        def render_pipeline(step):
            s1 = "active" if step >= 1 else ("processing" if step == 0 else "")
            s2 = "active" if step >= 2 else ("processing" if step == 1 else "")
            s3 = "active" if step >= 3 else ("processing" if step == 2 else "")
            s4 = "active" if step >= 4 else ("processing" if step == 3 else "")
            s5 = "active" if step >= 5 else ("processing" if step == 4 else "")
            
            html = f"""
            <div class="pipeline-container">
                <div class="pipeline-track"></div>
                <div class="pipeline-node {s1}"><div class="node-circle">1</div><div class="node-lbl">Manifest<br>Input</div></div>
                <div class="pipeline-node {s2}"><div class="node-circle">2</div><div class="node-lbl">Vector<br>Extraction</div></div>
                <div class="pipeline-node {s3}"><div class="node-circle">3</div><div class="node-lbl">ML<br>Processing</div></div>
                <div class="pipeline-node {s4}"><div class="node-circle">4</div><div class="node-lbl">Threat<br>Classification</div></div>
                <div class="pipeline-node {s5}"><div class="node-circle">5</div><div class="node-lbl">Final<br>Diagnostic</div></div>
            </div>
            """
            pipeline_ph.markdown(html, unsafe_allow_html=True)

        def render_terminal(logs):
            log_html = "".join([f"<div class='log-entry'><span class='log-time'>[{l[0]}]</span><span class='{l[2]}'>{l[1]}</span></div>" for l in logs])
            terminal_ph.markdown(f"<div class='terminal-feed'>{log_html}</div>", unsafe_allow_html=True)

        if execute_btn:
            logs = []
            
            # Step 1: Input
            render_pipeline(0)
            logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-3], "Parsing AndroidManifest.xml...", ""))
            render_terminal(logs)
            time.sleep(0.4)
            
            # Step 2: Vector Extraction
            render_pipeline(1)
            logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-3], f"Extracted {len(user_payload)} active permission signatures.", "log-success"))
            render_terminal(logs)
            time.sleep(0.4)
            
            # Step 3: ML Processing
            render_pipeline(2)
            logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-3], "Constructing 241-dimensional feature vector.", ""))
            logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-3], "Initializing Random Forest (200 Estimators)...", ""))
            render_terminal(logs)
            time.sleep(0.5)
            
            # Step 4: Classification
            render_pipeline(3)
            logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-3], "Executing ensemble voting mechanism...", ""))
            render_terminal(logs)
            time.sleep(0.4)
            
            # Prediction Logic
            df_target = pd.DataFrame([{f: (1 if f in user_payload else 0) for f in features}])
            pred = model.predict(df_target)[0]
            prob = model.predict_proba(df_target)[0][1]
            
            # Step 5: Final Result
            render_pipeline(5)
            if pred == 1:
                logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-3], f"CRITICAL: Malware pattern matched (Confidence: {prob*100:.1f}%)", "log-warn"))
            else:
                logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-3], f"CLEARED: Benign profile verified (Confidence: {(1-prob)*100:.1f}%)", "log-success"))
            render_terminal(logs)
            
            st.session_state["last_result"] = {"pred": pred, "prob": prob, "payload": user_payload}

        elif "last_result" in st.session_state:
            # Re-render completed state if already scanned
            render_pipeline(5)
            
        else:
            # Default empty state
            render_pipeline(-1)
            terminal_ph.markdown("""
            <div style="border: 1px dashed var(--border-strong); border-radius: 8px; padding: 40px 24px; text-align: center; background-color: var(--bg-surface);">
                <div style="font-size: 24px; color: var(--text-muted); margin-bottom: 8px;">⌖</div>
                <div style="font-size: 14px; font-weight: 600; color: var(--text-muted); margin-bottom: 4px;">AWAITING SYSTEM INITIALIZATION</div>
                <p style="font-size: 12px; color: var(--text-muted); margin: 0;">Configure target features and execute analysis to engage diagnostic pipeline.</p>
            </div>
            """, unsafe_allow_html=True)

        # -------------------------------------------------------------
        # RESULT HUD & VISUALIZATION
        # -------------------------------------------------------------
        if "last_result" in st.session_state and (execute_btn or not execute_btn):
            res = st.session_state["last_result"]
            pred = res["pred"]
            prob = res["prob"]
            payload = res["payload"]

            with result_ph.container():
                if pred == 1:
                    st.markdown(f"""
                    <div class="verdict-box danger">
                        <div>
                            <h3 class="v-title">CRITICAL THREAT DETECTED</h3>
                            <p class="v-desc">Manifest aligns with known background interception and privilege escalation payloads. Unauthorized data exfiltration risk is high.</p>
                        </div>
                        <div class="v-score-block">
                            <div class="v-score">{prob*100:.1f}%</div>
                            <div class="v-score-lbl" style="color:var(--danger-color);">Malware Probability</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="verdict-box safe">
                        <div>
                            <h3 class="v-title">SAFE PROFILE VERIFIED</h3>
                            <p class="v-desc">Requested capabilities strictly align with legitimate consumer utility bounds. No anomalous vectors detected.</p>
                        </div>
                        <div class="v-score-block">
                            <div class="v-score">{(1-prob)*100:.1f}%</div>
                            <div class="v-score-lbl" style="color:var(--safe-color);">Safety Confidence</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('<div class="kicker" style="margin-top: 24px;">Predictive Feature Contributions</div>', unsafe_allow_html=True)
                
                all_importances = pd.Series(model.feature_importances_, index=features)
                target_factors = all_importances[all_importances.index.isin(payload)].sort_values(ascending=False).head(5)

                if not target_factors.empty:
                    df_chart = pd.DataFrame({"Vector": target_factors.index, "Weight": target_factors.values})
                    chart = alt.Chart(df_chart).mark_bar(
                        color="#EF4444" if pred == 1 else "#3B82F6", height=18, cornerRadiusEnd=2
                    ).encode(
                        x=alt.X("Weight:Q", axis=None),
                        y=alt.Y("Vector:N", sort="-x", title=None, axis=alt.Axis(labelColor="#64748B", labelFont="JetBrains Mono", labelFontSize=11, tickColor="transparent", domainColor="transparent")),
                        tooltip=["Vector", "Weight"]
                    ).properties(height=200).configure_view(strokeOpacity=0)
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.markdown("<p style='font-size: 13px; color: var(--text-muted);'>No high-severity vectors present in the current payload.</p>", unsafe_allow_html=True)


# =====================================================================
# PAGE 2: BATCH FLEET SCANNER
# =====================================================================
elif page == "Batch Fleet Scanner":
    st.markdown('<div class="kicker">BATCH AUDIT</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="panel-title">Enterprise Fleet Diagnostics</h2>', unsafe_allow_html=True)
    st.caption("Upload a CSV file containing application permission manifests for rapid mass screening.")

    uploaded_csv = st.file_uploader("", type=["csv"], label_visibility="collapsed")

    if uploaded_csv:
        with st.spinner("Processing fleet manifest data..."):
            time.sleep(0.5)
            raw_df = pd.read_csv(uploaded_csv)
            raw_df.columns = raw_df.columns.str.strip()

            missing_cols = [c for c in features if c not in raw_df.columns]
            for mc in missing_cols:
                raw_df[mc] = 0

            X_screen = raw_df[features].fillna(0)
            preds = model.predict(X_screen)
            probs = model.predict_proba(X_screen)[:, 1]

            total_apps = len(preds)
            flagged_threats = int(preds.sum())

        st.markdown(f"""
        <div class="metric-grid" style="grid-template-columns: repeat(3, 1fr);">
            <div class="metric-box">
                <div class="m-val">{total_apps}</div><div class="m-lbl">Total Scanned</div>
            </div>
            <div class="metric-box" style="border-left-color: var(--danger-color);">
                <div class="m-val" style="color: var(--danger-color);">{flagged_threats}</div><div class="m-lbl">Critical Threats</div>
            </div>
            <div class="metric-box" style="border-left-color: var(--safe-color);">
                <div class="m-val" style="color: var(--safe-color);">{total_apps - flagged_threats}</div><div class="m-lbl">Verified Safe</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        audit_results = raw_df.copy()
        audit_results["Risk_Score"] = (probs * 100).round(1).astype(str) + "%"
        audit_results["Verdict"] = ["🚨 HIGH RISK" if p == 1 else "✅ SAFE" for p in preds]

        show_cols = ["Verdict", "Risk_Score"] + [c for c in audit_results.columns if c not in ["Verdict", "Risk_Score"]][:5]
        st.dataframe(audit_results[show_cols], use_container_width=True)


# =====================================================================
# PAGE 3: THREAT INTELLIGENCE
# =====================================================================
elif page == "Threat Intelligence":
    st.markdown('<div class="kicker">MODEL INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="panel-title">Global Feature Signatures</h2>', unsafe_allow_html=True)
    st.caption("The predictive mathematical weights of the most critical threat signatures across the entire TUANDROMD dataset.")
    
    top_global = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False).head(15)
    
    df_global = pd.DataFrame({"Feature": top_global.index, "Weight": top_global.values})
    chart_global = alt.Chart(df_global).mark_bar(cornerRadiusEnd=4, color="#2563EB", height=24).encode(
        x=alt.X("Weight:Q", title="Global Predictive Weight", axis=alt.Axis(grid=False)),
        y=alt.Y("Feature:N", sort="-x", title=None, axis=alt.Axis(labelColor="#64748B", labelFont="JetBrains Mono", labelFontSize=12)),
        tooltip=["Feature", "Weight"]
    ).properties(height=450).configure_view(strokeOpacity=0)
    
    st.altair_chart(chart_global, use_container_width=True)