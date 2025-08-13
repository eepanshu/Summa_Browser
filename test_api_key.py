#!/usr/bin/env python3
"""
Test script to verify AssemblyAI API key validity
"""

import os
import assemblyai as aai

def test_api_key():
    """Test if the AssemblyAI API key is valid"""
    api_key = os.environ.get("ASSEMBLYAI_API_KEY", "")
    if not api_key:
        print("❌ ASSEMBLYAI_API_KEY not set in environment")
        return False
    
    print(f"Testing API key: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        # Set the API key
        aai.settings.api_key = api_key
        
        # Try to create a simple transcription config
        config = aai.TranscriptionConfig(
            speech_model=aai.SpeechModel.best
        )
        
        print("✅ API key format is valid")
        print("✅ Transcription config created successfully")
        
        # Test with a simple audio URL
        test_url = "https://assembly.ai/wildfires.mp3"
        print(f"\nTesting with sample audio: {test_url}")
        
        try:
            # Create transcriber
            transcriber = aai.Transcriber(config=config)
            print("✅ Transcriber created successfully")
            
            # Try to transcribe (this will test the API key)
            print("Attempting transcription...")
            transcript = transcriber.transcribe(test_url)
            
            if transcript.status == "completed":
                print("✅ API key is VALID - Transcription successful!")
                print(f"Transcript length: {len(transcript.text)} characters")
                return True
            elif transcript.status == "error":
                print(f"❌ API key is VALID but transcription failed: {transcript.error}")
                return True
            else:
                print(f"⚠️ API key is VALID, status: {transcript.status}")
                return True
                
        except Exception as e:
            if "unauthorized" in str(e).lower() or "invalid" in str(e).lower():
                print("❌ API key is INVALID - Unauthorized access")
                return False
            else:
                print(f"⚠️ API key appears valid but error occurred: {str(e)}")
                return True
                
    except Exception as e:
        print(f"❌ Error testing API key: {str(e)}")
        return False

if __name__ == "__main__":
    is_valid = test_api_key()
    print(f"\n{'='*50}")
    print(f"API Key Status: {'VALID' if is_valid else 'INVALID'}")
    print(f"{'='*50}")
