# Robot WebSocket Server

A FastAPI WebSocket server for interacting with Raspberry Pi robots. Supports face recognition, LLM-based conversation, and handles multiple robot clients simultaneously.

## Features

- WebSocket-based communication
- Face recognition using `face_recognition` library
- LLM integration (OpenAI API, with mock mode for testing)
- Async support for multiple robot clients
- Comprehensive test suite with mock clients

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. (Optional) Set up environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_api_key_here
   KNOWN_FACES_DIR=path/to/faces/directory
   ```

   If these are not set, the server will use mock responses.

## Usage

1. Start the server:
   ```bash
   python app.py
   ```
   Server runs on `ws://localhost:8000/ws/robot`

2. Run mock tests:
   ```bash
   pytest tests/test_mock_client.py -v
   ```

## API Reference

### Robot → Server Messages

```json
{
    "text": "Optional text from speech",
    "frame": "Optional base64 encoded JPEG frame",
    "status": "Optional robot status info"
}
```

### Server → Robot Responses

Success:
```json
{
    "speech": "Text for the robot to speak"
}
```

Error:
```json
{
    "error": "Error message"
}
```

## Project Structure

- `app.py` - FastAPI application and WebSocket endpoints
- `schemas.py` - Pydantic models for message validation
- `vision.py` - Face recognition functionality
- `llm.py` - LLM integration and response generation
- `tests/test_mock_client.py` - Mock client tests
