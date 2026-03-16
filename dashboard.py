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
    page_title="Airlytics",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS — high contrast, fully readable
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Global font ── */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
}

/* ── Dark text only for main area — sidebar excluded ── */
section.main p, section.main span, section.main label,
section.main h2, section.main h3, section.main h4,
.main .stMarkdown p, .main .stMarkdown li,
.main .stMarkdown span, .main .stMarkdown strong,
.main .stMarkdown em, .main .element-container p,
.main .element-container span {
    color: #111827 !important;
}

.stApp {
    background: #f0f4f8 !important;
}

/* ── Force all markdown text to be dark ── */
.stMarkdown p,
.stMarkdown li,
.stMarkdown span,
.stMarkdown strong,
.stMarkdown em,
.element-container p,
.element-container span {
    color: #111827 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #1e293b !important;
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"],
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] b,
[data-testid="stSidebar"] em,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stMarkdown *,
[data-testid="stSidebar"] .stSlider *,
[data-testid="stSidebar"] .stSelectbox *,
[data-testid="stSidebar"] .element-container * {
    color: #f1f5f9 !important;
    -webkit-text-fill-color: #f1f5f9 !important;
}
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSelectbox label {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    font-size: 0.70rem !important;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
/* ── Selectbox: lock ALL states to consistent dark-slate style ── */
[data-testid="stSidebar"] .stSelectbox div[role="combobox"],
[data-testid="stSidebar"] .stSelectbox div[role="combobox"] *,
[data-testid="stSidebar"] [data-baseweb="select"],
[data-testid="stSidebar"] [data-baseweb="select"] *,
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="select"] > div > div,
[data-testid="stSidebar"] [data-baseweb="select"] input,
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="popover"] *,
[data-testid="stSidebar"] ul[role="listbox"],
[data-testid="stSidebar"] ul[role="listbox"] li,
[data-testid="stSidebar"] ul[role="listbox"] li * {
    background: #334155 !important;
    background-color: #334155 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    -webkit-text-fill-color: #f1f5f9 !important;
}
/* Hover state for dropdown options */
[data-testid="stSidebar"] ul[role="listbox"] li:hover,
[data-testid="stSidebar"] ul[role="listbox"] li[aria-selected="true"],
[data-testid="stSidebar"] ul[role="listbox"] li:hover *,
[data-testid="stSidebar"] ul[role="listbox"] li[aria-selected="true"] * {
    background: #1e40af !important;
    background-color: #1e40af !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
/* The chevron/arrow icon inside the selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: #94a3b8 !important;
    color: #94a3b8 !important;
}
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] b {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] .stCaption * {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}
[data-testid="stSidebar"] hr {
    border-color: #334155 !important;
}

/* ── Section heading ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1rem;
    font-weight: 700;
    color: #0f172a !important;
    letter-spacing: 0.01em;
    margin: 0 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid #cbd5e1;
}
.sec-head * { color: #0f172a !important; }
.sec-head-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 1rem;
}

/* ── Page header ── */
.page-header {
    background: linear-gradient(120deg, #0f172a 0%, #1d4ed8 55%, #3b82f6 100%);
    border-radius: 18px;
    padding: 30px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 12px 35px rgba(15, 23, 42, 0.25);
}
.page-header::after {
    content: '';
    position: absolute;
    right: -40px; top: -40px;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.page-header h1 {
    font-size: 1.9rem;
    font-weight: 800;
    margin: 0 0 8px;
    letter-spacing: -0.02em;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    text-shadow: 0 2px 14px rgba(0,0,0,0.5);
}
.page-header p {
    font-size: 0.95rem;
    margin: 0;
    color: #e0eeff !important;
    -webkit-text-fill-color: #e0eeff !important;
    opacity: 1 !important;
}
.header-badges { display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap; }
.hbadge {
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.35);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: #ffffff !important;
}

/* ── White card ── */
.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.07);
}
.card p, .card span, .card div, .card strong, .card b {
    color: #111827 !important;
}

