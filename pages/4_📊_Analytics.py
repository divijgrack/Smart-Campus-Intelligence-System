"""
📊 Analytics — Smart Campus Intelligence System
Visual attendance analytics with Plotly charts.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from modules import attendance, database
from styles import inject_css

st.set_page_config(page_title="Analytics | SCIS", page_icon="📊", layout="wide")
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
                    text-transform:uppercase; letter-spacing:0.5px;">Analytics Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.83rem; color:#64748b; line-height:2.1;">
        📊 Student-wise attendance<br>
        🎯 Risk distribution pie chart<br>
        📅 Daily attendance trend<br>
        ⚠️ At-risk student alerts<br>
        📋 Full data export table
    </div>
    """, unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────
st.markdown("""
<div class="scis-header header-amber">
    <div class="scis-header-content">
        <div class="header-badge">📊 Analytics Module</div>
        <h2>Analytics Dashboard</h2>
        <p>Visual attendance analytics, student insights, and performance tracking</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Load Data ───────────────────────────────────────────
stats = attendance.get_attendance_stats()

# ─── Metric Cards ────────────────────────────────────────
st.markdown('<div class="section-title">📈 Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
absent = stats['total_students'] - stats['present_today']

metrics = [
    (col1, "stat-card-blue",  stats['total_students'],          "Total Enrolled",  "👥"),
    (col2, "stat-card-green", stats['present_today'],           "Present Today",   "✅"),
    (col3, "stat-card-rose",  absent,                           "Absent Today",    "❌"),
    (col4, "stat-card-amber", f"{stats['attendance_rate_today']}%", "Today's Rate","📈"),
]
for col, cls, val, label, icon in metrics:
    with col:
        st.markdown(f"""
        <div class="stat-card {cls}">
            <div style="font-size:1.5rem; margin-bottom:0.4rem;">{icon}</div>
            <div class="stat-number">{val}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Charts ──────────────────────────────────────────────
if not stats['student_stats'].empty:

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown('<div class="section-title">📊 Student-wise Attendance</div>', unsafe_allow_html=True)

        df = stats['student_stats'].sort_values("Attendance %", ascending=True)
        colors = ['#ef4444' if x < 75 else '#10b981' for x in df['Attendance %']]

        fig = go.Figure(go.Bar(
            x=df['Attendance %'],
            y=df['Name'],
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(width=0)
            ),
            text=df['Attendance %'].apply(lambda x: f'{x}%'),
            textposition='outside',
            textfont=dict(color='#94a3b8', size=11)
        ))

        fig.add_vline(
            x=75, line_dash="dash",
            line_color="rgba(239,68,68,0.5)",
            annotation_text="75% Threshold",
            annotation_font_color="#ef4444",
            annotation_font_size=11
        )

        fig.update_layout(
            height=max(300, len(df) * 52),
            xaxis_title="Attendance %",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="#94a3b8"),
            margin=dict(l=0, r=60, t=10, b=40),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                zerolinecolor='rgba(255,255,255,0.05)',
                tickfont=dict(color='#64748b')
            ),
            yaxis=dict(tickfont=dict(color='#94a3b8')),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-title">🎯 Attendance Distribution</div>', unsafe_allow_html=True)

        good = len(df[df['Attendance %'] >= 75])
        at_risk = len(df[df['Attendance %'] < 75])

        fig_pie = go.Figure(go.Pie(
            labels=['Good Standing (≥75%)', 'At Risk (<75%)'],
            values=[good, at_risk],
            marker=dict(
                colors=['#10b981', '#ef4444'],
                line=dict(color='#0a0a1a', width=2)
            ),
            hole=0.6,
            textinfo='label+value',
            textfont=dict(size=12, color='#cbd5e1'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
        ))

        fig_pie.add_annotation(
            text=f"<b>{good+at_risk}</b><br><span style='font-size:10px'>Students</span>",
            x=0.5, y=0.5,
            font=dict(size=16, color='#e2e8f0'),
            showarrow=False
        )

        fig_pie.update_layout(
            height=370,
            showlegend=True,
            legend=dict(
                font=dict(color='#94a3b8', size=11),
                bgcolor='rgba(0,0,0,0)'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter"),
            margin=dict(l=0, r=0, t=10, b=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ─── Daily Trend ─────────────────────────────────────
    if not stats['daily_summary'].empty:
        st.markdown('<div class="section-title">📅 Daily Attendance Trend</div>', unsafe_allow_html=True)

        daily_df = stats['daily_summary']

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=daily_df['Date'],
            y=daily_df['Present'],
            mode='lines+markers',
            name='Present',
            line=dict(color='#6366f1', width=3),
            marker=dict(size=7, color='#818cf8',
                        line=dict(color='#0a0a1a', width=2)),
            fill='tozeroy',
            fillcolor='rgba(99,102,241,0.07)',
            hovertemplate='<b>%{x}</b><br>Present: %{y}<extra></extra>'
        ))
        fig_trend.add_trace(go.Scatter(
            x=daily_df['Date'],
            y=daily_df['Total Enrolled'],
            mode='lines',
            name='Total Enrolled',
            line=dict(color='rgba(255,255,255,0.15)', width=2, dash='dot'),
            hovertemplate='<b>%{x}</b><br>Enrolled: %{y}<extra></extra>'
        ))

        fig_trend.update_layout(
            height=280,
            xaxis_title="Date",
            yaxis_title="Students",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="#94a3b8"),
            legend=dict(
                font=dict(color='#94a3b8', size=11),
                bgcolor='rgba(0,0,0,0)',
                orientation="h", y=1.1
            ),
            margin=dict(l=0, r=0, t=40, b=40),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.04)',
                tickfont=dict(color='#64748b')
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.04)',
                tickfont=dict(color='#64748b')
            ),
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    # ─── At-Risk / Good Standing ─────────────────────────
    st.markdown('<div class="section-title">⚠️ Student Status</div>', unsafe_allow_html=True)

    col_risk, col_good = st.columns(2, gap="large")

    with col_risk:
        st.markdown("""
        <div style="color:#ef4444; font-size:0.85rem; font-weight:600; margin-bottom:0.8rem;
                    text-transform:uppercase; letter-spacing:0.5px;">
            ❌ At-Risk Students (&lt; 75%)
        </div>
        """, unsafe_allow_html=True)
        at_risk_df = stats['student_stats'][stats['student_stats']['Attendance %'] < 75]

        if not at_risk_df.empty:
            for _, row in at_risk_df.iterrows():
                pct = row['Attendance %']
                bar_color = "#ef4444" if pct < 50 else "#f97316"
                st.markdown(f"""
                <div class="risk-high">
                    <strong>{row['Name']}</strong>
                    <span style="opacity:0.6; font-size:0.8rem;"> · {row['Student ID']}</span><br>
                    <div style="display:flex; align-items:center; gap:0.6rem; margin-top:0.4rem;">
                        <div style="flex:1; background:rgba(255,255,255,0.06);
                                    border-radius:4px; height:6px; overflow:hidden;">
                            <div style="width:{pct}%; background:{bar_color};
                                        height:100%; border-radius:4px;"></div>
                        </div>
                        <span style="font-weight:700; color:{bar_color};">{pct}%</span>
                    </div>
                    <span style="font-size:0.78rem; opacity:0.6;">
                        {row['Days Present']}/{row['Total Days']} days attended
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="success-box">
                🎉 <strong>All students above 75%!</strong><br>
                <span style="font-size:0.85rem; opacity:0.8;">No students are currently at risk.</span>
            </div>
            """, unsafe_allow_html=True)

    with col_good:
        st.markdown("""
        <div style="color:#10b981; font-size:0.85rem; font-weight:600; margin-bottom:0.8rem;
                    text-transform:uppercase; letter-spacing:0.5px;">
            ✅ Good Standing (≥ 75%)
        </div>
        """, unsafe_allow_html=True)
        good_df = stats['student_stats'][stats['student_stats']['Attendance %'] >= 75]

        if not good_df.empty:
            for _, row in good_df.iterrows():
                pct = row['Attendance %']
                st.markdown(f"""
                <div class="risk-ok">
                    <strong>{row['Name']}</strong>
                    <span style="opacity:0.6; font-size:0.8rem;"> · {row['Student ID']}</span><br>
                    <div style="display:flex; align-items:center; gap:0.6rem; margin-top:0.4rem;">
                        <div style="flex:1; background:rgba(255,255,255,0.06);
                                    border-radius:4px; height:6px; overflow:hidden;">
                            <div style="width:{pct}%; background:#10b981;
                                        height:100%; border-radius:4px;"></div>
                        </div>
                        <span style="font-weight:700; color:#10b981;">{pct}%</span>
                    </div>
                    <span style="font-size:0.78rem; opacity:0.6;">
                        {row['Days Present']}/{row['Total Days']} days attended
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No attendance records yet.")

    # ─── Full Data Table ──────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Complete Attendance Data</div>', unsafe_allow_html=True)
    st.dataframe(stats['student_stats'], use_container_width=True, hide_index=True)

else:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:4rem 2rem; margin-top:1rem;">
        <div style="font-size:3.5rem; margin-bottom:1rem;">📭</div>
        <h3 style="color:#475569; font-family:'Space Grotesk',sans-serif; margin-bottom:0.5rem;">
            No Attendance Data Yet
        </h3>
        <p style="color:#374151; font-size:0.9rem; line-height:1.8;">
            To see analytics:<br>
            1. Go to <strong style="color:#a5b4fc;">📋 Enroll Student</strong> and register some students<br>
            2. Go to <strong style="color:#a5b4fc;">📸 Mark Attendance</strong> and mark their attendance<br>
            3. Come back here to see the analytics!
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="scis-footer">Smart Campus Intelligence System · Analytics Dashboard · Powered by ChromaDB + Plotly</div>
""", unsafe_allow_html=True)
