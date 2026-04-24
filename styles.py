"""
Shared premium dark-theme CSS for Smart Campus Intelligence System.
Import and call inject_css() at the top of every page.
"""

GLOBAL_CSS = """
<style>
/* ── Google Fonts ─────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Global Reset ─────────────────────────────── */
*:not(.material-symbols-rounded):not(.material-icons) {
    font-family: 'Inter', sans-serif !important;
}
*, *::before, *::after {
    box-sizing: border-box;
}

/* ── App Background ───────────────────────────── */
.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0f0f2d 40%, #0a1628 100%) !important;
    min-height: 100vh;
}

/* ── Hide Streamlit branding ──────────────────── */
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar ──────────────────────────────────── */
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d2b 0%, #0a1628 60%, #050d1a 100%) !important;
    border-right: 1px solid rgba(100, 120, 255, 0.15) !important;
}
div[data-testid="stSidebar"] * {
    color: #c8d6f0 !important;
}
div[data-testid="stSidebar"] hr {
    border-color: rgba(100, 120, 255, 0.2) !important;
}
div[data-testid="stSidebar"] .stMetric {
    background: rgba(100, 120, 255, 0.1);
    border: 1px solid rgba(100, 120, 255, 0.2);
    border-radius: 10px;
    padding: 0.8rem 1rem;
}

/* ── Sidebar nav links ────────────────────────── */
div[data-testid="stSidebarNav"] a {
    color: #a0b4d0 !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stSidebarNav"] a:hover,
div[data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: rgba(100, 120, 255, 0.15) !important;
    color: #ffffff !important;
}

/* ── Main content area ────────────────────────── */
.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1400px !important;
}

/* ── Page Header Banner ───────────────────────── */
.scis-header {
    position: relative;
    padding: 2.5rem 2.5rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 2rem;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}
.scis-header::before {
    content: '';
    position: absolute;
    inset: 0;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}
.scis-header-content { position: relative; z-index: 1; }
.scis-header h1, .scis-header h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.5px;
}
.scis-header p {
    opacity: 0.85;
    font-weight: 300;
    margin: 0;
    font-size: 1.05rem;
}
.scis-header .header-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 0.25rem 0.9rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── Gradient variants for headers ───────────── */
.header-indigo  { background: linear-gradient(135deg, #1a1a6e 0%, #4f46e5 50%, #7c3aed 100%); }
.header-teal    { background: linear-gradient(135deg, #064e3b 0%, #059669 50%, #34d399 100%); }
.header-rose    { background: linear-gradient(135deg, #7f1d1d 0%, #dc2626 50%, #f472b6 100%); }
.header-amber   { background: linear-gradient(135deg, #78350f 0%, #d97706 50%, #fbbf24 100%); }
.header-cyan    { background: linear-gradient(135deg, #0c4a6e 0%, #0284c7 50%, #38bdf8 100%); }

/* ── Glassmorphism cards ──────────────────────── */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 1.6rem;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.glass-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
    border-color: rgba(100, 120, 255, 0.25);
}

/* ── Stat / Metric cards ──────────────────────── */
.stat-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.5rem 1rem;
    text-align: center;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.stat-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.stat-card-blue::after   { background: linear-gradient(90deg, #4f46e5, #7c3aed); }
.stat-card-green::after  { background: linear-gradient(90deg, #059669, #34d399); }
.stat-card-rose::after   { background: linear-gradient(90deg, #dc2626, #f472b6); }
.stat-card-amber::after  { background: linear-gradient(90deg, #d97706, #fbbf24); }
.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    border-color: rgba(100,120,255,0.2);
}
.stat-number {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a5b4fc, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.stat-label {
    font-size: 0.8rem;
    color: #94a3b8;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Feature cards ────────────────────────────── */
.feature-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 2rem 1.8rem;
    height: 100%;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.feature-card::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 120px; height: 120px;
    border-radius: 50%;
    opacity: 0.06;
    transition: opacity 0.3s ease;
}
.feature-card:hover { 
    transform: translateY(-4px);
    border-color: rgba(100,120,255,0.2);
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
}
.feature-card:hover::before { opacity: 0.12; }
.feature-card-1::before { background: #4f46e5; }
.feature-card-2::before { background: #059669; }
.feature-card-3::before { background: #dc2626; }
.feature-card-4::before { background: #d97706; }
.feature-icon {
    font-size: 2.2rem;
    margin-bottom: 1rem;
    display: block;
}
.feature-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.15rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 0.6rem;
}
.feature-desc {
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.65;
}

/* ── Tech badges ──────────────────────────────── */
.tech-badge {
    display: inline-block;
    background: rgba(79, 70, 229, 0.15);
    border: 1px solid rgba(79, 70, 229, 0.3);
    color: #a5b4fc;
    padding: 0.35rem 1rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 0.25rem;
    transition: all 0.2s ease;
}
.tech-badge:hover {
    background: rgba(79, 70, 229, 0.3);
    border-color: rgba(79, 70, 229, 0.6);
    color: #c7d2fe;
}

/* ── Section headings ─────────────────────────── */
.section-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.1rem;
    font-weight: 600;
    color: #cbd5e1;
    letter-spacing: 0.3px;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(100,120,255,0.3), transparent);
}

/* ── Info / success / risk boxes ──────────────── */
.info-box {
    background: rgba(79, 70, 229, 0.08);
    border: 1px solid rgba(79, 70, 229, 0.25);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    color: #c7d2fe;
    font-size: 0.9rem;
    line-height: 1.7;
}
.success-box {
    background: rgba(5, 150, 105, 0.1);
    border: 1px solid rgba(5, 150, 105, 0.3);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    color: #6ee7b7;
    font-size: 0.9rem;
    line-height: 1.7;
}
.risk-high {
    background: rgba(220, 38, 38, 0.08);
    border-left: 3px solid #ef4444;
    border-radius: 0 10px 10px 0;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.6rem;
    color: #fca5a5;
    font-size: 0.88rem;
    line-height: 1.6;
}
.risk-ok {
    background: rgba(5, 150, 105, 0.08);
    border-left: 3px solid #10b981;
    border-radius: 0 10px 10px 0;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.6rem;
    color: #6ee7b7;
    font-size: 0.88rem;
    line-height: 1.6;
}

/* ── Chat bubbles ─────────────────────────────── */
.chat-user {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 1rem 1.4rem;
    margin: 0.8rem 0 0.8rem 4rem;
    font-size: 0.92rem;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3);
}
.chat-ai {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px 18px 18px 4px;
    padding: 1.2rem 1.5rem;
    margin: 0.8rem 4rem 0.8rem 0;
    font-size: 0.92rem;
    line-height: 1.7;
    color: #cbd5e1;
}
.chat-empty {
    background: rgba(255,255,255,0.02);
    border: 2px dashed rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 3.5rem 2rem;
    text-align: center;
    color: #64748b;
    margin-top: 1rem;
}
.chat-empty .chat-empty-icon { font-size: 3rem; margin-bottom: 1rem; display: block; }

/* ── Example query buttons ────────────────────── */
.stButton > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #94a3b8 !important;
    border-radius: 10px !important;
    font-size: 0.83rem !important;
    transition: all 0.2s ease !important;
    text-align: left !important;
}
.stButton > button:hover {
    background: rgba(79, 70, 229, 0.12) !important;
    border-color: rgba(79, 70, 229, 0.35) !important;
    color: #a5b4fc !important;
    transform: translateX(2px);
}

/* ── Primary buttons ──────────────────────────── */
.stButton > button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    box-shadow: 0 4px 20px rgba(79, 70, 229, 0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 8px 30px rgba(79, 70, 229, 0.5) !important;
    transform: translateY(-1px);
}

/* ── Input fields ─────────────────────────────── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 0.9rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(79, 70, 229, 0.5) !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
}
.stTextInput label, .stSelectbox label, .stFileUploader label,
.stRadio label, .stTextArea label {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ── Chat input ───────────────────────────────── */
.stChatInput > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
}
.stChatInput input {
    color: #e2e8f0 !important;
}

/* ── Dataframes ───────────────────────────────── */
.stDataFrame {
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    overflow: hidden;
}
.stDataFrame table { background: transparent !important; }
.stDataFrame th {
    background: rgba(79, 70, 229, 0.12) !important;
    color: #a5b4fc !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.stDataFrame td { color: #94a3b8 !important; font-size: 0.88rem !important; }
.stDataFrame tr:hover td { background: rgba(255,255,255,0.03) !important; }

/* ── Alerts & info boxes ──────────────────────── */
.stAlert { border-radius: 12px !important; }
.stSuccess { 
    background: rgba(5,150,105,0.1) !important;
    border: 1px solid rgba(5,150,105,0.3) !important;
    color: #6ee7b7 !important;
}
.stInfo {
    background: rgba(79,70,229,0.08) !important;
    border: 1px solid rgba(79,70,229,0.25) !important;
    color: #a5b4fc !important;
}
.stWarning {
    background: rgba(217,119,6,0.1) !important;
    border: 1px solid rgba(217,119,6,0.3) !important;
}
.stError {
    background: rgba(220,38,38,0.1) !important;
    border: 1px solid rgba(220,38,38,0.3) !important;
}

/* ── Expanders ────────────────────────────────── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-top: none !important;
}

/* ── Divider ──────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.07) !important;
    margin: 1.5rem 0 !important;
}

/* ── Metrics ──────────────────────────────────── */
.stMetric { color: #e2e8f0 !important; }
.stMetric label { color: #64748b !important; font-size: 0.8rem !important; }
.stMetric .metric-container .metric-value { color: #a5b4fc !important; }

/* ── Spinner ──────────────────────────────────── */
.stSpinner > div { border-color: #4f46e5 !important; }

/* ── Scrollbar ────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb { background: rgba(100,120,255,0.25); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(100,120,255,0.4); }

/* ── Footer ───────────────────────────────────── */
.scis-footer {
    text-align: center;
    color: #475569;
    font-size: 0.78rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 2rem;
    letter-spacing: 0.3px;
}

/* ── Animated glow orbs (decorative) ─────────── */
.orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.06;
    pointer-events: none;
    z-index: 0;
}
.orb-1 {
    width: 400px; height: 400px;
    background: #4f46e5;
    top: -100px; right: -100px;
}
.orb-2 {
    width: 300px; height: 300px;
    background: #7c3aed;
    bottom: 100px; left: -80px;
}

/* ── Preview placeholder ──────────────────────── */
.photo-placeholder {
    background: rgba(255,255,255,0.02);
    border: 2px dashed rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 4rem 2rem;
    text-align: center;
    color: #475569;
    transition: border-color 0.2s;
}
.photo-placeholder:hover { border-color: rgba(79,70,229,0.25); }
.photo-placeholder .placeholder-icon { font-size: 3rem; margin-bottom: 1rem; display: block; }
</style>
"""

SIDEBAR_CSS = """
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
"""

def inject_css():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
