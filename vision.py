"""
Face recognition helpers for processing robot camera frames.
Mock version for development and testing.
"""
import os
import base64
from typing import List, Optional, Tuple
from io import BytesIO

try:
    import face_recognition
    from PIL import Image
    import numpy as np
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False

class FaceRecognitionHelper:
    def __init__(self):
        """Initialize with empty known faces. Load from directory if available."""
        self.known_faces = []
        self.known_names = []
        self.using_mock = not FACE_RECOGNITION_AVAILABLE
        
        if not self.using_mock:
            # Try to load known faces from a directory
            faces_dir = os.getenv("KNOWN_FACES_DIR")
            if faces_dir and os.path.exists(faces_dir):
                self._load_known_faces(faces_dir)

    def _load_known_faces(self, directory: str) -> None:
        """Load known faces from image files in directory."""
        for filename in os.listdir(directory):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(directory, filename)
                
                image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(image)
                
                if face_encoding:
                    self.known_faces.append(face_encoding[0])
                    self.known_names.append(name)

    def process_frame(self, frame_data: str) -> Tuple[List[str], Optional[str]]:
        """
        Process a base64 encoded camera frame to detect and recognize faces.
        Falls back to mock mode if face_recognition is not available.
        
        Args:
            frame_data: Base64 encoded JPEG image
            
        Returns:
            Tuple of (list of recognized names, error message if any)
        """
        if self.using_mock:
            return self.mock_process_frame(frame_data)
            
        try:
            # Decode base64 frame
            image_bytes = base64.b64decode(frame_data)
            image = Image.open(BytesIO(image_bytes))
            
            # Convert to numpy array for face_recognition
            image_array = np.array(image)
            
            # Find faces in frame
            face_locations = face_recognition.face_locations(image_array)
            face_encodings = face_recognition.face_encodings(image_array, face_locations)
            
            recognized_names = []
            
            # Compare with known faces
            for face_encoding in face_encodings:
                if not self.known_faces:  # No known faces to compare against
                    return ["unknown person"], None
                    
                matches = face_recognition.compare_faces(self.known_faces, face_encoding)
                if True in matches:
                    matched_indexes = [i for i, match in enumerate(matches) if match]
                    recognized_names.append(self.known_names[matched_indexes[0]])
                else:
                    recognized_names.append("unknown person")
                    
            return recognized_names, None
            
        except Exception as e:
            return [], f"Error processing frame: {str(e)}"

    def mock_process_frame(self, frame_data: str) -> Tuple[List[str], Optional[str]]:
        """
        Mock version of process_frame for testing without face recognition.
        
        Args:
            frame_data: Base64 encoded JPEG image (ignored in mock)
            
        Returns:
            Tuple of (list of mock recognized names, None for no error)
        """
        return ["Mock Person"], None