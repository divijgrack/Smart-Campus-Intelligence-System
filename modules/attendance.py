"""
Smart Campus Intelligence System — Attendance Module
Processes camera frames to mark attendance and provides attendance stats.
"""
import pandas as pd
from datetime import datetime, date
from modules import database, face_engine


def process_frame_for_attendance(frame):
    """
    Process a camera frame: detect faces, recognize them, mark attendance.
    
    Args:
        frame: numpy.ndarray (BGR OpenCV image)
    
    Returns:
        list of dicts: [{'student_id', 'name', 'confidence', 'box', 'status'}, ...]
        where status is 'marked', 'already_marked', or 'unknown'
    """
    # Detect all faces in the frame
    detected_faces = face_engine.detect_faces_in_frame(frame)
    
    results = []
    
    for face_data in detected_faces:
        face_img = face_data["face_img"]
        box = face_data["box"]
        
        # Try to recognize this face
        match = face_engine.recognize_face(face_img)
        
        if match:
            student_id = match["student_id"]
            name = match["name"]
            confidence = match["confidence"]
            
            # Check if already marked today
            if database.is_already_marked_today(student_id):
                status = "already_marked"
            else:
                # Mark attendance
                database.log_attendance(student_id, name)
                status = "marked"
            
            results.append({
                "student_id": student_id,
                "name": name,
                "confidence": confidence,
                "box": box,
                "status": status
            })
        else:
            results.append({
                "student_id": None,
                "name": "Unknown",
                "confidence": 0,
                "box": box,
                "status": "unknown"
            })
    
    return results


def get_today_attendance_df():
    """Get today's attendance as a pandas DataFrame."""
    records = database.get_today_attendance()
    
    if not records['ids']:
        return pd.DataFrame(columns=["Student ID", "Name", "Time", "Status"])
    
    data = []
    for meta in records['metadatas']:
        data.append({
            "Student ID": meta.get("student_id", ""),
            "Name": meta.get("name", ""),
            "Time": meta.get("time", ""),
            "Status": meta.get("status", "present").title()
        })
    
    df = pd.DataFrame(data)
    # Remove duplicates, keep first occurrence
    df = df.drop_duplicates(subset=["Student ID"], keep="first")
    return df


def get_attendance_stats():
    """
    Compute attendance statistics for all students.
    
    Returns:
        dict: {
            'total_students': int,
            'present_today': int,
            'attendance_rate_today': float,
            'student_stats': DataFrame with per-student stats,
            'daily_summary': DataFrame with per-day summary
        }
    """
    all_students = database.get_all_students()
    total_students = len(all_students['ids'])
    
    today_records = database.get_today_attendance()
    today_unique = set()
    for meta in today_records.get('metadatas', []):
        today_unique.add(meta.get("student_id", ""))
    present_today = len(today_unique)
    
    attendance_rate = (present_today / total_students * 100) if total_students > 0 else 0
    
    # Per-student attendance stats
    all_records = database.get_all_attendance()
    
    student_attendance = {}
    all_dates = set()
    
    for meta in all_records.get('metadatas', []):
        sid = meta.get("student_id", "")
        d = meta.get("date", "")
        name = meta.get("name", "")
        
        if sid not in student_attendance:
            student_attendance[sid] = {"name": name, "dates_present": set()}
        student_attendance[sid]["dates_present"].add(d)
        all_dates.add(d)
    
    total_days = len(all_dates) if all_dates else 1
    
    student_stats_data = []
    for sid, info in student_attendance.items():
        days_present = len(info["dates_present"])
        percentage = round(days_present / total_days * 100, 1)
        student_stats_data.append({
            "Student ID": sid,
            "Name": info["name"],
            "Days Present": days_present,
            "Total Days": total_days,
            "Attendance %": percentage,
            "Status": "✅ Good" if percentage >= 75 else "⚠️ At Risk"
        })
    
    student_stats_df = pd.DataFrame(student_stats_data)
    
    # Daily summary
    daily_data = {}
    for meta in all_records.get('metadatas', []):
        d = meta.get("date", "")
        if d not in daily_data:
            daily_data[d] = set()
        daily_data[d].add(meta.get("student_id", ""))
    
    daily_summary_data = [
        {"Date": d, "Present": len(sids), "Total Enrolled": total_students}
        for d, sids in sorted(daily_data.items())
    ]
    daily_summary_df = pd.DataFrame(daily_summary_data) if daily_summary_data else pd.DataFrame()
    
    return {
        "total_students": total_students,
        "present_today": present_today,
        "attendance_rate_today": round(attendance_rate, 1),
        "student_stats": student_stats_df,
        "daily_summary": daily_summary_df
    }
