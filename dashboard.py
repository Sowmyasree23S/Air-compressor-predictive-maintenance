import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI-Based Predictive Maintenance System",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS — clean light industrial theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #0f172a;
}

/* Light background */
.stApp { background: #f3f6ff; color: #0f172a !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #dbeafe;
    box-shadow: 2px 0 8px rgba(15, 23, 42, 0.06);
}
[data-testid="stSidebar"] * { color: #0f172a !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider  label {
    color: #1e293b !important;
    font-size: 0.72rem !important;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 2px;
}
[data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] select, [data-testid="stSidebar"] .stSlider {
    color: #0f172a !important;
    background: #f9fbff !important;
    border-color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stSelectbox div[role="combobox"] {
    background: #ffffff !important;
    border: 1px solid #dbeafe !important;
    border-radius: 10px;
    color: #1f2937 !important;
}


/* ── Section heading ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1rem;
    font-weight: 700;
    color: #1a202c;
    letter-spacing: 0.01em;
    margin: 0 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid #e2e8f0;
}
.sec-head-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 1rem;
}

/* ── Page header ── */
.page-header {
    background: linear-gradient(120deg, #0f172a 0%, #1d4ed8 50%, #60a5fa 100%);
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 28px;
    color: #fff;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0 12px 35px rgba(15, 23, 42, 0.2);
}
.page-header::after {
    content: '';
    position: absolute;
    right: -30px; top: -30px;
    width: 200px; height: 200px;
    background: rgba(255, 255, 255, 0.24);
    border-radius: 50%;
}
.page-header h1 {
    font-size: 2rem;
    font-weight: 800;
    margin: 0 0 6px;
    letter-spacing: -0.02em;
    text-shadow: 1px 1px 8px rgba(0,0,0,0.4);
}
.page-header p {
    font-size: 0.95rem;
    opacity: 0.95;
    margin: 0;
    color: #f8fbff;
}
.header-badges { display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap; }
.hbadge {
    background: #eaf4ff;
    border: 1px solid #c3ddff;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    color: #1a202c;
}

/* ── White card ── */
.card {
    background: #ffffff;
    border: 1px solid #dbeafe;
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 20px;
    box-shadow: 0 8px 26px rgba(15, 23, 42, 0.08);
}

/* ── Sensor card ── */
.sensor-card {
    background: #f8fbff;
    border: 1px solid #dbeafe;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
}
.sensor-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #718096;
    margin-bottom: 6px;
}
.sensor-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.1;
    color: #1a202c;
}
.sensor-unit {
    font-size: 0.9rem;
    color: #a0aec0;
    font-weight: 400;
}
.sensor-status {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    margin-top: 10px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
}
.status-normal  { background: #38a169; color: white; border: 1px solid #2f855a; }
.status-warning { background: #fffbeb; color: #4b5563; border: 1px solid #f2c94c; }
.status-critical{ background: #fee2e2; color: #9b2c2c; border: 1px solid #fca5a5; }
/* ── Health score bar ── */
.health-wrap { margin-top: 8px; }
.health-bar-bg {
    background: #edf2f7;
    border-radius: 8px;
    height: 28px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}
.health-bar-fill {
    height: 100%;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    color: #fff;
    transition: width 0.5s ease;
}

/* ── Fault table ── */
.fault-row {
    display: grid;
    grid-template-columns: 1.5fr 1fr 2fr;
    gap: 12px;
    padding: 12px 14px;
    border-radius: 8px;
    margin-bottom: 8px;
    border: 1px solid;
    align-items: center;
}
.fault-row-critical { background: #fff5f5; border-color: #fed7d7; }
.fault-row-warning  { background: #fffff0; border-color: #fef08a; }
.fault-row-none     { background: #f0fff4; border-color: #9ae6b4; }
.fault-name { font-weight: 700; font-size: 0.88rem; color: #1a202c; }
.fault-severity {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    padding: 3px 10px;
    border-radius: 20px;
    text-align: center;
}
.sev-critical { background: #fed7d7; color: #9b2c2c; }
.sev-warning  { background: #fef08a; color: #744210; }
.sev-normal   { background: #c6f6d5; color: #276749; }
.fault-action { font-size: 0.8rem; color: #4a5568; }

/* ── Alert box ── */
.alert-box {
    border-radius: 10px;
    padding: 16px 20px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 12px;
    border: 1px solid;
}
.alert-critical { background: #fff5f5; border-color: #fc8181; }
.alert-warning  { background: #fffbeb; border-color: #f6ad55; }
.alert-info     { background: #ebf8ff; border-color: #90cdf4; }
.alert-icon { font-size: 1.3rem; margin-top: 1px; }
.alert-title { font-weight: 700; font-size: 0.9rem; color: #1a202c; }
.alert-body  { font-size: 0.82rem; color: #4a5568; margin-top: 2px; }

/* ── Downtime comparison ── */
.dt-compare {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 18px;
}
.dt-card {
    border-radius: 10px;
    padding: 18px;
    text-align: center;
    border: 1px solid;
}
.dt-traditional { background: #fff5f5; border-color: #fed7d7; }
.dt-predictive  { background: #f0fff4; border-color: #9ae6b4; }
.dt-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #718096; margin-bottom: 8px; }
.dt-hours { font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; font-weight: 700; line-height: 1; }
.dt-traditional .dt-hours { color: #c53030; }
.dt-predictive  .dt-hours { color: #276749; }
.dt-sub { font-size: 0.75rem; color: #718096; margin-top: 4px; }

.reduction-pill {
    .reduction-pill {
    background: linear-gradient(135deg, #2b6cb0, #3182ce);
    color: #fff;
    border-radius: 30px;
    padding: 10px 24px;
    text-align: center;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.04em;
    margin-bottom: 8px;
    display: inline-block;
}

/* ── Metric overrides ── */
[data-testid="metric-container"] {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 14px 18px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
[data-testid="stMetricLabel"] { color: #718096 !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600 !important; }
[data-testid="stMetricValue"] { color: #1a202c !important; font-family: 'JetBrains Mono', monospace !important; }

/* ── Divider ── */
hr { border-color: #e2e8f0; margin: 24px 0; }

/* ── Table ── */
.stDataFrame { border-radius: 10px; overflow: hidden; border: 1px solid #e2e8f0; } 
            /* ── Streamlit alert color override ── */

/* success (green box) */
div[data-testid="stAlert"][kind="success"] {
    background-color: #f0fff4 !important;
    border: 1px solid #9ae6b4 !important;
    color: #276749 !important;
}

/* info (blue box) */
div[data-testid="stAlert"][kind="info"] {
    background-color: #f7fafc !important;
    border: 1px solid #cbd5e0 !important;
    color: #2d3748 !important;
}

/* warning */
div[data-testid="stAlert"][kind="warning"] {
    background-color: #ecf4ff !important;
    border: 1px solid #bfd7ff !important;
    color: #1f2937 !important;
}

/* error */
div[data-testid="stAlert"][kind="error"] {
    background-color: #fff7f8 !important;
    border: 1px solid #f8c2cb !important;
    color: #831843 !important;
}

/* make sidebar select lighter and non-black */
[data-testid="stSidebar"] select, [data-testid="stSidebar"] .css-1uc7j8h, [data-testid="stSidebar"] .stSelectbox {
    background: #f8fafb !important;
    color: #1f2937 !important;
    border: 1px solid #dbeafe !important;
}

[data-testid="stSidebar"] .css-1uc7j8h::placeholder {
    color: #475569 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONSTANTS & DEFAULTS
# ─────────────────────────────────────────────
DEFAULT_TEMP = 80.0
DEFAULT_VIB = 0.25
DEFAULT_PRESSURE = 3.5

MACHINE_LOCATIONS = {"C1": "Compressor Room A",
                     "C2": "Compressor Room B", "C3": "Production Line Area"}

TRAD_DOWNTIME = 8   # hours
PRED_DOWNTIME = 2   # hours

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────


def sensor_status(temp, vib, pressure):
    if temp > 75 or vib > 0.7 or pressure < 4.0:
        return "Critical", "critical"
    if temp > 60 or vib > 0.5 or pressure < 5.0:
        return "Warning", "warning"
    return "Normal", "normal"


def temp_status(v):
    if v > 75:
        return "Critical", "critical"
    if v > 60:
        return "Warning",  "warning"
    return "Normal", "normal"


def vib_status(v):
    if v > 0.7:
        return "Critical", "critical"
    if v > 0.5:
        return "Warning",  "warning"
    return "Normal", "normal"


def pres_status(v):
    if v < 4.0:
        return "Critical", "critical"
    if v < 5.0:
        return "Warning",  "warning"
    return "Normal", "normal"


def detect_faults(temp, vib, pressure):
    faults = []
    if temp > 75:
        faults.append({
            "fault": "Overheating",
            "sensor": f"Temp: {temp}°C",
            "severity": "Critical",
            "sev_class": "sev-critical",
            "row_class": "fault-row-critical",
            "action": "Shut down & inspect cooling system immediately",
            "icon": "🔴",
        })
    if vib > 0.7:
        faults.append({
            "fault": "Bearing Failure",
            "sensor": f"Vib: {vib} g",
            "severity": "Critical",
            "sev_class": "sev-critical",
            "row_class": "fault-row-critical",
            "action": "Replace bearing — schedule emergency maintenance",
            "icon": "🔴",
        })
    if pressure < 4.0:
        faults.append({
            "fault": "Valve Leakage",
            "sensor": f"Press: {pressure} bar",
            "severity": "Warning",
            "sev_class": "sev-warning",
            "row_class": "fault-row-warning",
            "action": "Inspect & reseat inlet/outlet valves",
            "icon": "🟡",
        })
    if not faults:
        faults.append({
            "fault": "No Faults Detected",
            "sensor": "All nominal",
            "severity": "Normal",
            "sev_class": "sev-normal",
            "row_class": "fault-row-none",
            "action": "Continue standard monitoring schedule",
            "icon": "🟢",
        })
    return faults


def health_score(temp, vib, pressure):
    t = max(0, 100 - ((temp - 20) / 80) * 100)
    v = max(0, 100 - (vib / 1.0) * 100)
    p = max(0, min(100, (pressure / 10) * 100))
    return round(t * 0.35 + v * 0.40 + p * 0.25)


def health_bar(score):
    if score >= 70:
        col = "#38a169"
    elif score >= 40:
        col = "#d69e2e"
    else:
        col = "#e53e3e"
    return f"""
    <div class="health-bar-bg">
        <div class="health-bar-fill" style="width:{score}%;background:{col};">
            {score}%
        </div>
    </div>"""


def sensor_card_html(icon, label, value, unit, status_label, status_class):
    return f"""
    <div class="sensor-card">
        <div class="sensor-label">{icon} {label}</div>
        <div class="sensor-value">{value}<span class="sensor-unit"> {unit}</span></div>
        <div class="sensor-status status-{status_class}">
            {'●' if status_class == 'normal' else '▲'} {status_label}
        </div>
    </div>"""


def generate_trend(base, noise_std, low, high, n=50):
    np.random.seed(7)
    vals = np.clip(base + np.cumsum(np.random.randn(n) * noise_std), low, high)
    times = [datetime.now() - timedelta(minutes=(n - i) * 3) for i in range(n)]
    return times, np.round(vals, 3)


def trend_fig(times, vals, label, color, y_range):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times, y=vals, mode="lines",
        line=dict(color=color, width=2.5, shape="spline"),
        fill="tozeroy", fillcolor="rgba(229,62,62,0.1)",
        name=label,
    ))
    fig.add_hline(y=vals[-1], line_dash="dot", line_color=color, opacity=0.5)
    fig.update_layout(
        height=200, margin=dict(l=0, r=0, t=8, b=0),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Inter", size=11, color="#4a5568"),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0", zeroline=False,
                   range=y_range, tickfont=dict(size=10)),
        showlegend=False,
    )
    return fig


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    st.markdown("---")
    machine_id = st.selectbox("Machine ID", ["C1", "C2", "C3"], index=1)
    location = MACHINE_LOCATIONS[machine_id]
    st.markdown(f"📍 **Location:** {location}")
    st.markdown("---")
    st.markdown("**Simulate Sensor Values**")
    temperature = st.slider("🌡 Temperature (°C)", 20,
                            100, int(DEFAULT_TEMP), 1)
    vibration = st.slider("📳 Vibration (g)",    0.0, 1.0, DEFAULT_VIB, 0.01)
    pressure = st.slider("💨 Pressure (bar)",   0.0,
                         10.0, DEFAULT_PRESSURE, 0.1)
    st.markdown("---")
    st.caption("💡 Default values: Temp=80°C · Vib=0.25g · Pressure=3.5 bar")
    st.markdown("---")
    st.caption("🏭 Predictive Maintenance System v2.0")

# ─────────────────────────────────────────────
#  DERIVED DATA
# ─────────────────────────────────────────────
score = health_score(temperature, vibration, pressure)
faults = detect_faults(temperature, vibration, pressure)
_, sys_kind = sensor_status(temperature, vibration, pressure)
t_lbl, t_cls = temp_status(temperature)
v_lbl, v_cls = vib_status(vibration)
p_lbl, p_cls = pres_status(pressure)

t_times, t_vals = generate_trend(temperature, 1.8, 20, 100)
v_times, v_vals = generate_trend(vibration,   0.02, 0.0, 1.0)
p_times, p_vals = generate_trend(pressure,    0.15, 0.0, 10.0)

reduction_pct = round((TRAD_DOWNTIME - PRED_DOWNTIME) / TRAD_DOWNTIME * 100)

# ─────────────────────────────────────────────
#  MAIN LAYOUT
# ─────────────────────────────────────────────

# ── Page Header ──
st.markdown(f"""
<div class="page-header">
    <h1>⚙️ AI-Based Predictive Maintenance System for Industrial Air Compressors</h1>
    <p>Hybrid AI Monitoring: clustering + prediction for real-time compressor health and maintenance alerts.</p>
    <div class="header-badges">
        <span class="hbadge">🤖 Hybrid AI</span>
        <span class="hbadge">📊 Industry 4.0</span>
        <span class="hbadge">🧠 Fault Prediction</span>
        <span class="hbadge">📍 {machine_id} - {location}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ──
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("🌡 Temperature",  f"{temperature} °C",
              delta=f"{temperature - 45} °C vs baseline", delta_color="inverse")
with k2:
    st.metric("📳 Vibration",    f"{vibration:.2f} g",
              delta=f"{round(vibration - 0.25, 2)} g vs baseline", delta_color="inverse")
with k3:
    st.metric("💨 Pressure",     f"{pressure:.1f} bar",
              delta=f"{round(pressure - 5.5, 1)} bar vs nominal", delta_color="normal")
with k4:
    st.metric("🏥 Health Score", f"{score} / 100")

st.markdown("---")

# ═══════════════════════════════════════
#  SECTION 1 — LIVE SENSOR MONITORING
# ═══════════════════════════════════════
st.markdown("""
<div class="sec-head">
    <span class="sec-head-icon" style="background:#ebf8ff;">📡</span>
    Section 1 — Live Sensor Monitoring
</div>""", unsafe_allow_html=True)

sc1, sc2, sc3 = st.columns(3)
with sc1:
    st.markdown(sensor_card_html("🌡", "Temperature",
                f"{temperature}", "°C",  t_lbl, t_cls), unsafe_allow_html=True)
    st.plotly_chart(trend_fig(t_times, t_vals, "Temp", "#e53e3e", [
                    15, 105]), use_container_width=True)
with sc2:
    st.markdown(sensor_card_html("📳", "Vibration",
                f"{vibration:.2f}", "g",  v_lbl, v_cls), unsafe_allow_html=True)
    st.plotly_chart(trend_fig(v_times, v_vals, "Vib",  "#d69e2e",
                    [-0.05, 1.05]), use_container_width=True)
with sc3:
    st.markdown(sensor_card_html("💨", "Pressure",
                f"{pressure:.1f}", "bar", p_lbl, p_cls), unsafe_allow_html=True)
    st.plotly_chart(trend_fig(p_times, p_vals, "Press",
                    "#3182ce", [-0.3, 10.5]), use_container_width=True)

# Sensor summary table
sensor_table = pd.DataFrame({
    "Sensor":        ["Temperature", "Vibration", "Pressure"],
    "Value":         [f"{temperature} °C", f"{vibration:.2f} g", f"{pressure:.1f} bar"],
    "Normal Range":  ["20 – 60 °C", "0.0 – 0.5 g", "5.0 – 9.0 bar"],
    "Status":        [t_lbl, v_lbl, p_lbl],
    "Threshold":     ["> 75°C = Critical", "> 0.7g = Critical", "< 4.0 bar = Warning"],
})
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("**📋 Sensor Summary Table**", unsafe_allow_html=False)
st.table(sensor_table)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════
#  SECTION 2 — MACHINE HEALTH ANALYSIS
# ═══════════════════════════════════════
st.markdown("""
<div class="sec-head">
    <span class="sec-head-icon" style="background:#f0fff4;">🏥</span>
    Section 2 — Machine Health Analysis
</div>""", unsafe_allow_html=True)

ha1, ha2 = st.columns([1.2, 1])

with ha1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Machine Health Score**")
    st.markdown(health_bar(score), unsafe_allow_html=True)

    if score >= 70:
        health_desc = ("🟢 **Good Condition** — Compressor is operating within safe parameters. "
                       "Continue routine monitoring schedule.")
        st.success(health_desc)
    elif score >= 40:
        health_desc = ("🟡 **Moderate Concern** — Some sensor readings are elevated. "
                       "Schedule preventive inspection within 48 hours.")
        st.warning(health_desc)
    else:
        health_desc = ("🔴 **Poor Condition** — Multiple sensors outside safe range. "
                       "Immediate maintenance intervention required.")
        st.error(health_desc)

    st.markdown("""
    <div style="margin-top:14px; font-size:0.78rem; color:#718096; line-height:1.8;">
        <strong>Score Weights:</strong><br>
        📳 Vibration: 40% &nbsp;|&nbsp; 🌡 Temperature: 35% &nbsp;|&nbsp; 💨 Pressure: 25%
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with ha2:
    # Gauge chart
    gauge_col = "#38a169" if score >= 70 else (
        "#d69e2e" if score >= 40 else "#e53e3e")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        delta={"reference": 70, "increasing": {"color": "#38a169"},
               "decreasing": {"color": "#e53e3e"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#a0aec0", "tickfont": {"size": 10}},
            "bar": {"color": gauge_col, "thickness": 0.25},
            "bgcolor": "white",
            "borderwidth": 2, "bordercolor": "#e2e8f0",
            "steps": [
                {"range": [0,  40], "color": "#fff5f5"},
                {"range": [40, 70], "color": "#fffff0"},
                {"range": [70, 100], "color": "#f0fff4"},
            ],
            "threshold": {"line": {"color": "#2d3748", "width": 3}, "thickness": 0.75, "value": 70},
        },
        title={"text": f"Health Score — {machine_id}",
               "font": {"size": 13, "color": "#4a5568"}},
        number={"font": {"size": 36, "color": gauge_col}},
    ))
    fig_gauge.update_layout(
        height=260, margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="white", font=dict(family="Inter"),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════
#  SECTION 3 — FAULT DETECTION RESULTS
# ═══════════════════════════════════════
st.markdown("""
<div class="sec-head">
    <span class="sec-head-icon" style="background:#fff5f5;">🔍</span>
    Section 3 — Fault Detection Results
</div>""", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("""
<div style="display:grid; grid-template-columns:1.5fr 0.8fr 2fr; gap:12px;
    padding:8px 14px; margin-bottom:4px; font-size:0.72rem; font-weight:700;
    text-transform:uppercase; letter-spacing:0.08em; color:#718096;
    border-bottom:2px solid #e2e8f0;">
    <span>Fault Type / Sensor</span><span>Severity</span><span>Recommended Action</span>
</div>
""", unsafe_allow_html=True)

for f in faults:
    st.markdown(f"""
    <div class="fault-row {f['row_class']}">
        <div>
            <div class="fault-name">{f['icon']} {f['fault']}</div>
            <div style="font-size:0.75rem; color:#718096; margin-top:2px; font-family:'JetBrains Mono',monospace;">{f['sensor']}</div>
        </div>
        <div><span class="fault-severity {f['sev_class']}">{f['severity']}</span></div>
        <div class="fault-action">⚙️ {f['action']}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════
#  SECTION 4 — MAINTENANCE ALERTS
# ═══════════════════════════════════════
st.markdown("""
<div class="sec-head">
    <span class="sec-head-icon" style="background:#fffbeb;">🔔</span>
    Section 4 — Maintenance Alert System
</div>""", unsafe_allow_html=True)

has_critical = any(
    f["severity"] == "Critical" for f in faults if f["fault"] != "No Faults Detected")
has_warning = any(
    f["severity"] == "Warning" for f in faults if f["fault"] != "No Faults Detected")

if has_critical:
    st.error(f"🚨 **CRITICAL ALERT** — Immediate Maintenance Required\n\n"
             f"Compressor **{machine_id}** at **{location}** has one or more critical sensor readings. "
             f"Dispatch technician immediately to prevent equipment failure.")

if has_warning:
    st.warning(f"⚠️ **WARNING** — Maintenance Recommended\n\n"
               f"Compressor **{machine_id}** at **{location}** shows early fault indicators. "
               f"Schedule inspection within 24–48 hours to avoid escalation.")

if not has_critical and not has_warning:
    st.success(f"✅ **All Clear** — No Maintenance Required\n\n"
               f"Compressor **{machine_id}** at **{location}** is operating normally. "
               f"Next scheduled maintenance: as per standard interval.")

# Alert log table
alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
alert_rows = []
for f in faults:
    if f["fault"] != "No Faults Detected":
        alert_rows.append({
            "Timestamp":   alert_time,
            "Machine":     machine_id,
            "Location":    location,
            "Fault":       f["fault"],
            "Severity":    f["severity"],
            "Action":      f["action"],
        })

if alert_rows:
    st.markdown("**📋 Active Alert Log**")
    st.table(pd.DataFrame(alert_rows))
else:
    st.info("📋 No active alerts in the system log.")

st.markdown("---")

# ═══════════════════════════════════════
#  SECTION 5 — DOWNTIME REDUCTION REPORT
# ═══════════════════════════════════════
st.markdown("""
<div class="sec-head">
    <span class="sec-head-icon" style="background:#f0fff4;">📊</span>
    Section 5 — Downtime Reduction Report
</div>""", unsafe_allow_html=True)

dt1, dt2 = st.columns([1, 1.4])

with dt1:
    st.markdown(f"""
    <div class="card">
        <div class="dt-compare">
            <div class="dt-card dt-traditional">
                <div class="dt-label">Traditional Maintenance</div>
                <div class="dt-hours">{TRAD_DOWNTIME}h</div>
                <div class="dt-sub">avg. downtime / event</div>
            </div>
            <div class="dt-card dt-predictive">
                <div class="dt-label">Predictive Maintenance</div>
                <div class="dt-hours">{PRED_DOWNTIME}h</div>
                <div class="dt-sub">avg. downtime / event</div>
            </div>
        </div>
        <div style="text-align:center;">
            <span class="reduction-pill">⬇ {reduction_pct}% Downtime Reduction</span>
            <div style="font-size:0.78rem; color:#718096; margin-top:8px;">
                Saving <strong>{TRAD_DOWNTIME - PRED_DOWNTIME} hours</strong> per maintenance event<br>
                through AI-driven early fault detection.
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.progress(reduction_pct / 100,
                text=f"Efficiency Improvement: {reduction_pct}%")

with dt2:
    categories = ["Fault Detection", "Diagnosis Time",
                  "Part Sourcing", "Repair Time", "Testing"]
    trad_vals = [2.0, 1.5, 2.0, 2.0, 0.5]
    pred_vals = [0.2, 0.5, 0.5, 0.5, 0.3]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="Traditional", x=categories, y=trad_vals,
        marker_color="#fc8181", marker_line_color="#e53e3e", marker_line_width=1,
    ))
    fig_bar.add_trace(go.Bar(
        name="Predictive AI", x=categories, y=pred_vals,
        marker_color="#68d391", marker_line_color="#38a169", marker_line_width=1,
    ))
    fig_bar.update_layout(
        barmode="group",
        title=dict(text="Downtime Breakdown by Phase (hours)",
                   font=dict(size=13, color="#2d3748")),
        height=280, margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="white", plot_bgcolor="white",
        legend=dict(orientation="h", y=-0.18, font=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0", title="Hours"),
        xaxis=dict(tickfont=dict(size=10)),
        font=dict(family="Inter"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ROI metrics
    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("Time Saved",
                  f"{TRAD_DOWNTIME - PRED_DOWNTIME} hrs", "per event")
    with r2:
        st.metric("Reduction",
                  f"{reduction_pct}%",                   "downtime ↓")
    with r3:
        st.metric("Est. Cost Save", "₹48,000",
                  "per incident")

# ── Footer ──
st.markdown("---")
st.markdown("""
<div style="text-align:center; font-size:0.72rem; color:#a0aec0; letter-spacing:0.08em; padding: 8px 0 4px;">
    PREDICTIVE MAINTENANCE SYSTEM v2.0 &nbsp;·&nbsp; INDUSTRY 4.0 PROTOTYPE &nbsp;·&nbsp;
    AI-DRIVEN FAULT DETECTION &nbsp;·&nbsp; REAL-TIME SENSOR FUSION
</div>""", unsafe_allow_html=True)
