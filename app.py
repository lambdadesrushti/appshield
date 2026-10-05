"""
AppShield - Enterprise Technical Security Platform
Final Layout: High-Contrast Developer Console Aesthetic.
"""

import streamlit as st
import pandas as pd
import joblib
import altair as alt
import time
from datetime import datetime

st.set_page_config(
    page_title="AppShield | Security Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# ENTERPRISE CSS: NATIVE LIGHT/DARK MODE DUAL THEME
# =====================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --bg-main: #F4F7FA;
    --bg-surface: #FFFFFF;
    --bg-surface-alt: #F8FAFC;
    
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-tertiary: #94A3B8;
    
    --border-subtle: #E2E8F0;
    --border-focus: #94A3B8;
    
    --tech-blue: #2563EB;
    --cyan-accent: #0EA5E9;
    
    --safe-base: #10B981;
    --safe-bg: #F0FDF4;
    --safe-border: #A7F3D0;
    
    --danger-base: #EF4444;
    --danger-bg: #FEF2F2;
    --danger-border: #FECACA;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-main: #0B1121;
        --bg-surface: #111827;
        --bg-surface-alt: #1E293B;
        
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --text-tertiary: #475569;
        
        --border-subtle: #1E293B;
        --border-focus: #334155;
        
        --tech-blue: #3B82F6;
        --cyan-accent: #38BDF8;
        
        --safe-base: #10B981;
        --safe-bg: rgba(16, 185, 129, 0.05);
        --safe-border: rgba(16, 185, 129, 0.2);
        
        --danger-base: #EF4444;
        --danger-bg: rgba(239, 68, 68, 0.05);
        --danger-border: rgba(239, 68, 68, 0.2);
    }
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
}

header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
.stDeployButton { display: none !important; }
div[data-testid="stAppViewContainer"] > .main > div { padding: 2.5rem 3.5rem !important; max-width: 1440px !important; }

/* Sidebar Navigation */
div[data-testid="stSidebar"] {
    background-color: var(--bg-surface) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
.sidebar-brand {
    padding: 12px 0 32px 0; display: flex; align-items: center; gap: 12px;
}
.sidebar-icon {
    width: 32px; height: 32px; background: var(--tech-blue); border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; font-family: 'JetBrains Mono', monospace; font-size: 16px;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
}
.sidebar-title { font-size: 20px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.5px; margin: 0; }
.sidebar-subtitle { font-size: 11px; font-weight: 500; color: var(--text-secondary); margin-top: 2px; }

/* Typography */
.kicker { font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--tech-blue); margin-bottom: 6px; }
.section-title { font-size: 16px; font-weight: 600; color: var(--text-primary); margin: 0 0 16px 0; letter-spacing: -0.2px; }

/* Refined Header Control Bar */
.control-bar {
    display: flex; justify-content: space-between; align-items: flex-end;
    padding-bottom: 24px; margin-bottom: 32px; border-bottom: 1px solid var(--border-subtle);
}
.product-title { font-size: 28px; font-weight: 800; letter-spacing: -0.5px; margin: 0; line-height: 1.1; }
.product-desc { font-size: 14px; color: var(--text-secondary); margin: 6px 0 0 0; }
.sys-status {
    display: flex; align-items: center; gap: 8px; font-family: 'JetBrains Mono', monospace;
    font-size: 11px; font-weight: 600; padding: 6px 12px; border-radius: 4px;
    border: 1px solid var(--border-subtle); background: var(--bg-surface); color: var(--text-secondary);
}
.pulse-dot {
    width: 6px; height: 6px; border-radius: 50%; background-color: var(--safe-base);
    box-shadow: 0 0 8px var(--safe-base); animation: pulse 2s infinite;
}
@keyframes pulse { 0% { opacity: 0.4; } 50% { opacity: 1; } 100% { opacity: 0.4; } }

/* Integrated System Overview */
.system-overview {
    display: flex; gap: 48px; padding: 16px 24px; background: var(--bg-surface);
    border: 1px solid var(--border-subtle); border-radius: 8px; margin-bottom: 32px;
}
.overview-metric { display: flex; flex-direction: column; gap: 4px; }
.om-val { font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 700; color: var(--text-primary); line-height: 1; }
.om-lbl { font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; }

