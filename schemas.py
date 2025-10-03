"""
Pydantic models for robot WebSocket communication.
"""
from typing import Optional
from pydantic import BaseModel, Field

class RobotMessage(BaseModel):
    """
    Incoming message from Raspberry Pi robot client.
    
    Example:
        {
            "text": "Hello robot!",
            "frame": "base64_encoded_jpeg_data",
            "status": "tracking person, distance=1.5"
        }
    """
    text: Optional[str] = None
    frame: Optional[str] = Field(None, description="Base64 encoded JPEG camera frame")
    status: Optional[str] = None

class ServerResponse(BaseModel):
    """
    Outgoing message to robot client.
    
    Example:
        {
            "speech": "Hello! I see that you're standing 1.5 meters away."
        }
    """
    speech: str = Field(..., description="Text for the robot to speak")

class ErrorResponse(BaseModel):
    """
    Error response for invalid messages.
    
    Example:
        {
            "error": "Invalid JSON format"
        }
    """
    error: str = Field(..., description="Error message describing what went wrong")