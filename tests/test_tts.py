import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tts_service import TTSService, TTSServiceException

def test_tts_service():
    print("Initializing TTSService...")
    service = TTSService()

    # Test cases for each language
    test_cases = [
        {"text": "Hello, this is a test of AgriVision AI crop disease diagnosis.", "lang": "en"},
        {"text": "नमस्ते, यह एग्रीविज़न एआई फसल रोग निदान का परीक्षण है।", "lang": "hi"},
        {"text": "नमस्कार, ही अॅग्रीव्हिजन एआय पीक रोग निदानाची चाचणी आहे.", "lang": "mr"}
    ]

    generated_files = []

    try:
        for case in test_cases:
            print(f"Generating audio for language: {case['lang']}...")
            audio_path = service.generate_audio(case["text"], language=case["lang"])
            
            # Assert file exists and is not empty
            assert audio_path is not None
            assert os.path.exists(audio_path)
            assert os.path.getsize(audio_path) > 0
            print(f"Success! File created at: {audio_path} (Size: {os.path.getsize(audio_path)} bytes)")
            
            generated_files.append(audio_path)

        # Test validation for empty text
        print("Testing validation: empty text...")
        try:
            service.generate_audio("", language="en")
            assert False, "Should raise TTSServiceException for empty text"
        except TTSServiceException as e:
            print(f"Successfully caught expected exception: {e}")

        # Test validation for unsupported language
        print("Testing validation: unsupported language...")
        try:
            service.generate_audio("Hello", language="es-MX")
            assert False, "Should raise TTSServiceException for unsupported language"
        except TTSServiceException as e:
            print(f"Successfully caught expected exception: {e}")

    finally:
        # Cleanup files
        print("Cleaning up generated test files...")
        for path in generated_files:
            if os.path.exists(path):
                service.cleanup_file(path)
                assert not os.path.exists(path), f"Failed to delete {path}"
        print("Cleanup completed successfully!")

if __name__ == "__main__":
    test_tts_service()
    print("All TTS tests passed successfully!")
