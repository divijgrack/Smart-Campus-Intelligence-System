"""
Smart Campus Intelligence System — ChromaDB Vector Database Layer
Handles all interactions with ChromaDB: face embeddings, student profiles, attendance records.
"""
import chromadb
from chromadb.config import Settings
from datetime import datetime, date
import json
import config


def _get_client():
    """Get persistent ChromaDB client."""
    return chromadb.PersistentClient(path=config.CHROMA_DB_PATH)


def get_face_collection():
    """Get or create the face embeddings collection."""
    client = _get_client()
    return client.get_or_create_collection(
        name=config.FACE_COLLECTION,
        metadata={"hnsw:space": "cosine"}  # Use cosine similarity for face matching
    )


def get_attendance_collection():
    """Get or create the attendance records collection."""
    client = _get_client()
    return client.get_or_create_collection(
        name=config.ATTENDANCE_COLLECTION,
    )


def get_student_collection():
    """Get or create the student profiles collection."""
    client = _get_client()
    return client.get_or_create_collection(
        name=config.STUDENT_COLLECTION,
    )


# ─── Face Embeddings ────────────────────────────────────

def add_face_embedding(student_id: str, embedding: list, metadata: dict):
    """
    Store a face embedding vector in ChromaDB.
    
    Args:
        student_id: Unique student registration ID (e.g., GF202454238)
        embedding: 512-dimensional face vector from DeepFace
        metadata: Student info (name, email, department, enrolled_date)
    """
    collection = get_face_collection()
    
    # Check if student already enrolled
    existing = collection.get(ids=[student_id])
    if existing and existing['ids']:
        # Update existing embedding
        collection.update(
            ids=[student_id],
            embeddings=[embedding],
            metadatas=[metadata],
            documents=[json.dumps(metadata)]
        )
    else:
        collection.add(
            ids=[student_id],
            embeddings=[embedding],
            metadatas=[metadata],
            documents=[json.dumps(metadata)]
        )


def search_face(embedding: list, n_results: int = 1):
    """
    Search for the closest matching face in the database.
    
    Args:
        embedding: 512-dim face vector to search for
        n_results: Number of closest matches to return
        
    Returns:
        dict with 'ids', 'distances', 'metadatas' or None if no match
    """
    collection = get_face_collection()
    
    if collection.count() == 0:
        return None
    
    results = collection.query(
        query_embeddings=[embedding],
        n_results=min(n_results, collection.count())
    )
    
    return results


def get_all_students():
    """Get all enrolled students from the face collection."""
    collection = get_face_collection()
    if collection.count() == 0:
        return {"ids": [], "metadatas": [], "documents": []}
    return collection.get()


def delete_student(student_id: str):
    """Remove a student from the face collection."""
    collection = get_face_collection()
    collection.delete(ids=[student_id])
    
    # Also remove their attendance records
    att_collection = get_attendance_collection()
    try:
        results = att_collection.get(where={"student_id": student_id})
        if results and results['ids']:
            att_collection.delete(ids=results['ids'])
    except Exception:
        pass


# ─── Attendance Records ─────────────────────────────────

def log_attendance(student_id: str, name: str, timestamp: str = None, status: str = "present"):
    """
    Log an attendance record.
    
    Args:
        student_id: Student registration ID
        name: Student name
        timestamp: ISO format timestamp (auto-generated if None)
        status: 'present' or 'absent'
    """
    collection = get_attendance_collection()
    
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    today = date.today().isoformat()
    record_id = f"{student_id}_{today}_{timestamp.replace(':', '-')}"
    
    metadata = {
        "student_id": student_id,
        "name": name,
        "date": today,
        "time": datetime.now().strftime("%H:%M:%S") if timestamp is None else timestamp.split("T")[-1][:8],
        "status": status,
        "timestamp": timestamp
    }
    
    document = f"{name} ({student_id}) marked {status} on {today} at {metadata['time']}"
    
    collection.add(
        ids=[record_id],
        metadatas=[metadata],
        documents=[document]
    )


def get_today_attendance():
    """Get all attendance records for today."""
    collection = get_attendance_collection()
    
    if collection.count() == 0:
        return {"ids": [], "metadatas": [], "documents": []}
    
    today = date.today().isoformat()
    
    try:
        results = collection.get(
            where={"date": today}
        )
        return results
    except Exception:
        return {"ids": [], "metadatas": [], "documents": []}


def get_all_attendance():
    """Get all attendance records."""
    collection = get_attendance_collection()
    
    if collection.count() == 0:
        return {"ids": [], "metadatas": [], "documents": []}
    
    return collection.get()


def is_already_marked_today(student_id: str) -> bool:
    """Check if a student has already been marked present today."""
    collection = get_attendance_collection()
    
    if collection.count() == 0:
        return False
    
    today = date.today().isoformat()
    
    try:
        results = collection.get(
            where={
                "$and": [
                    {"student_id": student_id},
                    {"date": today}
                ]
            }
        )
        return len(results['ids']) > 0
    except Exception:
        return False
