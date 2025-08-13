#!/usr/bin/env python3
"""
Test script for video processing functionality
"""

from video_integration import process_video_request, video_processor

def test_video_integration():
    """Test the complete video integration"""
    print("Testing Video Integration...")
    
    # Test YouTube transcript first
    print("\n1. Testing YouTube transcript...")
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        result = process_video_request(youtube_url)
        print(f"YouTube result: {result}")
        
        if result.get('success'):
            print("✅ YouTube processing successful!")
        else:
            print(f"❌ YouTube failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ YouTube test error: {str(e)}")
    
    # Test AssemblyAI fallback
    print("\n2. Testing AssemblyAI fallback...")
    try:
        # Test with a direct audio URL
        audio_url = "https://assembly.ai/wildfires.mp3"
        result = video_processor.transcribe_with_assemblyai(audio_url)
        print(f"AssemblyAI result: {result}")
        
        if result and isinstance(result, dict) and result.get('success'):
            print("✅ AssemblyAI processing successful!")
        else:
            print(f"❌ AssemblyAI failed: {result}")
            
    except Exception as e:
        print(f"❌ AssemblyAI test error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_video_integration()
