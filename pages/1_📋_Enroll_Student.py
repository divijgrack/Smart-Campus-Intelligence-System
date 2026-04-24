"""
📋 Enroll Student — Smart Campus Intelligence System
Register new students by capturing/uploading their face photo.
"""
import streamlit as st
from PIL import Image
from modules import face_engine, database
import config
from styles import inject_css

st.set_page_config(page_title="Enroll Student | SCIS", page_icon="📋", layout="wide")
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
                    text-transform:uppercase; letter-spacing:0.5px;">Enroll Student</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.83rem; color:#64748b; line-height:2.1;">
        <strong style="color:#a5b4fc;">How enrollment works:</strong><br>
        1️⃣ Fill in student details<br>
        2️⃣ Upload or capture photo<br>
        3️⃣ DeepFace extracts 512-dim vector<br>
        4️⃣ Stored in ChromaDB forever
    </div>
    """, unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────
st.markdown("""
<div class="scis-header header-teal">
    <div class="scis-header-content">
        <div class="header-badge">📋 Registration Module</div>
        <h2>Enroll New Student</h2>
        <p>Capture a face photo and register a new student in the vector database</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Enrollment Form ─────────────────────────────────────
col_form, col_preview = st.columns([1, 1], gap="large")

with col_form:
    st.markdown('<div class="section-title">📝 Student Details</div>', unsafe_allow_html=True)

    student_id = st.text_input(
        "Registration ID *",
        placeholder="e.g., GF202454238",
        help="Unique registration/roll number"
    )
    name = st.text_input(
        "Full Name *",
        placeholder="e.g., Divij Sharma",
        help="Student's full name"
    )
    email = st.text_input(
        "Email Address",
        placeholder="e.g., divij@college.edu",
        help="Optional email address"
    )
    department = st.selectbox(
        "Department",
        ["Computer Science", "Information Technology", "Electronics",
         "Mechanical", "Civil", "Electrical", "Other"]
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📷 Face Photo</div>', unsafe_allow_html=True)

    upload_method = st.radio(
        "Input method:",
        ["📁 Upload Photo", "📷 Capture from Webcam"],
        horizontal=True
    )

    uploaded_image = None
    if upload_method == "📁 Upload Photo":
        uploaded_file = st.file_uploader(
            "Upload a clear face photo",
            type=["jpg", "jpeg", "png"],
            help="Well-lit photo showing the student's face clearly"
        )
        if uploaded_file is not None:
            uploaded_image = Image.open(uploaded_file)
    else:
        camera_image = st.camera_input("Take a photo")
        if camera_image is not None:
            uploaded_image = Image.open(camera_image)

with col_preview:
    st.markdown('<div class="section-title">👀 Preview & Summary</div>', unsafe_allow_html=True)

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Photo", use_container_width=True)
        st.markdown(f"""
        <div class="info-box" style="margin-top:1rem;">
            <strong>📋 Ready to enroll:</strong><br><br>
            👤 &nbsp;Name: <strong style="color:#c7d2fe;">{name or '—'}</strong><br>
            🆔 &nbsp;ID: <strong style="color:#c7d2fe;">{student_id or '—'}</strong><br>
            🏛️ &nbsp;Department: <strong style="color:#c7d2fe;">{department}</strong><br>
            📐 &nbsp;Image: <strong style="color:#c7d2fe;">{uploaded_image.size[0]}×{uploaded_image.size[1]} px</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="photo-placeholder">
            <span class="placeholder-icon">📷</span>
            <p style="color:#475569; font-size:0.9rem;">Upload or capture a photo<br>to see the preview here</p>
        </div>
        """, unsafe_allow_html=True)

# ─── Enroll Button ───────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Enroll Student", type="primary", use_container_width=True):
    if not student_id:
        st.error("❌ Please enter a Registration ID.")
    elif not name:
        st.error("❌ Please enter the student's Full Name.")
    elif uploaded_image is None:
        st.error("❌ Please upload or capture a face photo.")
    else:
        with st.spinner("🔄 Extracting face embedding and enrolling..."):
            success, message = face_engine.enroll_student(
                image_input=uploaded_image,
                student_id=student_id.strip(),
                name=name.strip(),
                email=email.strip(),
                department=department
            )

        if success:
            st.success(message)
            st.balloons()
            st.markdown(f"""
            <div class="success-box" style="margin-top:1rem;">
                <strong>✅ Enrollment Complete!</strong><br><br>
                <strong style="color:#a7f3d0;">{name}</strong> has been enrolled with ID
                <strong style="color:#a7f3d0;">{student_id}</strong>.<br>
                Their face has been converted to a <strong>512-dimensional vector</strong>
                and stored in <strong>ChromaDB</strong>.<br><br>
                🔒 <em>Note: Only the vector embedding is used for recognition —
                no raw face image is stored.</em>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(message)

# ─── Enrolled Students Table ─────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">📚 Currently Enrolled Students</div>', unsafe_allow_html=True)

try:
    students = database.get_all_students()
    if students['ids']:
        student_data = []
        for i, sid in enumerate(students['ids']):
            meta = students['metadatas'][i] if i < len(students['metadatas']) else {}
            student_data.append({
                "Registration ID": sid,
                "Name": meta.get("name", "Unknown"),
                "Email": meta.get("email", "N/A"),
                "Department": meta.get("department", "N/A"),
                "Enrolled": meta.get("enrolled_date", "N/A")[:10]
            })

        st.dataframe(student_data, use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div style="text-align:right; color:#64748b; font-size:0.8rem; margin-top:0.5rem;">
            Total: <strong style="color:#a5b4fc;">{len(students['ids'])}</strong> students enrolled
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🗑️ Remove a Student"):
            del_id = st.selectbox("Select student to remove:", students['ids'])
            if st.button("Remove Student", type="secondary"):
                database.delete_student(del_id)
                st.success(f"Removed student {del_id}")
                st.rerun()
    else:
        st.info("No students enrolled yet. Use the form above to enroll the first student!")

except Exception as e:
    st.warning(f"Could not load student list: {e}")

# Footer
st.markdown("""
<div class="scis-footer">Smart Campus Intelligence System · Enroll Student Module</div>
""", unsafe_allow_html=True)
