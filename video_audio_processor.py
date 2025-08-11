# Video Summarization Enhancement for SummaBrowser
# Option 2: Audio Extraction + Speech Recognition

import os
import requests
import tempfile
from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_path):
    """Extract audio from video file"""
    try:
        # Load video and extract audio
        video = VideoFileClip(video_path)
        
        # Create temporary audio file
        audio_path = tempfile.mktemp(suffix='.wav')
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        video.close()
        return audio_path
        
    except Exception as e:
        return None, f"Audio extraction failed: {str(e)}"

def transcribe_audio_with_whisper_api(audio_path):
    """Use OpenAI Whisper API for transcription"""
    try:
        # This would use OpenAI's Whisper API
        # You'd need an OpenAI API key
        
        with open(audio_path, 'rb') as audio_file:
            files = {'file': audio_file}
            data = {
                'model': 'whisper-1',
                'language': 'en'
            }
            headers = {
                'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}'
            }
            
            response = requests.post(
                'https://api.openai.com/v1/audio/transcriptions',
                files=files,
                data=data,
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()['text']
            else:
                return None, f"Transcription failed: {response.text}"
                
    except Exception as e:
        return None, f"Transcription error: {str(e)}"

def process_video_file(video_path):
    """Process uploaded video file"""
    try:
        # Extract audio
        audio_path = extract_audio_from_video(video_path)
        if not audio_path:
            return {'success': False, 'error': 'Audio extraction failed'}
        
        # Transcribe audio
        transcript = transcribe_audio_with_whisper_api(audio_path)
        
        # Clean up audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        if transcript:
            # Generate summary
            summary = advanced_summarize(transcript)
            
            return {
                'success': True,
                'transcript': transcript,
                'summary': summary,
                'type': 'video_file'
            }
        else:
            return {'success': False, 'error': 'Transcription failed'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

# New requirements:
# moviepy
# openai (for Whisper API)
# or speech_recognition (for free alternatives)