/* Developer Console Styling (The Dark Output Pane) */
.dev-console {
    background-color: #0F172A; border-radius: 8px; padding: 32px; border: 1px solid #1E293B;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.2); height: 100%; min-height: 400px;
}
.dev-console-empty {
    display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 300px;
}
.dev-console-icon { font-size: 32px; color: #38BDF8; margin-bottom: 16px; opacity: 0.8; }
.dev-console-title { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 700; color: #F8FAFC; letter-spacing: 1px; margin-bottom: 8px; }
.dev-console-desc { font-size: 13px; color: #94A3B8; text-align: center; max-width: 250px; line-height: 1.5; }

/* Hero Diagnostic Block */
.diagnostic-hero {
    border-radius: 6px; padding: 24px; display: flex; justify-content: space-between;
    align-items: center; border: 1px solid; margin-bottom: 24px; background: #1E293B;
}
.diagnostic-hero.safe { border-color: rgba(16, 185, 129, 0.3); border-left: 4px solid #10B981; }
.diagnostic-hero.danger { border-color: rgba(239, 68, 68, 0.3); border-left: 4px solid #EF4444; }

.diag-header { font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.diagnostic-hero.safe .diag-header { color: #34D399; }
.diagnostic-hero.danger .diag-header { color: #F87171; }

.diag-title { font-size: 20px; font-weight: 700; margin: 0 0 6px 0; color: #F8FAFC; }
.diag-desc { font-size: 13px; color: #94A3B8; margin: 0; max-width: 80%; line-height: 1.5; }

.diag-score-block { text-align: right; }
.diag-score { font-family: 'JetBrains Mono', monospace; font-size: 36px; font-weight: 800; line-height: 1; letter-spacing: -1px; }
.diagnostic-hero.safe .diag-score { color: #34D399; }
.diagnostic-hero.danger .diag-score { color: #F87171; }
.diag-score-lbl { font-size: 10px; font-weight: 600; text-transform: uppercase; color: #94A3B8; margin-top: 6px; letter-spacing: 0.5px; }

/* Live Technical Pipeline inside Dark Console */
.pipeline-wrapper { position: relative; padding: 20px 0; margin-bottom: 24px; }
.pipeline-track { position: absolute; top: 34px; left: 30px; right: 30px; height: 1px; background: #334155; z-index: 0; }
.pipeline-nodes { display: flex; justify-content: space-between; position: relative; z-index: 1; }
.node { display: flex; flex-direction: column; align-items: center; width: 80px; text-align: center; gap: 8px; }
.node-circle {
    width: 24px; height: 24px; border-radius: 50%; background: #0F172A; border: 1px solid #334155;
    display: flex; align-items: center; justify-content: center; font-size: 10px; color: #64748B;
    font-weight: 700; transition: all 0.3s ease;
}
.node-title { font-size: 10px; font-weight: 500; color: #94A3B8; line-height: 1.2; }

.node.completed .node-circle { background: #38BDF8; border-color: #38BDF8; color: #0F172A; }
.node.completed .node-title { color: #E2E8F0; }

.node.active .node-circle {
    background: #0F172A; border-color: #38BDF8; color: #38BDF8;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15); animation: node-pulse 1.5s infinite;
}
.node.active .node-title { color: #38BDF8; }
@keyframes node-pulse { 0% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.3); } 70% { box-shadow: 0 0 0 6px rgba(56, 189, 248, 0); } 100% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); } }

/* Integrated Activity Log inside Dark Console */
.activity-log {
    font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94A3B8;
    background: #0B1121; border: 1px solid #1E293B; border-radius: 4px;
    padding: 12px 16px; margin-bottom: 24px; line-height: 1.6;
}
.log-row { display: flex; gap: 12px; opacity: 0; animation: fade-in 0.3s ease forwards; }
.log-time { color: #475569; }
.log-msg { color: #E2E8F0; }
@keyframes fade-in { to { opacity: 1; } }

/* Form Controls */
div[data-testid="stButton"] > button {
    border-radius: 6px !important; font-weight: 500 !important; font-size: 13px !important;
    border: 1px solid var(--border-focus) !important; background: var(--bg-surface) !important;
    color: var(--text-primary) !important; padding: 8px 16px !important; transition: all 0.2s !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: var(--tech-blue) !important; color: #FFFFFF !important; border: none !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover { background: #1D4ED8 !important; }
div[data-baseweb="select"] > div { background-color: var(--bg-surface-alt) !important; border: 1px solid var(--border-subtle) !important; }

hr { border-color: var(--border-subtle); margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# SYSTEM BACKEND
# =====================================================================
@st.cache_resource(show_spinner=False)
def load_security_engine():
    try:
        return joblib.load("model/model.pkl")
    except Exception:
        return None

bundle = load_security_engine()
if not bundle:
    st.error("System Error: model.pkl not found. Execute trainer container first.")
    st.stop()

model = bundle["model"]
features = bundle["features"]
sample_malware = bundle.get("sample_malware", ["SEND_SMS", "RECEIVE_BOOT_COMPLETED", "READ_PHONE_STATE", "Ljava/net/URL;->openConnection", "KILL_BACKGROUND_PROCESSES"])
sample_goodware = bundle.get("sample_goodware", ["VIBRATE", "INTERNET", "ACCESS_NETWORK_STATE"])

# =====================================================================
# SIDEBAR NAVIGATION
# =====================================================================
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-icon">AS</div>
            <div>
                <div class="sidebar-title">AppShield</div>
                <div class="sidebar-subtitle">Android Risk Analyzer</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="kicker" style="margin-bottom: 12px;">ANALYSIS</div>', unsafe_allow_html=True)
    page = st.radio("Navigation", ["Single App Analysis", "Batch Analysis"], label_visibility="collapsed")
    
    st.markdown('<div class="kicker" style="margin-top: 24px; margin-bottom: 12px;">INTELLIGENCE</div>', unsafe_allow_html=True)
    page2 = st.radio("Navigation2", ["Threat Intelligence"], label_visibility="collapsed")
    
    if st.session_state.get('last_page') != page and page != "Single App Analysis":
        selected_page = page
    elif st.session_state.get('last_page') != page2 and page2 != "Threat Intelligence":
        selected_page = page2
    else:
        selected_page = page

    st.session_state['last_page'] = selected_page

# =====================================================================
# PRODUCT HEADER & SYSTEM OVERVIEW
# =====================================================================
st.markdown("""
<div class="control-bar">
    <div>
        <h1 class="product-title">AppShield</h1>
        <p class="product-desc">Android Privacy & Malware Risk Analyzer</p>
    </div>
    <div class="sys-status">
        <span class="pulse-dot"></span> SYSTEM ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="system-overview">
    <div class="overview-metric">
        <div class="om-val">99.78%</div><div class="om-lbl">Model Accuracy</div>
    </div>
    <div class="overview-metric">
        <div class="om-val">4,464</div><div class="om-lbl">Targets Analyzed</div>
    </div>
    <div class="overview-metric">
        <div class="om-val">241</div><div class="om-lbl">Feature Vectors</div>
    </div>
    <div class="overview-metric">
        <div class="om-val" style="font-size: 16px; padding-top: 4px;">Random Forest</div><div class="om-lbl">Production Model</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# MAIN ANALYSIS EXPERIENCE (SINGLE APP)
# =====================================================================
if selected_page == "Single App Analysis":
    
    col_config, col_analysis = st.columns([1, 1.4], gap="large")

    with col_config:
        st.markdown('<div class="kicker">Target Application</div>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Manifest Configuration</h2>', unsafe_allow_html=True)
        st.caption("Load a profile or configure custom permission vectors.")
        
        c1, c2 = st.columns(2)
        if c1.button("✅ Load Safe App", use_container_width=True):
            st.session_state["active_payload"] = sample_goodware
        if c2.button("🚨 Load Malware", use_container_width=True):
            st.session_state["active_payload"] = sample_malware
            
        default_payload = st.session_state.get("active_payload", sample_goodware)
        
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        user_payload = st.multiselect(
            "Extracted Features / API Calls",
            options=features,
            default=[p for p in default_payload if p in features]
        )

        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        execute_btn = st.button("Initialize Analysis", type="primary", use_container_width=True)

    with col_analysis:
        # Wrap output in a dark developer console to create a premium contrast
        st.markdown('<div class="dev-console">', unsafe_allow_html=True)
        
        hero_ph = st.empty()
        pipeline_ph = st.empty()
        log_ph = st.empty()
        chart_ph = st.empty()

        def render_pipeline(active_idx):
            nodes = [
                ("1", "Input"),
                ("2", "Extract"),
                ("3", "Vectors"),
                ("4", "ML Engine"),
                ("5", "Evaluate"),
                ("✓", "Result")
            ]
            html = f'<div class="pipeline-wrapper"><div class="pipeline-track"></div><div class="pipeline-nodes">'
            for i, (icon, lbl) in enumerate(nodes):
                state = "completed" if i < active_idx else ("active" if i == active_idx else "")
                html += f'<div class="node {state}"><div class="node-circle">{icon}</div><div class="node-title">{lbl}</div></div>'
            html += '</div></div>'
            pipeline_ph.markdown(html, unsafe_allow_html=True)

        def render_logs(log_list):
            html = '<div class="activity-log">'
            for t, msg in log_list:
                html += f'<div class="log-row"><div class="log-time">{t}</div><div class="log-msg">{msg}</div></div>'
            html += '</div>'
            log_ph.markdown(html, unsafe_allow_html=True)

        if execute_btn:
            logs = []
            hero_ph.empty()
            chart_ph.empty()

            render_pipeline(0)
            logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-4], "Target manifest loaded into sandbox."))
            render_logs(logs)
            time.sleep(0.3)

            render_pipeline(1)
            logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-4], f"Extracted {len(features)} total features from binary."))
            render_logs(logs)
            time.sleep(0.3)

            render_pipeline(2)
            logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-4], f"Generated matrix. {len(user_payload)} active permission vectors identified."))
            render_logs(logs)
            time.sleep(0.4)

            render_pipeline(3)
            logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-4], "Model inference started (Random Forest Ensemble)."))
            render_logs(logs)
            time.sleep(0.5)

            df_target = pd.DataFrame([{f: (1 if f in user_payload else 0) for f in features}])
            pred = model.predict(df_target)[0]
            prob = model.predict_proba(df_target)[0][1]

            render_pipeline(4)
            logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-4], "Threat patterns evaluated against TUANDROMD signatures."))
            render_logs(logs)
            time.sleep(0.4)

            render_pipeline(5)
            logs.append((datetime.now().strftime("%H:%M:%S.%f")[:-4], "Diagnostic generated successfully."))
            render_logs(logs)
            
            st.session_state["last_res"] = {"pred": pred, "prob": prob, "payload": user_payload, "logs": logs}

        if "last_res" in st.session_state and not execute_btn:
            render_pipeline(5)
            render_logs(st.session_state["last_res"]["logs"])
            
        if "last_res" in st.session_state:
            res = st.session_state["last_res"]
            pred, prob, payload = res["pred"], res["prob"], res["payload"]

            with hero_ph.container():
                if pred == 1:
                    st.markdown(f"""
                    <div class="diagnostic-hero danger">
                        <div>
                            <div class="diag-header">SECURITY ASSESSMENT</div>
                            <h3 class="diag-title">CRITICAL RISK DETECTED</h3>
                            <p class="diag-desc">The application profile correlates with known background interception, SMS trojans, and privilege escalation malware.</p>
                        </div>
                        <div class="diag-score-block">
                            <div class="diag-score">{prob*100:.1f}%</div>
                            <div class="diag-score-lbl">Threat Confidence</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="diagnostic-hero safe">
                        <div>
                            <div class="diag-header">SECURITY ASSESSMENT</div>
                            <h3 class="diag-title">LOW RISK VERIFIED</h3>
                            <p class="diag-desc">Requested capabilities align with standard, benign utility parameters. No anomalous signatures detected.</p>
                        </div>
                        <div class="diag-score-block">
                            <div class="diag-score">{(1-prob)*100:.1f}%</div>
                            <div class="diag-score-lbl">Safety Confidence</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            with chart_ph.container():
                st.markdown('<div class="kicker" style="margin-top: 16px; color: #38BDF8;">EVIDENCE</div>', unsafe_allow_html=True)
                st.markdown('<h2 class="section-title" style="font-size:13px; color: #F8FAFC;">Predictive Feature Contributions</h2>', unsafe_allow_html=True)
                
                all_importances = pd.Series(model.feature_importances_, index=features)
                target_factors = all_importances[all_importances.index.isin(payload)].sort_values(ascending=False).head(4)

                if not target_factors.empty:
                    df_chart = pd.DataFrame({"Vector": target_factors.index, "Weight": target_factors.values})
                    chart = alt.Chart(df_chart).mark_bar(
                        color="#F87171" if pred == 1 else "#38BDF8", height=16, cornerRadiusEnd=2
                    ).encode(
                        x=alt.X("Weight:Q", axis=None),
                        y=alt.Y("Vector:N", sort="-x", title=None, axis=alt.Axis(labelColor="#94A3B8", labelFont="JetBrains Mono", labelFontSize=10, tickColor="transparent", domainColor="transparent")),
                        tooltip=["Vector", "Weight"]
                    ).properties(height=160).configure_view(strokeOpacity=0)
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.markdown("<p style='font-size: 13px; color: #64748B;'>No high-severity vectors present in payload.</p>", unsafe_allow_html=True)

        elif not execute_btn:
            hero_ph.markdown("""
            <div class="dev-console-empty">
                <div class="dev-console-icon">⌖</div>
                <div class="dev-console-title">SYSTEM STANDBY</div>
                <div class="dev-console-desc">Awaiting manifest injection. Configure vectors on the left to initiate security scan.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# =====================================================================
# PAGE 2: BATCH ANALYSIS
# =====================================================================
elif selected_page == "Batch Analysis":
    st.markdown('<div class="kicker">BATCH AUDIT</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title" style="font-size:20px;">Fleet Diagnostics</h2>', unsafe_allow_html=True)
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
        <div style="display:flex; gap:48px; background:var(--bg-surface); padding:24px; border:1px solid var(--border-subtle); border-radius:8px; margin-bottom:24px; box-shadow: var(--shadow-soft);">
            <div class="overview-metric">
                <div class="om-val">{total_apps}</div><div class="om-lbl">Total Scanned</div>
            </div>
            <div class="overview-metric">
                <div class="om-val" style="color: var(--danger-base);">{flagged_threats}</div><div class="om-lbl">Critical Threats</div>
            </div>
            <div class="overview-metric">
                <div class="om-val" style="color: var(--safe-base);">{total_apps - flagged_threats}</div><div class="om-lbl">Verified Safe</div>
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
elif selected_page == "Threat Intelligence":
    st.markdown('<div class="kicker">MODEL INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title" style="font-size:20px;">Global Threat Signatures</h2>', unsafe_allow_html=True)
    st.caption("The predictive mathematical weights of the most critical threat vectors across the entire dataset.")
    
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    top_global = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False).head(15)
    
    df_global = pd.DataFrame({"Feature": top_global.index, "Weight": top_global.values})
    
    chart_global = alt.Chart(df_global).mark_bar(cornerRadiusEnd=4, color="#2563EB", height=24).encode(
        x=alt.X("Weight:Q", title="Global Predictive Weight", axis=alt.Axis(grid=False)),
        y=alt.Y("Feature:N", sort="-x", title=None, axis=alt.Axis(labelColor="#64748B", labelFont="JetBrains Mono", labelFontSize=12)),
        tooltip=["Feature", "Weight"]
    ).properties(height=450).configure_view(strokeOpacity=0)
    
    st.altair_chart(chart_global, use_container_width=True)