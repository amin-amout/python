"""
LLM interaction module for generating responses to robot messages.
"""
import os
from typing import Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

class LLMHelper:
    def __init__(self):
        """Initialize LLM helper with API configuration."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    async def generate_response(
        self, 
        text: Optional[str], 
        recognized_names: list[str], 
        status: Optional[str]
    ) -> str:
        """
        Generate a response using the LLM based on context.
        
        Args:
            text: Optional text message from robot
            recognized_names: List of names of recognized people
            status: Optional robot status message
            
        Returns:
            Generated response string
        """
        if not self.api_key:
            return self.mock_generate_response(text, recognized_names, status)

        try:
            # Build context-aware prompt
            context_parts = []
            
            if recognized_names:
                names_str = ", ".join(recognized_names)
                context_parts.append(f"You see: {names_str}")
                
            if status:
                context_parts.append(f"Robot status: {status}")
                
            if text:
                context_parts.append(f"Human said: {text}")
            
            prompt = (
                "You are a friendly robot assistant. "
                "Keep responses brief and natural. "
                f"Context: {' | '.join(context_parts)}\n"
                "Generate a short, friendly response:"
            )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": prompt},
                        ],
                        "max_tokens": 100
                    }
                )
                
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def mock_generate_response(
        self, 
        text: Optional[str], 
        recognized_names: list[str], 
        status: Optional[str]
    ) -> str:
        """
        Generate a mock response for testing without LLM API.
        
        Args:
            text: Optional text message from robot
            recognized_names: List of names of recognized people
            status: Optional robot status message
            
        Returns:
            Mock response string
        """
        if text and "hello" in text.lower():
            return "Hello! Nice to meet you!"
        elif recognized_names:
            return f"Hi {recognized_names[0]}! How are you today?"
        elif status and "tracking" in status.lower():
            return "I'm following along!"
        else:
            return "This is a mock response from the robot."