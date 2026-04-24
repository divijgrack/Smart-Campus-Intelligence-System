"""
Smart Campus Intelligence System — Face Recognition Engine
Uses DeepFace to extract 512-dim face embeddings and perform face recognition.
"""
import os
import numpy as np
from PIL import Image
import cv2
from deepface import DeepFace
from datetime import datetime
import config
from modules import database


def get_face_embedding(image_input):
    """
    Extract a 512-dimensional face embedding from an image.
    
    Args:
        image_input: Can be:
            - str: Path to an image file
            - numpy.ndarray: OpenCV image (BGR format)
            - PIL.Image: Pillow image object
    
    Returns:
        list: 512-dimensional embedding vector, or None if no face detected
    """
    try:
        # Convert PIL Image to numpy array if needed
        if isinstance(image_input, Image.Image):
            image_input = np.array(image_input.convert("RGB"))
            image_input = cv2.cvtColor(image_input, cv2.COLOR_RGB2BGR)
        
        # Use DeepFace to extract embedding
        embeddings = DeepFace.represent(
            img_path=image_input,
            model_name=config.FACE_MODEL,
            detector_backend=config.FACE_DETECTOR,
            enforce_detection=True
        )
        
        if embeddings and len(embeddings) > 0:
            return embeddings[0]["embedding"]
        
        return None
        
    except Exception as e:
        print(f"[FaceEngine] Error extracting embedding: {e}")
        return None


def enroll_student(image_input, student_id: str, name: str, email: str = "", department: str = ""):
    """
    Enroll a new student — extract face embedding and store in ChromaDB.
    
    Args:
        image_input: Image (path, numpy array, or PIL Image)
        student_id: Unique registration ID (e.g., GF202454238)
        name: Full name
        email: Email address
        department: Department name
    
    Returns:
        tuple: (success: bool, message: str)
    """
    # Extract face embedding
    embedding = get_face_embedding(image_input)
    
    if embedding is None:
        return False, "❌ No face detected in the image. Please upload a clear photo with a visible face."
    
    # Save the photo locally
    photo_filename = f"{student_id}.jpg"
    photo_path = os.path.join(config.STUDENT_PHOTOS_DIR, photo_filename)
    
    try:
        if isinstance(image_input, str):
            img = Image.open(image_input)
        elif isinstance(image_input, np.ndarray):
            img = Image.fromarray(cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB))
        elif isinstance(image_input, Image.Image):
            img = image_input
        else:
            img = image_input
        
        img.save(photo_path, "JPEG", quality=90)
    except Exception as e:
        print(f"[FaceEngine] Warning: Could not save photo: {e}")
    
    # Prepare metadata
    metadata = {
        "name": name,
        "student_id": student_id,
        "email": email,
        "department": department,
        "enrolled_date": datetime.now().isoformat(),
        "photo_path": photo_path
    }
    
    # Store in ChromaDB
    database.add_face_embedding(student_id, embedding, metadata)
    
    return True, f"✅ {name} ({student_id}) enrolled successfully!"


def recognize_face(image_input):
    """
    Recognize a face against enrolled students in ChromaDB.
    
    Args:
        image_input: Image (path, numpy array, or PIL Image)
    
    Returns:
        dict or None: {
            'student_id': str,
            'name': str,
            'confidence': float (0-1, higher = better match),
            'metadata': dict
        }
        Returns None if no match found above threshold.
    """
    # Extract embedding from the input face
    embedding = get_face_embedding(image_input)
    
    if embedding is None:
        return None
    
    # Search ChromaDB for the closest match
    results = database.search_face(embedding, n_results=1)
    
    if results is None or not results['ids'][0]:
        return None
    
    # ChromaDB returns cosine distance (0 = identical, 2 = opposite)
    # Convert to similarity: similarity = 1 - distance
    distance = results['distances'][0][0]
    similarity = 1 - distance
    
    if similarity >= config.SIMILARITY_THRESHOLD:
        return {
            "student_id": results['ids'][0][0],
            "name": results['metadatas'][0][0].get("name", "Unknown"),
            "confidence": round(similarity * 100, 1),
            "metadata": results['metadatas'][0][0]
        }
    
    return None


def detect_faces_in_frame(frame):
    """
    Detect all faces in a video frame and return their bounding boxes.
    
    Args:
        frame: numpy.ndarray (BGR OpenCV image)
    
    Returns:
        list of dicts: [{'box': (x, y, w, h), 'face_img': numpy.ndarray}, ...]
    """
    try:
        faces = DeepFace.extract_faces(
            img_path=frame,
            detector_backend=config.FACE_DETECTOR,
            enforce_detection=False
        )
        
        results = []
        h, w = frame.shape[:2]
        
        for face in faces:
            if face["confidence"] > 0.5:
                region = face["facial_area"]
                x = max(0, region["x"])
                y = max(0, region["y"])
                fw = region["w"]
                fh = region["h"]
                
                # Extract face region from original frame
                face_img = frame[y:y+fh, x:x+fw]
                
                if face_img.size > 0:
                    results.append({
                        "box": (x, y, fw, fh),
                        "face_img": face_img
                    })
        
        return results
        
    except Exception as e:
        print(f"[FaceEngine] Error detecting faces: {e}")
        return []
