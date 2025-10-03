"""
FastAPI WebSocket server for robot interaction.
"""
import json
from typing import Dict
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from schemas import RobotMessage, ServerResponse, ErrorResponse
from vision import FaceRecognitionHelper
from llm import LLMHelper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Robot WebSocket Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize helpers
face_helper = FaceRecognitionHelper()
llm_helper = LLMHelper()

# Track connected clients
connected_clients: Dict[int, WebSocket] = {}
client_counter = 0

@app.websocket("/ws/robot")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for robot clients.
    
    Accepts JSON messages in the format:
    {
        "text": "Optional text from speech",
        "frame": "Optional base64 encoded JPEG frame",
        "status": "Optional robot status"
    }
    
    Responds with:
    {
        "speech": "Text for robot to speak"
    }
    """
    global client_counter
    client_id = client_counter
    client_counter += 1
    
    try:
        await websocket.accept()
        connected_clients[client_id] = websocket
        logger.info(f"Client {client_id} connected. Total clients: {len(connected_clients)}")
        
        while True:
            try:
                # Receive and parse message
                data = await websocket.receive_text()
                try:
                    message = RobotMessage.parse_raw(data)
                except Exception as e:
                    error_resp = ErrorResponse(error=f"Invalid message format: {str(e)}")
                    await websocket.send_text(error_resp.json())
                    continue
                
                # Process frame if present
                recognized_names = []
                if message.frame:
                    names, error = face_helper.process_frame(message.frame)
                    if error:
                        error_resp = ErrorResponse(error=error)
                        await websocket.send_text(error_resp.json())
                        continue
                    recognized_names = names
                
                # Generate response
                response_text = await llm_helper.generate_response(
                    message.text,
                    recognized_names,
                    message.status
                )
                
                # Send response
                response = ServerResponse(speech=response_text)
                await websocket.send_text(response.json())
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                error_resp = ErrorResponse(error=str(e))
                await websocket.send_text(error_resp.json())
                
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        if client_id in connected_clients:
            del connected_clients[client_id]
            logger.info(f"Client {client_id} disconnected. Remaining clients: {len(connected_clients)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)