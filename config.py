"""
Smart Campus Intelligence System — Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Paths ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")
STUDENT_PHOTOS_DIR = os.path.join(BASE_DIR, "data", "student_photos")

# Create directories if they don't exist
os.makedirs(CHROMA_DB_PATH, exist_ok=True)
os.makedirs(STUDENT_PHOTOS_DIR, exist_ok=True)

# ─── ChromaDB Collection Names ──────────────────────────
FACE_COLLECTION = "face_embeddings"
ATTENDANCE_COLLECTION = "attendance_records"
STUDENT_COLLECTION = "student_profiles"

# ─── Face Recognition Settings ─────────────────────────
FACE_MODEL = "Facenet512"          # Produces 512-dim embeddings
FACE_DETECTOR = "opencv"           # Fast and reliable detector
SIMILARITY_THRESHOLD = 0.65        # Cosine similarity threshold (lower = stricter)
FACE_DISTANCE_METRIC = "cosine"

# ─── Gemini API ─────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = "gemini-flash-lite-latest"    # Primary — most quota-friendly
GEMINI_FALLBACK_MODELS = [                   # Tried in order if primary is rate-limited
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest",
    "gemini-2.0-flash",
    "gemini-2.5-flash",
]

# ─── App Settings ───────────────────────────────────────
APP_TITLE = "🎓 Smart Campus Intelligence System"
APP_ICON = "🎓"
ATTENDANCE_COOLDOWN_SECONDS = 60   # Prevent duplicate attendance within 60s
