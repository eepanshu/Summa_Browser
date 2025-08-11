# Video Summarization Enhancement for SummaBrowser
# Option 3: Web-based services with free tiers

import requests
import json
import time

def get_video_transcript_assemblyai(video_url, api_key):
    """Use AssemblyAI (has free tier) for video transcription"""
    try:
        # Step 1: Upload video URL to AssemblyAI
        headers = {
            'authorization': api_key,
            'content-type': 'application/json'
        }
        
        data = {
            'audio_url': video_url,
            'auto_highlights': True,
            'summary': True,
            'summary_model': 'informative',
            'summary_type': 'bullets'
        }
        
        # Submit for transcription
        response = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            json=data,
            headers=headers
        )
        
        if response.status_code != 200:
            return None, f"Failed to submit video: {response.text}"
        
        transcript_id = response.json()['id']
        
        # Step 2: Poll for completion
        while True:
            response = requests.get(
                f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
                headers=headers
            )
            
            result = response.json()
            
            if result['status'] == 'completed':
                return {
                    'transcript': result['text'],
                    'summary': result.get('summary', ''),
                    'highlights': result.get('auto_highlights_result', {}).get('results', [])
                }
            elif result['status'] == 'error':
                return None, f"Transcription failed: {result['error']}"
            
            time.sleep(5)  # Wait 5 seconds before checking again
            
    except Exception as e:
        return None, f"AssemblyAI error: {str(e)}"

def transcribe_with_deepgram(video_url, api_key):
    """Use Deepgram (has free tier) for video transcription"""
    try:
        headers = {
            'Authorization': f'Token {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'url': video_url
        }
        
        params = {
            'model': 'nova-2',
            'smart_format': 'true',
            'summarize': 'v2',
            'detect_topics': 'true'
        }
        
        response = requests.post(
            'https://api.deepgram.com/v1/listen',
            headers=headers,
            json=data,
            params=params
        )
        
        if response.status_code == 200:
            result = response.json()
            transcript = result['results']['channels'][0]['alternatives'][0]['transcript']
            summary = result['results'].get('summary', {}).get('short', '')
            
            return {
                'transcript': transcript,
                'summary': summary,
                'service': 'deepgram'
            }
        else:
            return None, f"Deepgram error: {response.text}"
            
    except Exception as e:
        return None, f"Deepgram error: {str(e)}"

def extract_video_info(video_url):
    """Extract video information for processing"""
    if 'youtube.com' in video_url or 'youtu.be' in video_url:
        return {'type': 'youtube', 'url': video_url}
    elif video_url.startswith(('http://', 'https://')):
        return {'type': 'web_video', 'url': video_url}
    else:
        return {'type': 'unknown', 'url': video_url}

def process_video_with_free_services(video_url):
    """Process video using free web services"""
    try:
        video_info = extract_video_info(video_url)
        
        # Try AssemblyAI first (has generous free tier)
        assemblyai_key = os.environ.get('ASSEMBLYAI_API_KEY')
        if assemblyai_key:
            result = get_video_transcript_assemblyai(video_url, assemblyai_key)
            if result:
                return {
                    'success': True,
                    'data': result,
                    'service': 'assemblyai'
                }
        
        # Fallback to Deepgram
        deepgram_key = os.environ.get('DEEPGRAM_API_KEY')
        if deepgram_key:
            result = transcribe_with_deepgram(video_url, deepgram_key)
            if result:
                return {
                    'success': True,
                    'data': result,
                    'service': 'deepgram'
                }
        
        return {
            'success': False,
            'error': 'No valid API keys found for video transcription services'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Video processing failed: {str(e)}'
        }

# Free tier limits:
# AssemblyAI: 5 hours/month free
# Deepgram: 150 minutes/month free
# Both support various video formats and URLs
