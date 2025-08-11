# Video Summarization Enhancement for SummaBrowser
# Option 1: YouTube Integration

import os
import requests
import re
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_youtube_transcript(video_url):
    """Get transcript from YouTube video"""
    try:
        video_id = extract_video_id(video_url)
        if not video_id:
            return None, "Invalid YouTube URL"
        
        # Try to get transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all text
        full_text = ""
        for entry in transcript_list:
            full_text += entry['text'] + " "
        
        # Get video info
        yt = YouTube(video_url)
        video_info = {
            'title': yt.title,
            'duration': yt.length,
            'views': yt.views,
            'description': yt.description[:500] + "..." if len(yt.description) > 500 else yt.description
        }
        
        return full_text.strip(), video_info
        
    except Exception as e:
        return None, f"Error extracting transcript: {str(e)}"

def process_youtube_video(video_url):
    """Process YouTube video and return summary"""
    transcript, video_info = get_youtube_transcript(video_url)
    
    if transcript:
        # Use existing summarization function
        summary = advanced_summarize(transcript)
        
        return {
            'success': True,
            'video_info': video_info,
            'transcript': transcript,
            'summary': summary,
            'type': 'youtube_video'
        }
    else:
        return {
            'success': False,
            'error': video_info  # video_info contains error message in this case
        }

# New requirements to add:
# youtube-transcript-api
# pytube
