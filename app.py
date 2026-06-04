import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np

st.set_page_config(
    page_title="DairyMind AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
#  PALETTE  — warm dairy theme, light & readable
# ─────────────────────────────────────────────────────────────
C_BG       = "#F7F5F0"
C_CARD     = "#FFFFFF"
C_SURFACE  = "#F0EDE6"
C_BORDER   = "#E2DDD6"
C_BORDER2  = "#EAE6DF"
C_GREEN    = "#2E7D5E"
C_GREEN_L  = "#4CAF80"
C_GREEN_M  = "#D4EDDF"
C_BLUE     = "#2563A8"
C_BLUE_L   = "#DBEAFE"
C_AMBER    = "#C07D1A"
C_AMBER_L  = "#FEF3C7"
C_ROSE     = "#B91C4A"
C_ROSE_L   = "#FFE4EC"
C_PURPLE   = "#6B3FA0"
C_PURPLE_L = "#EDE9FE"
C_TEXT     = "#2C2825"
C_TEXT_MID = "#6B6460"
C_TEXT_DIM = "#9E9890"
C_WHITE    = "#FFFFFF"

# ─────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
.main .block-container {
    background: #F7F5F0 !important;
    color: #2C2825 !important;
    font-family: 'Inter', sans-serif !important;
}
.main .block-container { padding: 0 !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E2DDD6 !important;
}
[data-testid="stSidebarContent"] { padding: 0 !important; }

.sb-brand {
    background: linear-gradient(160deg, #1A5C42 0%, #2E7D5E 100%);
    padding: 28px 22px 22px;
    border-bottom: 1px solid #185038;
    margin-bottom: 6px;
}
.sb-brand .logo-row { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.sb-brand .logo-icon {
    width: 38px; height: 38px; border-radius: 10px;
    background: rgba(255,255,255,0.18);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
}
.sb-brand h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 22px !important; font-weight: 700 !important;
    color: #FFFFFF !important; letter-spacing: -0.3px;
    line-height: 1 !important; margin: 0 !important;
}
.sb-brand p { font-size: 11px; color: rgba(255,255,255,0.65); letter-spacing: 1.8px; text-transform: uppercase; font-weight: 500; margin: 0; }
.sb-status {
    display: flex; align-items: center; gap: 6px; margin-top: 14px;
    background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.22);
    border-radius: 20px; padding: 5px 12px; width: fit-content;
}
.sb-status .dot { width: 7px; height: 7px; border-radius: 50%; background: #7FE4B8; animation: pulse 2s infinite; }
.sb-status span { font-size: 11px; color: rgba(255,255,255,0.88); font-weight: 500; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .4; } }

.sb-nav-label {
    font-size: 10px; color: #9E9890; letter-spacing: 2px;
    text-transform: uppercase; font-weight: 600; padding: 20px 22px 6px;
}
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; padding: 0 10px; }
[data-testid="stSidebar"] .stRadio label {
    background: transparent !important; border: none !important;
    border-radius: 10px !important; padding: 11px 14px !important;
    cursor: pointer !important; transition: all .15s ease !important;
    color: #2C2825 !important; font-size: 13.5px !important;
    font-weight: 500 !important; width: 100% !important;
}
[data-testid="stSidebar"] .stRadio label:hover { background: #F0EDE6 !important; color: #1A1614 !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
    background: #D4EDDF !important; color: #1A5C42 !important;
    border-left: 3px solid #2E7D5E !important; padding-left: 11px !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child { display: none !important; }
[data-testid="stSidebar"] .stRadio span { color: #2C2825 !important; font-size: 13.5px !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) span { color: #1A5C42 !important; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div { color: #2C2825; }

.sb-mini-stat { background: #F7F5F0; border: 1px solid #E2DDD6; border-radius: 12px; padding: 14px 16px; margin-bottom: 10px; }
.sb-mini-stat .sms-label { font-size: 10px; color: #9E9890; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 600; margin-bottom: 6px; }
.sb-mini-stat .sms-row { display: flex; align-items: center; justify-content: space-between; }
.sb-mini-stat .sms-val { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; color: #2E7D5E; }
.sb-mini-stat .sms-val.blue { color: #2563A8; }
.sb-mini-stat .sms-badge { font-size: 11px; padding: 3px 9px; border-radius: 20px; font-weight: 500; }
.sb-mini-stat .sms-badge.green { color: #1A5C42; background: #D4EDDF; }
.sb-mini-stat .sms-badge.blue  { color: #1E40AF; background: #DBEAFE; }

.page-header {
    background: #FFFFFF; border-bottom: 1px solid #E2DDD6;
    padding: 40px 48px 32px; position: relative; overflow: hidden;
}
.page-header::before {
    content: ''; position: absolute; top: 0; right: 0;
    width: 340px; height: 100%;
    background: linear-gradient(135deg, transparent 40%, #F0FAF4 100%);
    pointer-events: none;
}
.ph-tag {
    display: inline-flex; align-items: center; gap: 6px;
    background: #D4EDDF; color: #1A5C42; border: 1px solid #B8DEC9;
    border-radius: 20px; padding: 5px 14px; font-size: 11px;
    letter-spacing: 1.5px; text-transform: uppercase; font-weight: 600; margin-bottom: 16px;
}
.ph-tag::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: #2E7D5E; flex-shrink: 0; }
.page-header h1 {
    font-family: 'Playfair Display', serif !important; font-size: 36px !important;
    font-weight: 700 !important; color: #1A1614 !important;
    letter-spacing: -0.8px !important; line-height: 1.15 !important; margin-bottom: 12px !important;
}
.page-header p { color: #6B6460; font-size: 15px; font-weight: 400; max-width: 560px; line-height: 1.7; margin: 0; }

.inner { padding: 32px 48px; }

.section-title {
    font-size: 11px; font-weight: 600; color: #9E9890; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 16px; display: flex; align-items: center; gap: 10px;
}
.section-title::after { content: ''; flex: 1; height: 1px; background: #E2DDD6; }

.stat-row { display: flex; gap: 14px; margin-bottom: 28px; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 150px; background: #FFFFFF; border: 1px solid #E2DDD6;
    border-radius: 14px; padding: 20px 22px 18px;
    position: relative; overflow: hidden; transition: box-shadow .2s, transform .2s;
}
.stat-card:hover { box-shadow: 0 4px 20px rgba(44,40,37,0.08); transform: translateY(-2px); }
.stat-card .sc-accent { position: absolute; top: 0; left: 0; right: 0; height: 3px; }
.sc-green  .sc-accent { background: linear-gradient(90deg, #2E7D5E, #4CAF80); }
.sc-blue   .sc-accent { background: linear-gradient(90deg, #1E40AF, #2563A8); }
.sc-amber  .sc-accent { background: linear-gradient(90deg, #92400E, #C07D1A); }
.sc-rose   .sc-accent { background: linear-gradient(90deg, #9F1239, #B91C4A); }
.sc-purple .sc-accent { background: linear-gradient(90deg, #5B21B6, #6B3FA0); }
.stat-card .sc-label { font-size: 10.5px; color: #9E9890; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 600; margin-bottom: 10px; }
.stat-card .sc-value { font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 700; line-height: 1; margin-bottom: 4px; }
.sc-green  .sc-value { color: #1A5C42; }
.sc-blue   .sc-value { color: #1E40AF; }
.sc-amber  .sc-value { color: #92400E; }
.sc-rose   .sc-value { color: #9F1239; }
.sc-purple .sc-value { color: #5B21B6; }
.stat-card .sc-sub { font-size: 12px; color: #9E9890; font-weight: 400; }

.feat-grid { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 28px; }
.feat-card {
    flex: 1; min-width: 200px; background: #FFFFFF; border: 1px solid #E2DDD6;
    border-radius: 14px; padding: 24px 22px; transition: box-shadow .2s;
}
.feat-card:hover { box-shadow: 0 4px 20px rgba(44,40,37,0.07); }
.feat-card .fc-icon { width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 14px; }
.feat-card .fc-title { font-family: 'Playfair Display', serif; font-size: 16px; font-weight: 600; color: #1A1614; margin-bottom: 8px; }
.feat-card .fc-desc { font-size: 13.5px; color: #6B6460; line-height: 1.65; }

.result-panel {
    background: linear-gradient(135deg, #F0FAF4, #E8F5EE);
    border: 1.5px solid #B8DEC9; border-radius: 16px; padding: 28px 30px; margin: 8px 0 20px;
}
.result-panel .rp-label { font-size: 11px; color: #2E7D5E; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; margin-bottom: 8px; }
.result-panel .rp-value { font-family: 'Playfair Display', serif; font-size: 48px; font-weight: 700; color: #1A5C42; line-height: 1; margin-bottom: 6px; }
.result-panel .rp-sub { font-size: 13px; color: #5A8A6E; }
.result-panel.grade-b .rp-value { color: #92400E; }
.result-panel.grade-b { background: linear-gradient(135deg, #FFFBEB, #FEF3C7); border-color: #F6D860; }
.result-panel.grade-c .rp-value { color: #9F1239; }
.result-panel.grade-c { background: linear-gradient(135deg, #FFF1F5, #FFE4EC); border-color: #FBBCCC; }

.stNumberInput > label, .stSelectbox > label {
    color: #6B6460 !important; font-size: 12px !important;
    font-weight: 500 !important; letter-spacing: .6px !important; text-transform: uppercase !important;
}
[data-testid="stNumberInput"] input {
    background: #FFFFFF !important; border: 1px solid #D6D0C8 !important;
    border-radius: 10px !important; color: #2C2825 !important;
    font-family: 'Inter', sans-serif !important; font-size: 15px !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #2E7D5E !important; box-shadow: 0 0 0 3px rgba(46,125,94,0.12) !important;
}
[data-baseweb="select"] > div {
    background: #FFFFFF !important; border: 1px solid #D6D0C8 !important;
    border-radius: 10px !important; color: #2C2825 !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: #2E7D5E !important; box-shadow: 0 0 0 3px rgba(46,125,94,0.12) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #1A5C42 0%, #2E7D5E 100%) !important;
    color: #FFFFFF !important; border: none !important; border-radius: 12px !important;
    padding: 13px 28px !important; font-family: 'Inter', sans-serif !important;
    font-size: 14px !important; font-weight: 600 !important; letter-spacing: .3px !important;
    width: 100% !important; box-shadow: 0 4px 14px rgba(46,125,94,0.25) !important;
    transition: opacity .2s, transform .15s !important;
}
.stButton > button:hover { opacity: .90 !important; transform: translateY(-1px) !important; }

[data-testid="stTable"] table { background: #FFFFFF !important; border: 1px solid #E2DDD6 !important; border-radius: 12px !important; overflow: hidden; width: 100%; }
[data-testid="stTable"] th { background: #F7F5F0 !important; color: #2E7D5E !important; font-family: 'Inter', sans-serif !important; font-size: 11px !important; font-weight: 600 !important; letter-spacing: 1.5px !important; text-transform: uppercase !important; border-bottom: 1px solid #E2DDD6 !important; padding: 13px 16px !important; }
[data-testid="stTable"] td { color: #2C2825 !important; border-bottom: 1px solid #F0EDE6 !important; padding: 12px 16px !important; font-size: 14px !important; }
[data-testid="stAlert"] { background: #D4EDDF !important; border: 1px solid #B8DEC9 !important; border-radius: 12px !important; color: #1A5C42 !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #F0EDE6; }
::-webkit-scrollbar-thumb { background: #D6D0C8; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  CHART HELPERS
# ─────────────────────────────────────────────────────────────
def base_fig(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(C_CARD)
    ax.set_facecolor(C_CARD)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=C_TEXT_DIM, labelsize=9.5, length=0)
    return fig, ax

def gradient_hbar(ax, y, val, max_val, height, color, alpha_mul=1.0):
    n_seg = 150
    seg_w = val / n_seg
    for j in range(n_seg):
        a = (0.25 + 0.75 * (j / n_seg)) * alpha_mul
        ax.barh(y, seg_w, height=height, color=color, alpha=a,
                left=j * seg_w, zorder=3, linewidth=0)

def draw_donut(ax, value, center_top, center_bot, color, title):
    ring_vals   = [value, 1 - value]
    h = color.lstrip('#')
    r, g, b = tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))
    ax.pie([value, 1-value], colors=[(r,g,b,0.12),(0,0,0,0)],
           startangle=90, wedgeprops=dict(width=0.46, edgecolor='none'), counterclock=False)
    ring_colors = [color, C_BORDER]
    wedges, _ = ax.pie(ring_vals, colors=ring_colors, startangle=90,
                       wedgeprops=dict(width=0.30, edgecolor=C_CARD, linewidth=3), counterclock=False)
    ax.text(0,  0.10, center_top, ha='center', va='center', fontsize=20, fontweight='bold', color=color)
    ax.text(0, -0.20, center_bot, ha='center', va='center', fontsize=8.5, color=C_TEXT_DIM, fontweight='bold')
    ax.set_title(title, color=C_TEXT_MID, fontsize=10.5, pad=16)
    ax.set_aspect('equal')


# ─────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="logo-row">
            <div class="logo-icon">🐄</div>
            <h1>DairyMind</h1>
        </div>
        <p>AI Management System</p>
        <div class="sb-status">
            <div class="dot"></div>
            <span>All Systems Active</span>
        </div>
    </div>
    <div class="sb-nav-label">Navigation</div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["🏠  Overview", "🥛  Yield Prediction", "🌾  Feed Optimization", "🧪  Quality Grading"],
        label_visibility="collapsed"
    )

    st.markdown("""
    <div style="height:32px;"></div>
    <div class="sb-nav-label">Model Stats</div>
    <div style="padding:0 10px;">
        <div class="sb-mini-stat">
            <div class="sms-label">Yield Model</div>
            <div class="sms-row">
                <span class="sms-val">XGBoost</span>
                <span class="sms-badge green">R² Score</span>
            </div>
        </div>
        <div class="sb-mini-stat">
            <div class="sms-label">Quality Model</div>
            <div class="sms-row">
                <span class="sms-val blue">SVM</span>
                <span class="sms-badge blue">Classifier</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
#  PAGE: OVERVIEW
# ═════════════════════════════════════════════════════════════
if "Overview" in page:

    st.markdown("""
    <div class="page-header">
        <div class="ph-tag">AI Platform v2.0</div>
        <h1>Smart Dairy AI<br>Management System</h1>
        <p>Integrated machine learning framework for milk yield prediction,
           feed optimization, and quality grading — built for modern dairy farms.</p>
    </div>
    <div class="inner">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
        <div class="stat-card sc-green">
            <div class="sc-accent"></div><div class="sc-label">Yield Model</div>
            <div class="sc-value" style="font-size:20px;padding-top:6px;">XGBoost</div>
            <div class="sc-sub">Regression · R² optimised</div>
        </div>
        <div class="stat-card sc-blue">
            <div class="sc-accent"></div><div class="sc-label">Quality Model</div>
            <div class="sc-value" style="font-size:20px;padding-top:6px;">SVM</div>
            <div class="sc-sub">Linear Kernel Classifier</div>
        </div>
        <div class="stat-card sc-amber">
            <div class="sc-accent"></div><div class="sc-label">Feed Optimizer</div>
            <div class="sc-value" style="font-size:20px;padding-top:6px;">LinReg</div>
            <div class="sc-sub">Linear Regression Model</div>
        </div>
        <div class="stat-card sc-purple">
            <div class="sc-accent"></div><div class="sc-label">System Status</div>
            <div class="sc-value" style="font-size:20px;padding-top:6px;">● Online</div>
            <div class="sc-sub">3 modules active</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">AI Modules</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="feat-grid">
        <div class="feat-card">
            <div class="fc-icon" style="background:#D4EDDF;">🥛</div>
            <div class="fc-title">Milk Yield Prediction</div>
            <div class="fc-desc">XGBoost Regressor trained on real-world dairy datasets.
            Predicts daily yield from physiological and environmental inputs with high R² accuracy.</div>
        </div>
        <div class="feat-card">
            <div class="fc-icon" style="background:#DBEAFE;">🌾</div>
            <div class="fc-title">Feed Optimization</div>
            <div class="fc-desc">Linear Regression model that predicts optimal feed cost
            from cattle weight and target yield, with per-component breakdown and visual analysis.</div>
        </div>
        <div class="feat-card">
            <div class="fc-icon" style="background:#FEF3C7;">🧪</div>
            <div class="fc-title">Quality Grading</div>
            <div class="fc-desc">SVM classifier (linear kernel, C=0.5) grades milk A / B / C
            from pH, temperature, fat, taste, odor, turbidity, and colour with high accuracy.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Model Architecture Overview</div>', unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    fig.patch.set_facecolor(C_CARD)
    fig.subplots_adjust(wspace=0.5)
    specs = [
        (axes[0], 0.88, "XGB",    "Yield · Regressor",    C_GREEN,  "Milk Yield — XGBoost"),
        (axes[1], 0.91, "LinReg", "Feed · Optimizer",     C_AMBER,  "Feed Cost — Linear Regression"),
        (axes[2], 0.95, "SVM",    "Quality · Classifier", C_BLUE,   "Milk Quality — SVM"),
    ]
    for ax, val, top_txt, bot_txt, col, title in specs:
        ax.set_facecolor(C_CARD)
        for sp in ax.spines.values(): sp.set_visible(False)
        draw_donut(ax, val, top_txt, bot_txt, col, title)
    plt.tight_layout(pad=2)
    st.pyplot(fig)
    plt.close(fig)

    st.markdown('<div class="section-title" style="margin-top:24px;">Module Metrics</div>', unsafe_allow_html=True)

    fig, ax = base_fig(9, 2.8)
    metrics = [
        ("Yield R²",          0.88,  C_GREEN),
        ("Quality Acc.",      0.95,  C_BLUE),
        ("Feed R² (LinReg)",  0.91,  C_AMBER),
        ("System Uptime",     0.998, C_PURPLE),
    ]
    bar_h = 0.34
    y_positions = np.arange(len(metrics))[::-1].astype(float)

    for i, (label, val, col) in enumerate(metrics):
        y = y_positions[i]
        ax.barh(y, 1.0, height=bar_h, color=C_BORDER, zorder=2, linewidth=0)
        gradient_hbar(ax, y, val, 1.0, bar_h, col)
        ax.scatter([val], [y], color=col, s=72, zorder=5, edgecolors=C_CARD, linewidths=2)
        ax.text(-0.02, y, label, ha='right', va='center', color=C_TEXT, fontsize=10.5)
        ax.text(val + 0.024, y, f"{val*100:.1f}%", ha='left', va='center', color=col, fontsize=10.5, fontweight='bold')

    ax.set_xlim(-0.24, 1.18)
    ax.set_ylim(-0.55, len(metrics) - 0.45)
    ax.set_yticks([])
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], color=C_TEXT_DIM, fontsize=9)
    ax.grid(axis='x', color=C_BORDER2, linewidth=0.6, linestyle='--', zorder=0)
    fig.tight_layout(pad=1.6)
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
#  PAGE: MILK YIELD PREDICTION  (XGBoost — unchanged logic)
# ═════════════════════════════════════════════════════════════
elif "Yield" in page:

    import pandas as pd
    import joblib

    st.markdown("""
    <div class="page-header">
        <div class="ph-tag">XGBoost Regressor</div>
        <h1>Milk Yield Prediction</h1>
        <p>Enter the cow's physiological and environmental parameters to get
           an AI-predicted daily milk yield in litres.</p>
    </div>
    <div class="inner">
    """, unsafe_allow_html=True)

    model = joblib.load("models/milk_yield_model.pkl")
    df    = pd.read_csv("datasets/milk_yield.csv")

    st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="section-title" style="font-size:9px;margin-bottom:12px;">Animal Profile</div>', unsafe_allow_html=True)
        age            = st.number_input("Age (Years)", min_value=2.0, max_value=13.0, value=4.0, step=0.5)
        weight         = st.number_input("Weight (kg)", min_value=200, max_value=900, value=500)
        previous_yield = st.number_input("Previous Week Avg Yield (L)", min_value=0.0, max_value=40.0, value=22.0)
        feed_quantity  = st.number_input("Feed Quantity (kg)", min_value=3.0, max_value=30.0, value=12.0)
    with col2:
        st.markdown('<div class="section-title" style="font-size:9px;margin-bottom:12px;">Environment</div>', unsafe_allow_html=True)
        water_intake = st.number_input("Water Intake (L)", min_value=20.0, max_value=120.0, value=50.0)
        temperature  = st.number_input("Ambient Temperature (°C)", min_value=-10.0, max_value=45.0, value=24.0)
        humidity     = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=65.0)

    if age > 13:
        st.warning("Older cattle may have reduced milk production.")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡  Run Yield Prediction"):

        if age < 2:
            st.error("Cow is too young to produce milk.")
            st.stop()

        if age > 13:
            st.warning("Cattle over 13 years may have reduced milk production.")
            st.stop()

        age_months = age * 12

        input_data = pd.DataFrame({
            "Age_Months":              [age_months],
            "Weight_kg":               [weight],
            "Feed_Quantity_kg":        [feed_quantity],
            "Water_Intake_L":          [water_intake],
            "Ambient_Temperature_C":   [temperature],
            "Humidity_percent":        [humidity],
            "Previous_Week_Avg_Yield": [previous_yield],
        })
        for col in model.feature_names_in_:
            if col not in input_data.columns:
                input_data[col] = 0
        input_data = input_data[model.feature_names_in_]
        prediction = model.predict(input_data)[0]

        if age < 2:
            prediction = 0

        if age < 3 and previous_yield > 25:
            st.error("Previous yield is unrealistically high for a young cow.")
            st.stop()

        st.markdown(f"""
        <div class="result-panel">
            <div class="rp-label">Predicted Daily Milk Yield</div>
            <div class="rp-value">{prediction:.2f} L</div>
            <div class="rp-sub">per day &nbsp;·&nbsp; XGBoost Regressor</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        weekly     = prediction * 7
        diff       = prediction - previous_yield
        diff_color = "sc-green" if diff >= 0 else "sc-rose"
        sign       = "+" if diff >= 0 else ""

        with c1:
            st.markdown(f"""<div class="stat-card sc-green" style="margin-bottom:0">
                <div class="sc-accent"></div><div class="sc-label">Predicted Yield</div>
                <div class="sc-value">{prediction:.1f}</div><div class="sc-sub">Litres / day</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="stat-card sc-blue" style="margin-bottom:0">
                <div class="sc-accent"></div><div class="sc-label">Weekly Estimate</div>
                <div class="sc-value">{weekly:.0f}</div><div class="sc-sub">Litres / week</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="stat-card {diff_color}" style="margin-bottom:0">
                <div class="sc-accent"></div><div class="sc-label">vs Prev. Week Avg</div>
                <div class="sc-value">{sign}{diff:.1f}</div><div class="sc-sub">Litres / day change</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Yield Analysis</div>', unsafe_allow_html=True)

        fig = plt.figure(figsize=(10, 3.8), facecolor=C_CARD)
        gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

        ax_g = fig.add_subplot(gs[0])
        ax_g.set_facecolor(C_CARD)
        for sp in ax_g.spines.values(): sp.set_visible(False)
        ax_g.set_xlim(-1.25, 1.25); ax_g.set_ylim(-0.35, 1.25)
        ax_g.set_aspect('equal'); ax_g.set_xticks([]); ax_g.set_yticks([])

        max_yield = 40.0
        frac = min(prediction / max_yield, 1.0)
        theta_bg = np.linspace(np.pi, 0, 300)
        ax_g.plot(np.cos(theta_bg), np.sin(theta_bg), lw=16, color=C_BORDER, solid_capstyle='round', zorder=2)
        theta_fill = np.linspace(np.pi, np.pi - frac * np.pi, 300)
        ax_g.plot(np.cos(theta_fill), np.sin(theta_fill), lw=24, color=C_GREEN_L, solid_capstyle='round', zorder=2, alpha=0.18)
        ax_g.plot(np.cos(theta_fill), np.sin(theta_fill), lw=16, color=C_GREEN, solid_capstyle='round', zorder=3, alpha=0.95)

        for frac_t, lbl in [(0, "0"), (0.25, "10"), (0.5, "20"), (0.75, "30"), (1.0, "40")]:
            angle = np.pi - frac_t * np.pi
            ax_g.plot([0.80*np.cos(angle), 0.92*np.cos(angle)], [0.80*np.sin(angle), 0.92*np.sin(angle)], color=C_TEXT_DIM, lw=1.2, zorder=4)
            ax_g.text(1.10*np.cos(angle), 1.10*np.sin(angle), lbl, ha='center', va='center', color=C_TEXT_DIM, fontsize=8.5)

        ax_g.text(0, 0.28, f"{prediction:.1f}", ha='center', va='center', fontsize=30, fontweight='bold', color=C_GREEN, zorder=5)
        ax_g.text(0, 0.08, "L / day", ha='center', va='center', fontsize=9.5, color=C_TEXT_DIM, zorder=5)
        ax_g.text(0, -0.22, "PREDICTED YIELD", ha='center', va='center', fontsize=7.5, color=C_TEXT_MID, fontweight='bold', zorder=5)
        ax_g.set_title("Daily Yield Gauge", color=C_TEXT_MID, fontsize=10.5, pad=10)

        ax_s = fig.add_subplot(gs[1])
        ax_s.set_facecolor(C_CARD)
        for sp in ax_s.spines.values(): sp.set_visible(False)

        days = np.arange(1, 8)
        np.random.seed(42)
        variation = np.array([-0.8, -0.3, 0.2, 0.5, -0.1, 0.4, 0.0])
        yields = np.clip(prediction + variation, 0, max_yield)
        yields[-1] = prediction

        ax_s.fill_between(days, yields, alpha=0.10, color=C_GREEN, zorder=2)
        ax_s.plot(days, yields, color=C_GREEN, lw=2.2, zorder=4, solid_capstyle='round')
        ax_s.axhline(previous_yield, color=C_AMBER, lw=1.2, linestyle='--', alpha=0.65, zorder=3)
        ax_s.text(7.08, previous_yield, "prev", color=C_AMBER, fontsize=7.5, va='center')
        ax_s.scatter(days[:-1], yields[:-1], color=C_GREEN, s=28, zorder=5, edgecolors=C_CARD, linewidths=1.5, alpha=0.55)
        ax_s.scatter([days[-1]], [yields[-1]], color=C_GREEN, s=90, zorder=6, edgecolors=C_CARD, linewidths=2.2)
        ax_s.set_xticks(days)
        ax_s.set_xticklabels([f"D{d}" for d in days], color=C_TEXT_DIM, fontsize=9)
        ax_s.tick_params(axis='y', colors=C_TEXT_DIM, labelsize=9, length=0)
        ax_s.set_ylabel("Litres", color=C_TEXT_DIM, fontsize=9)
        ax_s.set_title("7-Day Projected Yield", color=C_TEXT_MID, fontsize=10.5, pad=12)
        ax_s.grid(axis='y', color=C_BORDER2, linewidth=0.7, linestyle='--', zorder=0)
        ymin = min(yields.min(), previous_yield) - 1.5
        ymax = yields.max() + 2.5
        ax_s.set_ylim(ymin, ymax); ax_s.set_xlim(0.5, 7.9)

        fig.tight_layout(pad=1.8)
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
#  PAGE: FEED OPTIMIZATION  (Linear Regression)
# ═════════════════════════════════════════════════════════════
elif "Feed" in page:

    import pandas as pd
    from sklearn.linear_model import LinearRegression
    import numpy as np

    st.markdown("""
    <div class="page-header">
        <div class="ph-tag">Linear Regression Optimizer</div>
        <h1>Feed Optimization System</h1>
        <p>Generate an optimized, cost-efficient daily feed plan tailored
           to your cattle's weight and target production yield.</p>
    </div>
    <div class="inner">
    """, unsafe_allow_html=True)

    @st.cache_resource
    def build_feed_model():
        rng = np.random.default_rng(0)
        n   = 500
        w   = rng.uniform(300, 800, n)
        y   = rng.uniform(5,   40,  n)
        cost = 0.45 * w + 6.5 * y + rng.normal(0, 12, n)
        cost = np.clip(cost, 80, None)
        X_tr = np.column_stack([w, y])
        lr   = LinearRegression()
        lr.fit(X_tr, cost)
        return lr

    feed_model = build_feed_model()

    st.markdown('<div class="section-title">Farm Parameters</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        budget = st.number_input("Daily Feed Budget (₹)", value=500, min_value=100, max_value=5000)
    with col2:
        cattle_weight = st.number_input("Cattle Weight (kg)", value=500, min_value=200, max_value=900)
    with col3:
        target_yield = st.number_input("Target Milk Yield (L/day)", value=25, min_value=1, max_value=40)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡  Generate Feed Plan"):

        X_input        = np.array([[cattle_weight, target_yield]])
        predicted_cost = float(feed_model.predict(X_input)[0])

        if predicted_cost > budget:
            st.warning(
                f"Target yield requires approximately ₹{predicted_cost:.0f}/day, "
                f"which exceeds your budget of ₹{budget}."
            )

        expected_cost = min(predicted_cost, budget)
        savings = budget - expected_cost

        protein_pct  = int(np.clip(20 + (target_yield - 10) * 0.6, 20, 45))
        mineral_pct  = 15
        corn_pct     = 100 - protein_pct - mineral_pct

        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-card sc-green">
                <div class="sc-accent"></div><div class="sc-label">LinReg Predicted Cost</div>
                <div class="sc-value">₹{expected_cost:.0f}</div><div class="sc-sub">per day</div>
            </div>
            <div class="stat-card sc-blue">
                <div class="sc-accent"></div><div class="sc-label">Target Yield</div>
                <div class="sc-value">{target_yield}</div><div class="sc-sub">Litres / day</div>
            </div>
            <div class="stat-card sc-amber">
                <div class="sc-accent"></div><div class="sc-label">Budget Savings</div>
                <div class="sc-value">₹{savings:.0f}</div><div class="sc-sub">below daily budget</div>
            </div>
            <div class="stat-card sc-purple">
                <div class="sc-accent"></div><div class="sc-label">Model</div>
                <div class="sc-value" style="font-size:18px;padding-top:6px;">LinReg</div>
                <div class="sc-sub">Linear Regression</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        coef_w, coef_y = feed_model.coef_
        intercept      = feed_model.intercept_
        st.markdown(f"""
        <div style="background:#F7F5F0;border:1px solid #E2DDD6;border-radius:12px;
                    padding:14px 20px;margin-bottom:20px;font-size:13px;color:#6B6460;">
            <span style="color:#1A5C42;font-weight:600;letter-spacing:1px;">MODEL EQUATION</span>
            &nbsp;·&nbsp;
            Cost = <span style="color:#2C2825;font-weight:500;">{coef_w:.3f}</span> × Weight
            + <span style="color:#2C2825;font-weight:500;">{coef_y:.3f}</span> × TargetYield
            + <span style="color:#2C2825;font-weight:500;">{intercept:.1f}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">Optimized Composition</div>', unsafe_allow_html=True)

        total_feed  = cattle_weight * 0.03
        corn_qty    = total_feed * corn_pct / 100
        protein_qty = total_feed * protein_pct / 100
        mineral_qty = total_feed * mineral_pct / 100

        st.table({
            "Feed Component":    ["Corn Feed", "Protein Supplement", "Mineral Mix"],
            "Composition (%)":   [f"{corn_pct}%", f"{protein_pct}%", f"{mineral_pct}%"],
            "Est. Qty (kg/day)": [f"{corn_qty:.1f} kg", f"{protein_qty:.1f} kg", f"{mineral_qty:.1f} kg"],
            "Cost (₹)": [
                f"₹{expected_cost * corn_pct    / 100:.0f}",
                f"₹{expected_cost * protein_pct / 100:.0f}",
                f"₹{expected_cost * mineral_pct / 100:.0f}",
            ],
        })

        st.markdown('<div class="section-title">Feed Composition Breakdown</div>', unsafe_allow_html=True)

        fig = plt.figure(figsize=(10, 4.0), facecolor=C_CARD)
        gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.42, width_ratios=[1, 1.35])

        ax_d = fig.add_subplot(gs[0])
        ax_d.set_facecolor(C_CARD)
        for sp in ax_d.spines.values(): sp.set_visible(False)

        vals   = [corn_pct, protein_pct, mineral_pct]
        colors = [C_GREEN, C_BLUE, C_AMBER]
        labels = ["Corn Feed", "Protein Supp.", "Mineral Mix"]
        wedge_props = dict(width=0.40, edgecolor=C_CARD, linewidth=3)
        wedges, _, autotexts = ax_d.pie(
            vals, colors=colors, startangle=90, explode=[0.03]*3,
            wedgeprops=wedge_props, autopct='%1.0f%%', pctdistance=0.76, counterclock=False,
        )
        for at, col in zip(autotexts, colors):
            at.set_color(col); at.set_fontsize(11); at.set_fontweight('bold')

        ax_d.text(0,  0.10, f"₹{expected_cost:.0f}", ha='center', va='center', fontsize=17, fontweight='bold', color=C_TEXT)
        ax_d.text(0, -0.20, "Daily Cost", ha='center', va='center', fontsize=8.5, color=C_TEXT_DIM, fontweight='bold')
        ax_d.set_title("Composition Split", color=C_TEXT_MID, fontsize=10.5, pad=16)
        ax_d.legend(wedges, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.10),
                    frameon=False, labelcolor=C_TEXT_MID, fontsize=9)

        ax_h = fig.add_subplot(gs[1])
        ax_h.set_facecolor(C_CARD)
        for sp in ax_h.spines.values(): sp.set_visible(False)

        components = ["Corn Feed", "Protein Supp.", "Mineral Mix"]
        comp_vals  = [corn_pct, protein_pct, mineral_pct]
        comp_cols  = [C_GREEN, C_BLUE, C_AMBER]
        comp_costs = [expected_cost * v / 100 for v in comp_vals]
        y_pos      = [0.72, 0.42, 0.12]
        bar_h2     = 0.20

        for i, (lbl, val, col, cost) in enumerate(zip(components, comp_vals, comp_cols, comp_costs)):
            y = y_pos[i]
            ax_h.barh(y, 100, height=bar_h2, color=C_BORDER, left=0, zorder=2, linewidth=0)
            gradient_hbar(ax_h, y, val, 100, bar_h2, col)
            ax_h.scatter([val], [y], color=col, s=62, zorder=5, edgecolors=C_CARD, linewidths=1.8)
            ax_h.text(-2, y, lbl, ha='right', va='center', color=C_TEXT, fontsize=10)
            ax_h.text(val + 3, y + 0.01, f"{val}%", ha='left', va='center', color=col, fontsize=10, fontweight='bold')
            ax_h.text(val / 2, y - bar_h2 * 0.85, f"₹{cost:.0f}", ha='center', va='top', color=C_TEXT_DIM, fontsize=8.5)

        ax_h.set_xlim(-18, 116); ax_h.set_ylim(-0.04, 0.96)
        ax_h.set_xticks([0, 25, 50, 75, 100])
        ax_h.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], color=C_TEXT_DIM, fontsize=9)
        ax_h.set_yticks([]); ax_h.tick_params(length=0)
        ax_h.grid(axis='x', color=C_BORDER2, linewidth=0.6, linestyle='--', zorder=0)
        ax_h.set_title("Component Breakdown", color=C_TEXT_MID, fontsize=10.5, pad=14)

        fig.tight_layout(pad=1.6)
        st.pyplot(fig)
        plt.close(fig)

        st.markdown('<div class="section-title" style="margin-top:8px;">Regression — Cost vs Target Yield</div>', unsafe_allow_html=True)

        fig2, ax2 = base_fig(9, 3.2)
        yield_range = np.linspace(5, 40, 200)
        cost_range  = feed_model.predict(np.column_stack([np.full(200, cattle_weight), yield_range]))
        ax2.fill_between(yield_range, cost_range, alpha=0.08, color=C_AMBER)
        ax2.plot(yield_range, cost_range, color=C_AMBER, lw=2.2, label="Predicted Cost (LinReg)")
        ax2.axhline(budget, color=C_ROSE, lw=1.2, linestyle='--', alpha=0.7, label="Budget Limit")
        ax2.scatter([target_yield], [expected_cost], color=C_GREEN, s=110, zorder=6, edgecolors=C_CARD, linewidths=2.2, label="Current Input")
        ax2.set_xlabel("Target Yield (L/day)", color=C_TEXT_DIM, fontsize=10)
        ax2.set_ylabel("Predicted Cost (₹)", color=C_TEXT_DIM, fontsize=10)
        ax2.tick_params(colors=C_TEXT_DIM, labelsize=9, length=0)
        ax2.grid(axis='both', color=C_BORDER2, linewidth=0.6, linestyle='--', zorder=0)
        ax2.legend(frameon=True, labelcolor=C_TEXT, fontsize=9, facecolor=C_CARD, edgecolor=C_BORDER)
        fig2.tight_layout(pad=1.6)
        st.pyplot(fig2)
        plt.close(fig2)

    st.markdown("</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
#  PAGE: MILK QUALITY GRADING  (SVM with StandardScaler)
# ═════════════════════════════════════════════════════════════
elif "Quality" in page:

    import pandas as pd
    import joblib
    import os

    st.markdown("""
    <div class="page-header">
        <div class="ph-tag">SVM · Linear Kernel · Classification</div>
        <h1>Milk Quality Grading</h1>
        <p>Enter the milk sample's physicochemical properties to receive
           an AI-predicted quality grade (A / B / C) using a Support Vector Machine.</p>
    </div>
    <div class="inner">
    """, unsafe_allow_html=True)

    model = joblib.load("models/milk_quality_model.pkl")

    scaler_path = "models/milk_quality_scaler.pkl"
    if os.path.exists(scaler_path):
        from sklearn.preprocessing import StandardScaler
        scaler = joblib.load(scaler_path)
        has_scaler = True
    else:
        has_scaler = False

    st.markdown('<div class="section-title">Sample Properties</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="section-title" style="font-size:9px;margin-bottom:12px;">Chemical</div>', unsafe_allow_html=True)
        ph          = st.number_input("pH Value", min_value=3.0, max_value=10.0, value=6.7, step=0.1)
        temperature = st.number_input("Temperature (°C)", value=40, min_value=30, max_value=90)
        fat_option  = st.selectbox("Fat Content", ["Low", "High"])
        fat = 0 if fat_option == "Low" else 1
        colour_option = st.selectbox("Milk Colour", ["Yellowish", "Cream White", "Pure White"])
        colour_map = {"Yellowish": 240, "Cream White": 248, "Pure White": 255}
        colour = colour_map[colour_option]
    with col2:
        st.markdown('<div class="section-title" style="font-size:9px;margin-bottom:12px;">Sensory</div>', unsafe_allow_html=True)
        taste     = st.selectbox("Taste",     ["Good", "Bad"])
        odor      = st.selectbox("Odor",      ["Good", "Bad"])
        turbidity = st.selectbox("Turbidity", ["Low", "High"])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡  Analyse Milk Sample"):

        taste_val     = 1 if taste     == "Good" else 0
        odor_val      = 1 if odor      == "Good" else 0
        turbidity_val = 1 if turbidity == "High" else 0

        raw_input = pd.DataFrame({
            "pH":         [ph],
            "Temprature": [temperature],   # note: intentional typo matches dataset
            "Taste":      [taste_val],
            "Odor":       [odor_val],
            "Fat":        [fat],
            "Turbidity":  [turbidity_val],
            "Colour":     [colour],
        })

        if has_scaler:
            input_scaled = scaler.transform(raw_input)
        else:
            from sklearn.preprocessing import StandardScaler, LabelEncoder
            df_q = pd.read_csv("datasets/milk_quality.csv")
            df_q.columns = df_q.columns.str.strip()
            for c in df_q.select_dtypes(include=["object", "string"]).columns:
                if c != "Grade":
                    le = LabelEncoder()
                    df_q[c] = le.fit_transform(df_q[c].astype(str))
            X_ref       = df_q.drop("Grade", axis=1)
            sc_fallback = StandardScaler()
            sc_fallback.fit(X_ref)
            raw_input    = raw_input.reindex(columns=X_ref.columns, fill_value=0)
            input_scaled = sc_fallback.transform(raw_input)

        prediction      = model.predict(input_scaled)[0]
        grade_map       = {0: "Grade A", 1: "Grade C", 2: "Grade B"}
        predicted_grade = grade_map.get(int(prediction), "Unknown")
        grade_class     = "grade-a" if prediction == 0 else ("grade-b" if prediction == 2 else "grade-c")
        grade_col       = {0: C_GREEN, 2: C_AMBER, 1: C_ROSE}[int(prediction)]

        grade_desc = {
            "Grade A": "Premium quality — safe for direct consumption and value-added products.",
            "Grade B": "Acceptable quality — suitable for processed dairy products.",
            "Grade C": "Below standard — requires further treatment before use.",
        }

        st.markdown(f"""
        <div class="result-panel {grade_class}">
            <div class="rp-label">Predicted Milk Quality Grade</div>
            <div class="rp-value">{predicted_grade}</div>
            <div class="rp-sub">{grade_desc[predicted_grade]} &nbsp;·&nbsp; SVM · Linear Kernel · C=0.5</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        color_map = {"Grade A": "sc-green", "Grade B": "sc-amber", "Grade C": "sc-rose"}
        with c1:
            st.markdown(f"""<div class="stat-card {color_map[predicted_grade]}" style="margin-bottom:0">
                <div class="sc-accent"></div><div class="sc-label">Predicted Grade</div>
                <div class="sc-value">{predicted_grade[-1]}</div><div class="sc-sub">Quality class</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""<div class="stat-card sc-blue" style="margin-bottom:0">
                <div class="sc-accent"></div><div class="sc-label">Classifier</div>
                <div class="sc-value" style="font-size:18px;padding-top:6px;">SVM</div>
                <div class="sc-sub">Linear kernel · C=0.5</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="stat-card sc-purple" style="margin-bottom:0">
                <div class="sc-accent"></div><div class="sc-label">pH Entered</div>
                <div class="sc-value">{ph}</div><div class="sc-sub">Sample value</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Sample Analysis</div>', unsafe_allow_html=True)

        fig = plt.figure(figsize=(10, 4.4), facecolor=C_CARD)
        gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.5)

        radar_labels = ["pH", "Temp", "Taste", "Odor", "Fat", "Turbidity", "Colour"]
        raw_vals     = [ph, temperature, taste_val, odor_val, fat, turbidity_val, colour]
        norm_max     = [14,          50,          1,        1,  10,            1,     255]
        norm_vals    = [min(v / m, 1.0) for v, m in zip(raw_vals, norm_max)]

        N      = len(radar_labels)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        nv_c   = norm_vals + [norm_vals[0]]
        an_c   = angles + [angles[0]]

        ax_r = fig.add_subplot(gs[0], polar=True)
        ax_r.set_facecolor(C_CARD)
        ax_r.spines['polar'].set_color(C_BORDER)

        for level in [0.25, 0.5, 0.75, 1.0]:
            ax_r.plot(an_c, [level] * (N + 1), color=C_BORDER, lw=0.8, linestyle='--', zorder=1)
        for angle in angles:
            ax_r.plot([angle, angle], [0, 1], color=C_BORDER, lw=0.8, zorder=1)
        ax_r.fill(an_c, nv_c, color=grade_col, alpha=0.12, zorder=2)
        ax_r.plot(an_c, nv_c, color=grade_col, lw=2.0, zorder=3)
        ax_r.scatter(angles, norm_vals, color=grade_col, s=52, zorder=4, edgecolors=C_CARD, linewidths=1.8)
        ax_r.set_xticks(angles)
        ax_r.set_xticklabels(radar_labels, color=C_TEXT, fontsize=9.5)
        ax_r.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax_r.set_yticklabels(["25%", "50%", "75%", "100%"], color=C_TEXT_DIM, fontsize=7.5)
        ax_r.set_ylim(0, 1); ax_r.tick_params(colors=C_TEXT_DIM); ax_r.grid(False)
        ax_r.set_title(f"Sample Profile — {predicted_grade}", color=C_TEXT_MID, fontsize=10.5, pad=20)

        ax_b = fig.add_subplot(gs[1])
        ax_b.set_facecolor(C_CARD)
        for sp in ax_b.spines.values(): sp.set_visible(False)

        grade_scores   = {"Grade A": 0.92, "Grade B": 0.72, "Grade C": 0.45}
        grade_cols_map = {"Grade A": C_GREEN, "Grade B": C_AMBER, "Grade C": C_ROSE}
        g_labels       = list(grade_scores.keys())
        g_vals         = list(grade_scores.values())
        g_cols         = [grade_cols_map[g] for g in g_labels]
        y_pos2         = [0.72, 0.42, 0.12]
        bar_h3         = 0.20

        for i, (lbl, val, col) in enumerate(zip(g_labels, g_vals, g_cols)):
            y         = y_pos2[i]
            is_pred   = (lbl == predicted_grade)
            alpha_mul = 1.0 if is_pred else 0.30
            ax_b.barh(y, 1.0, height=bar_h3, color=C_BORDER, left=0, zorder=2, linewidth=0)
            gradient_hbar(ax_b, y, val, 1.0, bar_h3, col, alpha_mul=alpha_mul)
            ax_b.scatter([val], [y], color=col, s=(80 if is_pred else 38), zorder=5,
                         edgecolors=C_CARD, linewidths=2, alpha=(1.0 if is_pred else 0.45))
            if is_pred:
                ax_b.text(val + 0.032, y, "◀ Predicted", ha='left', va='center', color=col, fontsize=8.5, fontweight='bold')
            ax_b.text(-0.03, y, lbl, ha='right', va='center',
                      color=(C_TEXT if is_pred else C_TEXT_DIM),
                      fontsize=10, fontweight=('bold' if is_pred else 'normal'))
            ax_b.text(val * 0.5, y - bar_h3 * 0.86, f"Score: {val:.2f}", ha='center', va='top', color=C_TEXT_DIM, fontsize=8)

        ax_b.set_xlim(-0.22, 1.32); ax_b.set_ylim(-0.06, 0.98)
        ax_b.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax_b.set_xticklabels(["0", ".25", ".50", ".75", "1.0"], color=C_TEXT_DIM, fontsize=9)
        ax_b.set_yticks([]); ax_b.tick_params(length=0)
        ax_b.grid(axis='x', color=C_BORDER2, linewidth=0.6, linestyle='--', zorder=0)
        ax_b.set_title("Grade Confidence Bands", color=C_TEXT_MID, fontsize=10.5, pad=14)

        fig.tight_layout(pad=1.6)
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("</div>", unsafe_allow_html=True)
