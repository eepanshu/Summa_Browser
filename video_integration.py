# Complete Video Integration for SummaBrowser
# Supports: YouTube URLs, Direct Video URLs, File Uploads

import os
import sys
import requests
import json
import time
import tempfile
from urllib.parse import urlparse, parse_qs

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def advanced_summarize(text):
    """Enhanced text summarization (import from main app)"""
    try:
        # Import from the main app
        from app import advanced_summarize as main_summarizer
        return main_summarizer(text)
    except ImportError:
        # Fallback simple summarization
        sentences = text.split('. ')
        if len(sentences) <= 3:
            return text
        
        # Simple extractive summarization
        word_freq = {}
        words = text.lower().split()
        
        for word in words:
            if word not in word_freq:
                word_freq[word] = 0
            word_freq[word] += 1
        
        sentence_scores = {}
        for sentence in sentences:
            for word in sentence.lower().split():
                if word in word_freq:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = 0
                    sentence_scores[sentence] += word_freq[word]
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        summary_length = min(3, len(top_sentences))
        summary = '. '.join([sentence for sentence, score in top_sentences[:summary_length]])
        
        return summary if summary else text[:500] + "..."

class VideoProcessor:
    def __init__(self):
        self.youtube_api_key = os.environ.get('YOUTUBE_API_KEY')
        self.assemblyai_key = os.environ.get('ASSEMBLYAI_API_KEY')
        self.deepgram_key = os.environ.get('DEEPGRAM_API_KEY')
    
    def extract_youtube_id(self, url):
        """Extract YouTube video ID from URL"""
        try:
            if 'youtu.be' in url:
                return url.split('/')[-1].split('?')[0]
            elif 'youtube.com' in url:
                parsed = urlparse(url)
                return parse_qs(parsed.query)['v'][0]
            return None
        except:
            return None
    
    def get_youtube_transcript(self, video_url):
        """Get YouTube transcript using youtube-transcript-api"""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            from pytube import YouTube
            
            video_id = self.extract_youtube_id(video_url)
            if not video_id:
                return None, "Invalid YouTube URL"
            
            # Get transcript
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                transcript = ' '.join([item['text'] for item in transcript_list])
            except Exception as e:
                return None, f"No transcript available: {str(e)}"
            
            # Get video metadata
            try:
                yt = YouTube(video_url)
                metadata = {
                    'title': yt.title,
                    'author': yt.author,
                    'length': yt.length,
                    'views': yt.views
                }
            except:
                metadata = {}
            
            # Generate summary
            summary = advanced_summarize(transcript)
            
            return {
                'success': True,
                'transcript': transcript,
                'summary': summary,
                'metadata': metadata,
                'type': 'youtube_transcript'
            }
            
        except ImportError:
            return None, "YouTube transcript libraries not installed"
        except Exception as e:
            return None, f"YouTube processing failed: {str(e)}"
    
    def transcribe_with_assemblyai(self, video_url):
        """Use AssemblyAI for video transcription"""
        if not self.assemblyai_key:
            return None, "AssemblyAI API key not provided"
        
        try:
            headers = {
                'authorization': self.assemblyai_key,
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
                return None, f"AssemblyAI submission failed: {response.text}"
            
            transcript_id = response.json()['id']
            
            # Poll for completion
            max_attempts = 60  # 5 minutes max
            for attempt in range(max_attempts):
                response = requests.get(
                    f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
                    headers=headers
                )
                
                result = response.json()
                
                if result['status'] == 'completed':
                    return {
                        'success': True,
                        'transcript': result['text'],
                        'summary': result.get('summary', ''),
                        'highlights': result.get('auto_highlights_result', {}).get('results', []),
                        'type': 'assemblyai'
                    }
                elif result['status'] == 'error':
                    return None, f"AssemblyAI transcription failed: {result['error']}"
                
                time.sleep(5)
            
            return None, "AssemblyAI transcription timeout"
            
        except Exception as e:
            return None, f"AssemblyAI error: {str(e)}"
    
    def process_video(self, video_input, input_type='url'):
        """Main video processing function"""
        try:
            if input_type == 'url':
                video_url = video_input
                
                # Check if it's a YouTube URL
                if 'youtube.com' in video_url or 'youtu.be' in video_url:
                    # Try YouTube transcript first (free and fast)
                    result = self.get_youtube_transcript(video_url)
                    if result and result[0] is None:
                        # If transcript fails, try AssemblyAI
                        result = self.transcribe_with_assemblyai(video_url)
                    return result
                else:
                    # For other video URLs, use AssemblyAI
                    return self.transcribe_with_assemblyai(video_url)
            
            elif input_type == 'file':
                # Handle file upload (would need additional implementation)
                return None, "File upload processing not implemented yet"
            
            else:
                return None, "Unsupported input type"
                
        except Exception as e:
            return None, f"Video processing error: {str(e)}"

# Global video processor instance
video_processor = VideoProcessor()

def process_video_request(video_input, input_type='url'):
    """Process video request and return result"""
    result = video_processor.process_video(video_input, input_type)
    
    if result and isinstance(result, dict) and result.get('success'):
        return result
    elif result and len(result) == 2:  # Error tuple
        return {
            'success': False,
            'error': result[1]
        }
    else:
        return {
            'success': False,
            'error': 'Unknown error occurred'
        }

if __name__ == "__main__":
    # Test with a YouTube video
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll for testing
    result = process_video_request(test_url)
    print(json.dumps(result, indent=2))