/* ── Sensor card ── */
.sensor-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px 22px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.07);
    margin-bottom: 12px;
}
.sensor-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #475569 !important;
    margin-bottom: 8px;
}
.sensor-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.1;
    color: #0f172a !important;
}
.sensor-unit {
    font-size: 0.9rem;
    color: #64748b !important;
    font-weight: 400;
}
.sensor-status {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    margin-top: 10px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
}
.status-normal   { background: #dcfce7; color: #14532d !important; border: 1px solid #86efac; }
.status-warning  { background: #fef9c3; color: #713f12 !important; border: 1px solid #fde047; }
.status-critical { background: #fee2e2; color: #7f1d1d !important; border: 1px solid #fca5a5; }

/* ── Health score bar ── */
.health-bar-bg {
    background: #e2e8f0;
    border-radius: 8px;
    height: 30px;
    overflow: hidden;
    border: 1px solid #cbd5e1;
}
.health-bar-fill {
    height: 100%;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    font-weight: 700;
    color: #ffffff !important;
    transition: width 0.5s ease;
}

/* ── Fault table ── */
.fault-row {
    display: grid;
    grid-template-columns: 1.5fr 1fr 2fr;
    gap: 12px;
    padding: 14px 16px;
    border-radius: 10px;
    margin-bottom: 10px;
    border: 1px solid;
    align-items: center;
}
.fault-row-critical { background: #fff1f2; border-color: #fecdd3; }
.fault-row-warning  { background: #fefce8; border-color: #fde68a; }
.fault-row-none     { background: #f0fdf4; border-color: #bbf7d0; }
.fault-name {
    font-weight: 700;
    font-size: 0.88rem;
    color: #0f172a !important;
}
.fault-sensor-text {
    font-size: 0.75rem;
    color: #374151 !important;
    margin-top: 3px;
    font-family: 'JetBrains Mono', monospace;
}
.fault-severity {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    padding: 4px 12px;
    border-radius: 20px;
    text-align: center;
    display: inline-block;
}
.sev-critical { background: #fecdd3; color: #7f1d1d !important; }
.sev-warning  { background: #fde68a; color: #713f12 !important; }
.sev-normal   { background: #bbf7d0; color: #14532d !important; }
.fault-action {
    font-size: 0.82rem;
    color: #1e293b !important;
    font-weight: 500;
}

/* ── Downtime comparison cards ── */
.dt-compare {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 18px;
}
.dt-card {
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    border: 1px solid;
}
.dt-traditional { background: #fff1f2; border-color: #fecdd3; }
.dt-predictive  { background: #f0fdf4; border-color: #bbf7d0; }
.dt-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #374151 !important;
    margin-bottom: 8px;
}
.dt-hours {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1;
}
.dt-traditional .dt-hours { color: #991b1b !important; }
.dt-predictive  .dt-hours { color: #14532d !important; }
.dt-sub { font-size: 0.75rem; color: #374151 !important; margin-top: 6px; }

.reduction-pill {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: #ffffff !important;
    border-radius: 30px;
    padding: 10px 28px;
    text-align: center;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.04em;
    margin-bottom: 8px;
    display: inline-block;
    box-shadow: 0 4px 14px rgba(29, 78, 216, 0.3);
}

.saving-text {
    font-size: 0.82rem;
    color: #374151 !important;
    margin-top: 8px;
    line-height: 1.7;
}
.saving-text strong {
    color: #0f172a !important;
}

/* ── Score weight text ── */
.score-weights {
    margin-top: 14px;
    font-size: 0.8rem;
    color: #374151 !important;
    line-height: 2;
}
.score-weights strong {
    color: #0f172a !important;
}

/* ── Metric overrides ── */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] span {
    color: #475569 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] span {
    color: #0f172a !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stMetricDelta"] span {
    font-size: 0.78rem !important;
}

/* ── Streamlit alert overrides — fully visible text ── */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
}
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] div {
    font-weight: 500 !important;
    font-size: 0.88rem !important;
}
/* success */
div[data-testid="stAlert"][data-baseweb="notification"][kind="positive"],
.stAlert.stSuccess,
div.stSuccess {
    background-color: #f0fdf4 !important;
    border: 1.5px solid #86efac !important;
}
div[data-testid="stAlert"][data-baseweb="notification"][kind="positive"] p,
div[data-testid="stAlert"][data-baseweb="notification"][kind="positive"] span {
    color: #14532d !important;
}
/* info */
div[data-testid="stAlert"][data-baseweb="notification"][kind="info"] {
    background-color: #eff6ff !important;
    border: 1.5px solid #93c5fd !important;
}
div[data-testid="stAlert"][data-baseweb="notification"][kind="info"] p,
div[data-testid="stAlert"][data-baseweb="notification"][kind="info"] span {
    color: #1e3a8a !important;
}
/* warning */
div[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
    background-color: #fefce8 !important;
    border: 1.5px solid #fde047 !important;
}
div[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] p,
div[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] span {
    color: #713f12 !important;
}
/* error */
div[data-testid="stAlert"][data-baseweb="notification"][kind="error"] {
    background-color: #fff1f2 !important;
    border: 1.5px solid #fca5a5 !important;
}
div[data-testid="stAlert"][data-baseweb="notification"][kind="error"] p,
div[data-testid="stAlert"][data-baseweb="notification"][kind="error"] span {
    color: #7f1d1d !important;
}

/* ── Selectbox dropdown popover (renders OUTSIDE sidebar DOM) ── */
[data-baseweb="popover"],
[data-baseweb="popover"] *,
[data-baseweb="menu"],
[data-baseweb="menu"] *,
ul[role="listbox"],
ul[role="listbox"] li,
ul[role="listbox"] li * {
    background: #1e293b !important;
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
    -webkit-text-fill-color: #f1f5f9 !important;
    border-color: #475569 !important;
}
ul[role="listbox"] li:hover,
ul[role="listbox"] li[aria-selected="true"],
ul[role="listbox"] li:hover *,
ul[role="listbox"] li[aria-selected="true"] * {
    background: #1d4ed8 !important;
    background-color: #1d4ed8 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* ── Info box inside card ── */
.info-box {
    background: #eff6ff;
    border: 1px solid #93c5fd;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 0.82rem;
    color: #1e3a8a !important;
    margin-bottom: 8px;
}

/* ── Table ── */
.stDataFrame { border-radius: 10px; overflow: hidden; border: 1px solid #e2e8f0; }
table { color: #111827 !important; }
thead th { color: #0f172a !important; font-weight: 700 !important; background: #f8fafc !important; }
tbody td { color: #1e293b !important; }

/* ── Divider ── */
hr { border-color: #e2e8f0 !important; margin: 24px 0; }

/* ── Section header text ── */
h3 { color: #0f172a !important; }

/* ── Footer ── */
.footer-text { color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONSTANTS & DEFAULTS
# ─────────────────────────────────────────────
DEFAULT_TEMP = 80.0
DEFAULT_VIB = 0.25  # g
DEFAULT_PRESSURE = 3.5

MM_PER_S_PER_G = 1000.0

MACHINE_LOCATIONS = {
    "C1": "Compressor Room A",
    "C2": "Compressor Room B",
    "C3": "Production Line Area"
}

TRAD_DOWNTIME = 8
PRED_DOWNTIME = 2

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────


def sensor_status(temp, vib_mm, pressure):
    if temp > 75 or vib_mm > 700 or pressure < 4.0:
        return "Critical", "critical"
    if temp > 60 or vib_mm > 500 or pressure < 5.0:
        return "Warning", "warning"
    return "Normal", "normal"


def temp_status(v):
    if v > 75:
        return "Critical", "critical"
    if v > 60:
        return "Warning",  "warning"
    return "Normal", "normal"


def vib_status(v):
    if v > 700:
        return "Critical", "critical"
    if v > 500:
        return "Warning",  "warning"
    return "Normal", "normal"


def pres_status(v):
    if v < 4.0:
        return "Critical", "critical"
    if v < 5.0:
        return "Warning",  "warning"
    return "Normal", "normal"


def extract_vibration_features(vib_mm):
    n = 100
    rng = np.random.default_rng(123)
    signal = vib_mm + rng.normal(0, vib_mm * 0.08 + 0.3, size=n)
    rms = np.sqrt(np.mean(signal ** 2))
    m2 = np.mean((signal - np.mean(signal)) ** 2)
    m4 = np.mean((signal - np.mean(signal)) ** 4)
    kurtosis = m4 / (m2 ** 2) - 3 if m2 > 0 else 0.0
    fft = np.fft.rfft(signal)
    spectral_energy = np.sum(np.abs(fft) ** 2) / len(fft)
    return round(rms, 2), round(kurtosis, 2), round(spectral_energy, 2)


def detect_faults(temp, vib_mm, pressure):
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
    if vib_mm > 700:
        faults.append({
            "fault": "Bearing Failure",
            "sensor": f"Vib: {vib_mm:.1f} mm/s",
            "severity": "Critical",
            "sev_class": "sev-critical",
            "row_class": "fault-row-critical",
            "action": "Replace bearing — schedule emergency maintenance",
            "icon": "🔴",
        })
    elif vib_mm > 500:
        faults.append({
            "fault": "Bearing Wear",
            "sensor": f"Vib: {vib_mm:.1f} mm/s",
            "severity": "Warning",
            "sev_class": "sev-warning",
            "row_class": "fault-row-warning",
            "action": "Inspect bearings & alignment",
            "icon": "🟡",
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


def health_score(temp, vib_mm, pressure, vib_rms, vib_kurtosis):
    t = max(0, 100 - ((temp - 20) / 80) * 100)
    v_rms = max(0, 100 - min(vib_rms, 100))
    k = max(0, 100 - min(max((vib_kurtosis - 3) * 10, 0), 100))
    p = max(0, min(100, (pressure / 10) * 100))
    return round(t * 0.3 + v_rms * 0.3 + k * 0.2 + p * 0.2)


def health_bar(score):
    col = "#16a34a" if score >= 70 else (
        "#d97706" if score >= 40 else "#dc2626")
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
        fill="tozeroy", fillcolor=f"rgba(100,100,100,0.07)",
        name=label,
    ))
    fig.add_hline(y=vals[-1], line_dash="dot", line_color=color, opacity=0.6)
    fig.update_layout(
        height=200, margin=dict(l=0, r=0, t=8, b=0),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Inter", size=11, color="#374151"),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9", zeroline=False,
                   range=y_range, tickfont=dict(size=10, color="#374151")),
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
    vibration_mm = st.slider("📳 Vibration (mm/s)", 0.0,
                             1200.0, DEFAULT_VIB * 1000, 1.0)
    pressure = st.slider("💨 Pressure (bar)", 0.0, 10.0, DEFAULT_PRESSURE, 0.1)
    st.markdown("---")
    st.caption("💡 Default values: Temp=80°C · Vib=250 mm/s · Pressure=3.5 bar")
    st.markdown("---")
    st.caption("🏭 Airlytics v2.0")

# ─────────────────────────────────────────────
#  DERIVED DATA
# ─────────────────────────────────────────────
vibration_g = vibration_mm / MM_PER_S_PER_G
vibration_rms, vibration_kurtosis, vibration_energy = extract_vibration_features(
    vibration_mm)

score = health_score(temperature, vibration_mm, pressure,
                     vibration_rms, vibration_kurtosis)
faults = detect_faults(temperature, vibration_mm, pressure)
_, sys_kind = sensor_status(temperature, vibration_mm, pressure)
t_lbl, t_cls = temp_status(temperature)
v_lbl, v_cls = vib_status(vibration_mm)
p_lbl, p_cls = pres_status(pressure)

t_times, t_vals = generate_trend(temperature, 1.8, 20, 100)
v_times, v_vals = generate_trend(vibration_mm, 8.0, 0.0, 1200.0)
p_times, p_vals = generate_trend(pressure, 0.15, 0.0, 10.0)

reduction_pct = round((TRAD_DOWNTIME - PRED_DOWNTIME) / TRAD_DOWNTIME * 100)

# ─────────────────────────────────────────────
#  MAIN LAYOUT
# ─────────────────────────────────────────────

# ── Page Header ──
st.markdown(f"""
<div class="page-header">
    <h1>⚙️ Airlytics</h1>
    <p>AI-Based Predictive Maintenance System for Industrial Air Compressors —
    Hybrid AI Monitoring with real-time fault detection and health analytics.</p>
    <div class="header-badges">
        <span class="hbadge">🤖 Hybrid AI</span>
        <span class="hbadge">📊 Industry 4.0</span>
        <span class="hbadge">🧠 Fault Prediction</span>
        <span class="hbadge">📍 {machine_id} — {location}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ──
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("🌡 Temperature", f"{temperature} °C",
              delta=f"{temperature - 45} °C vs baseline", delta_color="inverse")
with k2:
    st.metric("📳 Vibration", f"{vibration_mm:.1f} mm/s",
              delta=f"{round(vibration_mm - 250, 1)} mm/s vs baseline", delta_color="inverse")
with k3:
    st.metric("💨 Pressure", f"{pressure:.1f} bar",
              delta=f"{round(pressure - 5.5, 1)} bar vs nominal", delta_color="normal")
with k4:
    st.metric("🏥 Health Score", f"{score} / 100")

k5, k6, k7 = st.columns(3)
with k5:
    st.metric("RMS", f"{vibration_rms} mm/s")
with k6:
    st.metric("Kurtosis", f"{vibration_kurtosis}")
with k7:
    st.metric("Spectral Energy", f"{vibration_energy}")

st.markdown("---")

# ═══════════════════════════════════════
#  SECTION 1 — LIVE SENSOR MONITORING
# ═══════════════════════════════════════
st.markdown("""
<div class="sec-head">
    <span class="sec-head-icon" style="background:#dbeafe;">📡</span>
    Section 1 — Live Sensor Monitoring
</div>""", unsafe_allow_html=True)

sc1, sc2, sc3 = st.columns(3)
with sc1:
    st.markdown(sensor_card_html("🌡", "Temperature",
                f"{temperature}", "°C", t_lbl, t_cls), unsafe_allow_html=True)
    st.plotly_chart(trend_fig(t_times, t_vals, "Temp",
                    "#dc2626", [15, 105]), width='stretch')
with sc2:
    st.markdown(sensor_card_html("📳", "Vibration",
                f"{vibration_mm:.1f}", "mm/s", v_lbl, v_cls), unsafe_allow_html=True)
    st.plotly_chart(trend_fig(v_times, v_vals, "Vib",
                    "#d97706", [0, 1200]), width='stretch')
with sc3:
    st.markdown(sensor_card_html("💨", "Pressure",
                f"{pressure:.1f}", "bar", p_lbl, p_cls), unsafe_allow_html=True)
    st.plotly_chart(trend_fig(p_times, p_vals, "Press",
                    "#2563eb", [-0.3, 10.5]), width='stretch')

sensor_table = pd.DataFrame({
    "Sensor":       ["Temperature", "Vibration", "Pressure"],
    "Value":        [f"{temperature} °C", f"{vibration_mm:.1f} mm/s", f"{pressure:.1f} bar"],
    "Normal Range": ["20 – 60 °C", "0 – 500 mm/s", "5.0 – 9.0 bar"],
    "Status":       [t_lbl, v_lbl, p_lbl],
    "Threshold":    ["> 75°C = Critical", "> 700 mm/s = Critical", "< 4.0 bar = Warning"],
})
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("**📋 Sensor Summary Table**")
st.table(sensor_table)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════
#  SECTION 2 — MACHINE HEALTH ANALYSIS
# ═══════════════════════════════════════
st.markdown("""
<div class="sec-head">
    <span class="sec-head-icon" style="background:#dcfce7;">🏥</span>
    Section 2 — Machine Health Analysis
</div>""", unsafe_allow_html=True)

ha1, ha2 = st.columns([1.2, 1])

with ha1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Machine Health Score**")
    st.markdown(health_bar(score), unsafe_allow_html=True)

    if score >= 70:
        st.success(
            "🟢 **Good Condition** — Compressor is operating within safe parameters. Continue routine monitoring schedule.")
    elif score >= 40:
        st.warning(
            "🟡 **Moderate Concern** — Some sensor readings are elevated. Schedule preventive inspection within 48 hours.")
    else:
        st.error(
            "🔴 **Poor Condition** — Multiple sensors outside safe range. Immediate maintenance intervention required.")

    st.markdown("""
    <div class="score-weights">
        <strong>Score Weights:</strong><br>
        📳 Vibration RMS: 30% &nbsp;|&nbsp; Kurtosis: 20% &nbsp;|&nbsp; 🌡 Temperature: 30% &nbsp;|&nbsp; 💨 Pressure: 20%
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with ha2:
    gauge_col = "#16a34a" if score >= 70 else (
        "#d97706" if score >= 40 else "#dc2626")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        delta={"reference": 70, "increasing": {"color": "#16a34a"},
               "decreasing": {"color": "#dc2626"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94a3b8", "tickfont": {"size": 10, "color": "#374151"}},
            "bar": {"color": gauge_col, "thickness": 0.25},
            "bgcolor": "white",
            "borderwidth": 2, "bordercolor": "#e2e8f0",
            "steps": [
                {"range": [0,  40], "color": "#fff1f2"},
                {"range": [40, 70], "color": "#fefce8"},
                {"range": [70, 100], "color": "#f0fdf4"},
            ],
            "threshold": {"line": {"color": "#0f172a", "width": 3}, "thickness": 0.75, "value": 70},
        },
        title={"text": f"Health Score — {machine_id}",
               "font": {"size": 13, "color": "#374151"}},
        number={"font": {"size": 36, "color": gauge_col}},
    ))
    fig_gauge.update_layout(
        height=260, margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="white", font=dict(family="Inter", color="#374151"),
    )
    st.plotly_chart(fig_gauge, width='stretch')

st.markdown("---")

# ═══════════════════════════════════════
#  SECTION 3 — FAULT DETECTION RESULTS
# ═══════════════════════════════════════
st.markdown("""
<div class="sec-head">
    <span class="sec-head-icon" style="background:#fee2e2;">🔍</span>
    Section 3 — Fault Detection Results
</div>""", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("""
<div style="display:grid; grid-template-columns:1.5fr 0.8fr 2fr; gap:12px;
    padding:8px 14px; margin-bottom:6px; font-size:0.72rem; font-weight:700;
    text-transform:uppercase; letter-spacing:0.08em; color:#374151 !important;
    border-bottom:2px solid #e2e8f0;">
    <span style="color:#374151 !important;">Fault Type / Sensor</span>
    <span style="color:#374151 !important;">Severity</span>
    <span style="color:#374151 !important;">Recommended Action</span>
</div>
""", unsafe_allow_html=True)

for f in faults:
    st.markdown(f"""
    <div class="fault-row {f['row_class']}">
        <div>
            <div class="fault-name">{f['icon']} {f['fault']}</div>
            <div class="fault-sensor-text">{f['sensor']}</div>
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
    <span class="sec-head-icon" style="background:#fef9c3;">🔔</span>
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

alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
alert_rows = []
for f in faults:
    if f["fault"] != "No Faults Detected":
        alert_rows.append({
            "Timestamp": alert_time,
            "Machine":   machine_id,
            "Location":  location,
            "Fault":     f["fault"],
            "Severity":  f["severity"],
            "Action":    f["action"],
        })

if alert_rows:
    st.markdown("**📋 Active Alert Log**")
    st.table(pd.DataFrame(alert_rows))
else:
    st.info("📋 No active alerts in the system log.")

st.markdown("---")
st.markdown("### 🤖 AI-Inspired Maintenance Recommendations")

ai_recommendations = []
if temperature > 75:
    ai_recommendations.append(
        "High temperature detected — check cooling system and airflow.")
if vibration_rms > 500 or vibration_mm > 700:
    ai_recommendations.append(
        "High vibration levels — inspect bearings, coupling, and shaft alignment.")
if vibration_kurtosis > 5:
    ai_recommendations.append(
        "Abnormal vibration kurtosis — schedule vibration diagnostics for bearing faults.")
if pressure < 4.5:
    ai_recommendations.append(
        "Low pressure detected — inspect valves, piping leaks, and inlet restrictions.")
if not ai_recommendations:
    ai_recommendations.append(
        "System nominal. Continue routine predictive maintenance checks.")

for rec in ai_recommendations:
    st.info(f"💡 {rec}")

st.markdown("---")

# ═══════════════════════════════════════
#  SECTION 5 — DOWNTIME REDUCTION REPORT
# ═══════════════════════════════════════
st.markdown("""
<div class="sec-head">
    <span class="sec-head-icon" style="background:#dcfce7;">📊</span>
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
            <div class="saving-text">
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
        marker_color="#f87171", marker_line_color="#dc2626", marker_line_width=1,
    ))
    fig_bar.add_trace(go.Bar(
        name="Predictive AI", x=categories, y=pred_vals,
        marker_color="#4ade80", marker_line_color="#16a34a", marker_line_width=1,
    ))
    fig_bar.update_layout(
        barmode="group",
        title=dict(text="Downtime Breakdown by Phase (hours)",
                   font=dict(size=13, color="#0f172a")),
        height=280, margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="white", plot_bgcolor="white",
        legend=dict(orientation="h", y=-0.18,
                    font=dict(size=11, color="#374151")),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9",
                   title=dict(text="Hours", font=dict(color="#374151")),
                   tickfont=dict(color="#374151")),
        xaxis=dict(tickfont=dict(size=10, color="#374151")),
        font=dict(family="Inter", color="#374151"),
    )
    st.plotly_chart(fig_bar, width='stretch')

    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("Time Saved",
                  f"{TRAD_DOWNTIME - PRED_DOWNTIME} hrs", "per event")
    with r2:
        st.metric("Reduction", f"{reduction_pct}%", "downtime ↓")
    with r3:
        st.metric("Est. Cost Save", "₹48,000", "per incident")

# ── Footer ──
st.markdown("---")
st.markdown("""
<div style="text-align:center; font-size:0.72rem; color:#94a3b8 !important;
     letter-spacing:0.08em; padding: 8px 0 4px;">
    AIRLYTICS v2.0 &nbsp;·&nbsp; INDUSTRY 4.0 PROTOTYPE &nbsp;·&nbsp;
    AI-DRIVEN FAULT DETECTION &nbsp;·&nbsp; REAL-TIME SENSOR FUSION
</div>""", unsafe_allow_html=True)
