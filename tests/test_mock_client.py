"""
Mock client for testing the robot WebSocket server.
"""
import os
import json
import asyncio
import base64
from typing import Optional
import websockets
import pytest
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL", "ws://localhost:8000/ws/robot")

async def send_message(message: dict) -> dict:
    """Send a message to the server and return the response."""
    async with websockets.connect(SERVER_URL) as websocket:
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        return json.loads(response)

def create_mock_frame() -> str:
    """Create a mock base64 encoded JPEG frame."""
    # Create a 1x1 black pixel JPEG
    mock_jpeg = base64.b64encode(bytes([
        0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46,
        0x49, 0x46, 0x00, 0x01, 0x01, 0x01, 0x00, 0x48,
        0x00, 0x48, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43,
        0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xC0, 0x00, 0x0B, 0x08, 0x00, 0x01, 0x00,
        0x01, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4, 0x00,
        0x14, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x0A, 0xFF, 0xDA, 0x00, 0x08,
        0x01, 0x01, 0x00, 0x00, 0x3F, 0x00, 0x37, 0xFF,
        0xD9
    ])).decode()
    return mock_jpeg

@pytest.mark.asyncio
async def test_text_only_chat():
    """Test sending text-only message."""
    response = await send_message({"text": "Hello robot!"})
    assert "speech" in response
    print("\nTest 1 - Text only chat:")
    print(f"Response: {response['speech']}")

@pytest.mark.asyncio
async def test_text_with_status():
    """Test sending text with robot status."""
    response = await send_message({
        "text": "What are you doing?",
        "status": "tracking person, distance=1.8"
    })
    assert "speech" in response
    print("\nTest 2 - Text with status:")
    print(f"Response: {response['speech']}")

@pytest.mark.asyncio
async def test_frame_with_status():
    """Test sending frame with status."""
    response = await send_message({
        "frame": create_mock_frame(),
        "status": "tracking person, distance=1.5"
    })
    assert "speech" in response
    print("\nTest 3 - Frame with status:")
    print(f"Response: {response['speech']}")

@pytest.mark.asyncio
async def test_invalid_json():
    """Test sending invalid JSON."""
    async with websockets.connect(SERVER_URL) as websocket:
        await websocket.send("invalid json{")
        response = json.loads(await websocket.recv())
        assert "error" in response
        print("\nTest 4 - Invalid JSON:")
        print(f"Error: {response['error']}")

@pytest.mark.asyncio
async def test_multiple_clients():
    """Test multiple clients sending messages simultaneously."""
    async def client(num: int) -> None:
        response = await send_message({
            "text": f"Hello from client {num}",
            "status": f"client_{num}_status"
        })
        print(f"\nClient {num} response: {response['speech']}")
    
    await asyncio.gather(client(1), client(2))

@pytest.mark.asyncio
async def test_empty_message():
    """Test sending empty message."""
    response = await send_message({})
    assert "speech" in response
    print("\nTest 6 - Empty message:")
    print(f"Response: {response['speech']}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])