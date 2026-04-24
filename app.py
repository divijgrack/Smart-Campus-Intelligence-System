"""
🎓 Smart Campus Intelligence System
Main Streamlit Application — Landing Page & Navigation
"""
import streamlit as st
import config
from modules import database
from styles import inject_css

# ─── Page Configuration ─────────────────────────────────
st.set_page_config(
    page_title="Smart Campus Intelligence System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()

# ─── Sidebar ────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1rem 0;">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.3rem; font-weight:700;
                    background:linear-gradient(135deg,#a5b4fc,#7c3aed);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; margin-bottom:0.2rem;">
            🎓 SCIS
        </div>
        <div style="color:#64748b; font-size:0.75rem; font-weight:500; letter-spacing:0.5px;
                    text-transform:uppercase;">
            Smart Campus Intelligence System
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="color:#64748b; font-size:0.72rem; font-weight:600; text-transform:uppercase;
                letter-spacing:0.8px; margin-bottom:0.7rem;">Navigation</div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.87rem; line-height:2.0; color:#94a3b8;">
    📋 <strong style="color:#cbd5e1;">Enroll Student</strong> — Register new faces<br>
    📸 <strong style="color:#cbd5e1;">Mark Attendance</strong> — Live face recognition<br>
    🤖 <strong style="color:#cbd5e1;">AI Query</strong> — Ask anything about students<br>
    📊 <strong style="color:#cbd5e1;">Analytics</strong> — Stats & insights
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    try:
        students = database.get_all_students()
        total = len(students['ids'])
    except Exception:
        total = 0

    st.markdown(f"""
    <div style="background:rgba(79,70,229,0.1); border:1px solid rgba(79,70,229,0.2);
                border-radius:12px; padding:1rem; text-align:center; margin-bottom:1rem;">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:2rem; font-weight:700;
                    background:linear-gradient(135deg,#a5b4fc,#818cf8);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">{total}</div>
        <div style="color:#64748b; font-size:0.75rem; font-weight:500; text-transform:uppercase;
                    letter-spacing:0.5px;">Enrolled Students</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="color:#64748b; font-size:0.72rem; font-weight:600; text-transform:uppercase;
                letter-spacing:0.8px; margin-bottom:0.7rem;">Tech Stack</div>
    <div style="font-size:0.8rem; color:#475569; line-height:1.9;">
        🧠 DeepFace &nbsp;·&nbsp; 🗄️ ChromaDB<br>
        🤖 Gemini &nbsp;·&nbsp; ⛓️ LangChain<br>
        🐍 Python 3.11 &nbsp;·&nbsp; 📊 Plotly
    </div>
    """, unsafe_allow_html=True)

# ─── Main Content ────────────────────────────────────────

# Header
st.markdown("""
<div class="scis-header header-indigo">
    <div class="scis-header-content">
        <div class="header-badge">✦ Generative AI Project</div>
        <h1>🎓 Smart Campus Intelligence System</h1>
        <p>Face Recognition &nbsp;·&nbsp; Vector Database &nbsp;·&nbsp; AI-Powered Insights &nbsp;·&nbsp; Real-Time Analytics</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Quick Stats Row ─────────────────────────────────────
try:
    students = database.get_all_students()
    total_students = len(students['ids'])
    all_att = database.get_all_attendance()
    total_records = len(all_att['ids']) if all_att['ids'] else 0
    today_att = database.get_today_attendance()
    today_count = len(set(m.get("student_id", "") for m in today_att.get('metadatas', [])))
except Exception:
    total_students = total_records = today_count = 0

rate = round(today_count / total_students * 100, 1) if total_students > 0 else 0

col1, col2, col3, col4 = st.columns(4)
stats = [
    (col1, "stat-card-blue",  total_students, "Enrolled Students",  "👥"),
    (col2, "stat-card-green", today_count,    "Present Today",       "✅"),
    (col3, "stat-card-rose",  total_records,  "Total Records",       "📋"),
    (col4, "stat-card-amber", f"{rate}%",     "Today's Rate",        "📈"),
]
for col, cls, val, label, icon in stats:
    with col:
        st.markdown(f"""
        <div class="stat-card {cls}">
            <div style="font-size:1.6rem;margin-bottom:0.4rem;">{icon}</div>
            <div class="stat-number">{val}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Feature Cards ───────────────────────────────────────
st.markdown('<div class="section-title">🚀 System Features</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
features = [
    (col1, "feature-card-1", "👤", "Face Recognition Enrollment",
     "Convert student faces into <strong>512-dimensional vector embeddings</strong> using DeepFace (Facenet512). "
     "Stored securely in ChromaDB — no raw images needed for recognition. Just pure math."),
    (col2, "feature-card-2", "📸", "Real-Time Attendance Marking",
     "Live camera feed detects and recognizes faces in real-time using <strong>cosine similarity search</strong> "
     "against ChromaDB. Attendance marked automatically — no manual roll call required."),
]
for col, cls, icon, title, desc in features:
    with col:
        st.markdown(f"""
        <div class="feature-card {cls}">
            <span class="feature-icon">{icon}</span>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col3, col4 = st.columns(2)
features2 = [
    (col3, "feature-card-3", "🤖", "AI Query Engine (RAG)",
     "Teachers ask questions in plain English. <strong>LangChain</strong> retrieves data from ChromaDB, "
     "sends context to <strong>Google Gemini</strong>, and returns intelligent answers. "
     "\"Show me students at risk of failing\" → instant AI analysis."),
    (col4, "feature-card-4", "📊", "Analytics Dashboard",
     "Visual attendance analytics with <strong>Plotly</strong> charts. Student-wise breakdowns, "
     "department trends, at-risk alerts, and daily performance tracking — all in one beautiful dashboard."),
]
for col, cls, icon, title, desc in features2:
    with col:
        st.markdown(f"""
        <div class="feature-card {cls}">
            <span class="feature-icon">{icon}</span>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── How It Works ────────────────────────────────────────
st.markdown('<div class="section-title">🔧 How It Works</div>', unsafe_allow_html=True)
st.markdown("""
<div class="glass-card" style="padding:1.8rem 2rem;">
    <div style="font-size:0.95rem; color:#94a3b8; line-height:1.9;">
        <strong style="color:#a5b4fc;">The key insight:</strong> A face is never stored as a photo. 
        It's stored as <strong style="color:#c7d2fe;">512 numbers</strong> (a vector embedding).<br>
        When a new face walks in, the system asks 
        <em style="color:#c7d2fe;">"whose 512 numbers are closest to these 512 numbers?"</em><br>
        That's <strong style="color:#a5b4fc;">vector similarity search</strong> — the same core technology powering 
        both face recognition <em>and</em> the AI query engine.
    </div>
    <div style="display:flex; gap:0.8rem; margin-top:1.4rem; flex-wrap:wrap; align-items:center;">
        <div style="display:flex; align-items:center; gap:0.5rem; background:rgba(79,70,229,0.1);
                    border:1px solid rgba(79,70,229,0.2); border-radius:8px; padding:0.5rem 0.9rem;
                    font-size:0.8rem; color:#a5b4fc;">📷 Face Photo</div>
        <div style="color:#475569; font-size:1.2rem;">→</div>
        <div style="display:flex; align-items:center; gap:0.5rem; background:rgba(79,70,229,0.1);
                    border:1px solid rgba(79,70,229,0.2); border-radius:8px; padding:0.5rem 0.9rem;
                    font-size:0.8rem; color:#a5b4fc;">🧠 DeepFace</div>
        <div style="color:#475569; font-size:1.2rem;">→</div>
        <div style="display:flex; align-items:center; gap:0.5rem; background:rgba(79,70,229,0.1);
                    border:1px solid rgba(79,70,229,0.2); border-radius:8px; padding:0.5rem 0.9rem;
                    font-size:0.8rem; color:#a5b4fc;">🔢 512-dim Vector</div>
        <div style="color:#475569; font-size:1.2rem;">→</div>
        <div style="display:flex; align-items:center; gap:0.5rem; background:rgba(79,70,229,0.1);
                    border:1px solid rgba(79,70,229,0.2); border-radius:8px; padding:0.5rem 0.9rem;
                    font-size:0.8rem; color:#a5b4fc;">🗄️ ChromaDB</div>
        <div style="color:#475569; font-size:1.2rem;">→</div>
        <div style="display:flex; align-items:center; gap:0.5rem; background:rgba(5,150,105,0.12);
                    border:1px solid rgba(5,150,105,0.25); border-radius:8px; padding:0.5rem 0.9rem;
                    font-size:0.8rem; color:#6ee7b7;">✅ Instant Recognition</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tech Stack ──────────────────────────────────────────
st.markdown('<div class="section-title">🛠️ Technology Stack</div>', unsafe_allow_html=True)

techs = [
    ("Python 3.11", "Core Language"),
    ("DeepFace", "Face Embeddings"),
    ("ChromaDB", "Vector Database"),
    ("LangChain", "RAG Framework"),
    ("Google Gemini", "LLM"),
    ("Streamlit", "Web Dashboard"),
    ("OpenCV", "Camera/Vision"),
    ("Plotly", "Visualizations"),
]

tech_html = "".join(f'<span class="tech-badge">{name} <span style="opacity:0.5">·</span> {role}</span> ' for name, role in techs)
st.markdown(f'<div style="margin-top:0.3rem;">{tech_html}</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────
st.markdown("""
<div class="scis-footer">
    Smart Campus Intelligence System &nbsp;·&nbsp; Built with ❤️ using GenAI + Vector Database
</div>
""", unsafe_allow_html=True)
