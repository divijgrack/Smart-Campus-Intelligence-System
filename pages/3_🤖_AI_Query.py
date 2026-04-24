"""
🤖 AI Query — Smart Campus Intelligence System
Natural language query interface powered by RAG (LangChain + Gemini).
"""
import streamlit as st
from modules import rag_engine, database
import config
from styles import inject_css

st.set_page_config(page_title="AI Query | SCIS", page_icon="🤖", layout="wide")
inject_css()

# ─── Sidebar ────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1rem 0;">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.3rem; font-weight:700;
                    background:linear-gradient(135deg,#a5b4fc,#7c3aed);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">🎓 SCIS</div>
        <div style="color:#64748b; font-size:0.75rem; font-weight:500;
                    text-transform:uppercase; letter-spacing:0.5px;">AI Query Engine</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    <div style="color:#64748b; font-size:0.72rem; font-weight:600;
                text-transform:uppercase; letter-spacing:0.8px; margin-bottom:0.8rem;">
        💡 Example Queries
    </div>
    """, unsafe_allow_html=True)

    example_queries = [
        "📊 Show me all enrolled students",
        "⚠️ Which students have attendance below 75%?",
        "📋 Give me today's attendance summary",
        "📈 Show overall attendance statistics",
        "🔍 Who are the students at risk of failing?",
        "📅 How many students were present today?",
        "🏫 Show department-wise breakdown",
    ]

    for eq in example_queries:
        if st.button(eq, use_container_width=True, key=f"eq_{eq}"):
            st.session_state.selected_query = eq

    st.markdown("---")

    with st.expander("🔍 View Database Context"):
        st.markdown("<span style='color:#64748b; font-size:0.8rem;'>Data the AI has access to:</span>",
                    unsafe_allow_html=True)
        context = rag_engine.get_context_preview()
        st.code(context, language="text")

    st.markdown("---")
    st.markdown("""
    <div style="color:#64748b; font-size:0.72rem; font-weight:600;
                text-transform:uppercase; letter-spacing:0.8px; margin-bottom:0.6rem;">
        ⚙️ Configuration
    </div>
    """, unsafe_allow_html=True)

    if config.GOOGLE_API_KEY and config.GOOGLE_API_KEY != "your_gemini_api_key_here":
        st.markdown("""
        <div style="background:rgba(5,150,105,0.1); border:1px solid rgba(5,150,105,0.3);
                    border-radius:8px; padding:0.6rem 0.9rem; font-size:0.8rem; color:#6ee7b7;">
            ✅ Gemini API key configured
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(220,38,38,0.1); border:1px solid rgba(220,38,38,0.3);
                    border-radius:8px; padding:0.6rem 0.9rem; font-size:0.8rem; color:#fca5a5;">
            ❌ Gemini API key not set
        </div>
        """, unsafe_allow_html=True)
        st.code("GOOGLE_API_KEY=your_key", language="bash")

    st.markdown(f"""
    <div style="color:#475569; font-size:0.75rem; margin-top:0.5rem;">
        Model: <span style="color:#a5b4fc;">{config.GEMINI_MODEL}</span>
    </div>
    """, unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────
st.markdown("""
<div class="scis-header header-rose">
    <div class="scis-header-content">
        <div class="header-badge">🤖 RAG Engine</div>
        <h2>AI Query Engine</h2>
        <p>Ask anything about students and attendance in plain English — powered by LangChain + Gemini</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Initialize Chat ─────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ─── Chat Area ───────────────────────────────────────────
st.markdown('<div class="section-title">💬 Chat with AI</div>', unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-user">
            <span style="font-size:0.75rem; opacity:0.7; display:block; margin-bottom:0.3rem;">
                🧑‍🏫 You
            </span>
            {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-ai">
            <span style="font-size:0.75rem; color:#64748b; display:block; margin-bottom:0.5rem;
                         font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">
                🤖 AI Assistant
            </span>
        """, unsafe_allow_html=True)
        st.markdown(msg["content"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div style="height:0.3rem;"></div>', unsafe_allow_html=True)

# Handle example query
if "selected_query" in st.session_state and st.session_state.selected_query:
    query_text = st.session_state.selected_query
    st.session_state.selected_query = None

    st.session_state.chat_history.append({"role": "user", "content": query_text})
    with st.spinner("🤖 Thinking... (querying ChromaDB + Gemini)"):
        response = rag_engine.query(query_text)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.rerun()

# Empty state
if not st.session_state.chat_history:
    st.markdown("""
    <div class="chat-empty">
        <span class="chat-empty-icon">💬</span>
        <p style="color:#475569; font-weight:600; font-size:1rem; margin-bottom:0.4rem;">
            Ask me anything about your campus!
        </p>
        <p style="color:#374151; font-size:0.85rem;">
            Try: <em>"Show students with less than 75% attendance"</em><br>
            or click an example query from the sidebar →
        </p>
    </div>
    """, unsafe_allow_html=True)

# Chat input
user_query = st.chat_input("Ask about students, attendance, or any campus data...")

if user_query:
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.spinner("🤖 Thinking... (querying ChromaDB + Gemini)"):
        response = rag_engine.query(user_query)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.rerun()

# Clear chat
if st.session_state.chat_history:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown("""
<div class="scis-footer">Smart Campus Intelligence System · AI Query Engine · Powered by RAG + Gemini</div>
""", unsafe_allow_html=True)
