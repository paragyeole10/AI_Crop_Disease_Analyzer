import os
import tempfile
import logging
from typing import Dict
from gtts import gTTS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agrivision-tts")

class TTSServiceException(Exception):
    """Base exception for TTS Service errors."""
    pass

class TTSService:
    """
    A production-ready Text-to-Speech (TTS) service using gTTS (Google Text-to-Speech).
    Designed to be modular and reusable in other architectures like FastAPI.
    """
    
    # Supported languages mapped to their ISO-639-1 language codes
    SUPPORTED_LANGUAGES: Dict[str, str] = {
        "en": "English",
        "hi": "Hindi",
        "mr": "Marathi"
    }

    def __init__(self, temp_dir: str = None):
        """
        Initialize the TTS Service.
        
        Parameters:
        - temp_dir: Optional directory path to store temporary audio files.
                    If not specified, uses the system default temp directory.
        """
        self.temp_dir = temp_dir
        if self.temp_dir:
            os.makedirs(self.temp_dir, exist_ok=True)
            logger.info(f"TTSService initialized with custom temp directory: {self.temp_dir}")
        else:
            logger.info("TTSService initialized with default system temp directory.")

    def generate_audio(self, text: str, language: str = "en") -> str:
        """
        Generate a playable speech MP3 file from text using gTTS.
        
        Parameters:
        - text: The input string to convert to speech. Cannot be empty.
        - language: Language code (options: 'en', 'hi', 'mr'). Defaults to 'en'.
        
        Returns:
        - path_to_audio_file: Absolute file system path to the generated MP3 audio file.
        
        Raises:
        - TTSServiceException: If audio generation fails due to missing arguments,
                               unsupported languages, network issues, or internal errors.
        """
        # 1. Validation Checks
        if not text or not text.strip():
            logger.error("TTS failed: Input text is empty.")
            raise TTSServiceException("Input text to generate speech cannot be empty.")
            
        language_lower = language.strip().lower()
        if language_lower not in self.SUPPORTED_LANGUAGES:
            logger.error(f"TTS failed: Unsupported language code '{language}'.")
            raise TTSServiceException(
                f"Unsupported language code '{language}'. "
                f"Supported options are: {list(self.SUPPORTED_LANGUAGES.keys())}."
            )

        logger.info(f"Generating audio for text (length: {len(text)}) in language: {self.SUPPORTED_LANGUAGES[language_lower]}")

        # 2. Audio Generation
        try:
            # Create a temporary file with a persistent path that won't be deleted immediately
            # delete=False allows Streamlit or external services to read the file after this method returns
            temp_file = tempfile.NamedTemporaryFile(
                dir=self.temp_dir,
                suffix=".mp3",
                delete=False
            )
            temp_file_path = temp_file.name
            temp_file.close() # Close handle so gtts can write to it on Windows systems

            # Initialize gTTS
            tts = gTTS(text=text, lang=language_lower, slow=False)
            
            # Write audio payload to the file
            tts.save(temp_file_path)
            
            logger.info(f"Audio file created successfully at: {temp_file_path}")
            return temp_file_path

        except Exception as e:
            # Clean up the empty temp file if it was created and exists on error
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception:
                    pass
            
            # Catch network connection or API resolution errors specifically
            err_msg = str(e).lower()
            if "connection" in err_msg or "http" in err_msg or "gtts" in err_msg or "socket" in err_msg or "dns" in err_msg:
                logger.error(f"TTS network error: {e}")
                raise TTSServiceException(
                    "Failed to generate speech. Please check your internet connection and try again."
                ) from e
            else:
                logger.error(f"TTS internal error: {e}")
                raise TTSServiceException(f"Failed to generate speech: {str(e)}") from e

    def cleanup_file(self, file_path: str) -> bool:
        """
        Helper method to manually delete a generated temporary audio file.
        
        Parameters:
        - file_path: Path of the file to remove.
        
        Returns:
        - True if deletion was successful, False otherwise.
        """
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary audio file: {file_path}")
                return True
        except Exception as e:
            logger.warning(f"Failed to delete temp file {file_path}: {e}")
        return False
