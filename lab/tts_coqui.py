from TTS.api import TTS
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTSEngine:
    def __init__(self):
        try:
            # Try simpler model first
            logger.info("Initializing TTS engine...")
            self.tts = TTS("tts_models/en/ljspeech/tacotron2-DDC", gpu=True)
            logger.info("TTS engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {str(e)}")
            raise
        
        # Create output directory
        os.makedirs("output", exist_ok=True)
    
    def speak(self, text: str, output_file: str = "output/speech.wav") -> tuple[bool, str]:
        """
        Generate speech from text
        
        Args:
            text: Text to convert to speech
            output_file: Path to save the audio file
            
        Returns:
            tuple: (success: bool, result: str)
                success: True if generation successful, False otherwise
                result: Path to audio file if successful, error message if failed
        """
        try:
            self.tts.tts_to_file(text=text, file_path=output_file)
            return True, output_file
        except Exception as e:
            error_msg = f"TTS generation failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

if __name__ == "__main__":
    # Test the implementation
    engine = TTSEngine()
    test_text = "Hello! This is a test of the text to speech engine."
    success, result = engine.speak(test_text)
    
    if success:
        logger.info(f"Audio saved to: {result}")
    else:
        logger.error(f"Error: {result}")



"""
# Add deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9 python3.9-venv python3.9-dev


# Create and activate virtual environment with Python 3.9
python3.9 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install TTS
"""
