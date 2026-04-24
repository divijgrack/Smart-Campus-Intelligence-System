"""
📸 Mark Attendance — Smart Campus Intelligence System
Live face recognition to automatically mark attendance.
"""
import streamlit as st
import numpy as np
from PIL import Image
import cv2
from datetime import datetime
from modules import face_engine, database, attendance
import config
from styles import inject_css

st.set_page_config(page_title="Mark Attendance | SCIS", page_icon="📸", layout="wide")
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
                    text-transform:uppercase; letter-spacing:0.5px;">Mark Attendance</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.83rem; color:#64748b; line-height:2.1;">
        <strong style="color:#a5b4fc;">How to mark attendance:</strong><br>
        1️⃣ Turn on the webcam<br>
        2️⃣ Look into the camera<br>
        3️⃣ DeepFace extracts embedding<br>
        4️⃣ ChromaDB finds closest match<br>
        5️⃣ Auto-logs time if confidence > 65%
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    # Quick Stats
    try:
        today_att = database.get_today_attendance()
        today_count = len(set(m.get("student_id", "") for m in today_att.get('metadatas', [])))
    except Exception:
        today_count = 0

    st.markdown(f"""
    <div style="background:rgba(5,150,105,0.1); border:1px solid rgba(5,150,105,0.2);
                border-radius:12px; padding:1rem; text-align:center;">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:2rem; font-weight:700;
                    background:linear-gradient(135deg,#6ee7b7,#34d399);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">{today_count}</div>
        <div style="color:#64748b; font-size:0.75rem; font-weight:500; text-transform:uppercase;
                    letter-spacing:0.5px;">Present Today</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────
st.markdown("""
<div class="scis-header header-cyan">
    <div class="scis-header-content">
        <div class="header-badge">📸 Live Vision Module</div>
        <h2>Real-Time Attendance</h2>
        <p>Live camera feed detects faces and performs similarity search against the vector database</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Layout ──────────────────────────────────────────────
col_cam, col_log = st.columns([1.2, 1], gap="large")

with col_cam:
    st.markdown('<div class="section-title">📷 Live Camera Feed</div>', unsafe_allow_html=True)

    img_file_buffer = st.camera_input("Take a photo to mark attendance", label_visibility="collapsed")

    if img_file_buffer is not None:
        with st.spinner("🤖 Processing frame..."):
            image = Image.open(img_file_buffer)
            frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            success, results = attendance.process_frame_for_attendance(frame)

            if success:
                st.markdown("""
                <div class="success-box" style="margin-top:1rem;">
                    ✅ <strong>Faces processed successfully</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="risk-high" style="margin-top:1rem;">
                    <strong>❌ Could not process frame</strong><br>
                    <span style="font-size:0.8rem; opacity:0.8;">{results}</span>
                </div>
                """, unsafe_allow_html=True)

            # Display the processed frame (if bounding boxes were drawn)
            st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_container_width=True)

with col_log:
    st.markdown('<div class="section-title">📝 Today\'s Attendance Log</div>', unsafe_allow_html=True)

    try:
        today_records = database.get_today_attendance()

        if today_records['ids']:
            # Sort by time (newest first)
            records = []
            for i, _ in enumerate(today_records['ids']):
                meta = today_records['metadatas'][i]
                records.append({
                    "time": meta.get("time", ""),
                    "student_id": meta.get("student_id", "Unknown"),
                    "name": meta.get("name", "Unknown"),
                    "confidence": meta.get("confidence", 0)
                })

            records.sort(key=lambda x: x['time'], reverse=True)

            for rec in records:
                conf = rec['confidence']
                conf_color = "#10b981" if conf > 80 else "#f59e0b"

                st.markdown(f"""
                <div class="glass-card" style="padding:1rem 1.2rem; margin-bottom:0.8rem;
                                              border-left:4px solid {conf_color};">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <strong style="color:#e2e8f0; font-size:1.05rem;">{rec['name']}</strong><br>
                            <span style="color:#94a3b8; font-size:0.85rem; font-family:monospace;">
                                {rec['student_id']}
                            </span>
                        </div>
                        <div style="text-align:right;">
                            <div style="color:#a5b4fc; font-weight:600; font-size:0.95rem;">
                                {rec['time']}
                            </div>
                            <div style="color:{conf_color}; font-size:0.75rem; font-weight:600;">
                                {conf}% match
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="photo-placeholder" style="padding:3rem 1.5rem;">
                <span class="placeholder-icon">📭</span>
                <p style="color:#475569; font-size:0.9rem;">
                    No attendance marked today.<br>Capture a photo to log the first entry.
                </p>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Could not load attendance log: {e}")

st.markdown("""
<div class="scis-footer">Smart Campus Intelligence System · Mark Attendance Module</div>
""", unsafe_allow_html=True)
