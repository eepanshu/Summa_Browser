#!/usr/bin/env python3
"""
Quick video test for immediate results
"""

import requests
import json

def test_quick_video():
    print("🚀 Quick Video Processing Test")
    print("=" * 40)
    
    # Very short video for quick testing
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"🎥 Testing: {video_url}")
    print("⏳ Processing...")
    
    try:
        response = requests.post(
            "https://summabrowser-api.onrender.com/process-video",
            data={"video_url": video_url},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n📊 Status: {'✅ SUCCESS' if data.get('success') else '❌ FAILED'}")
            
            if data.get('success'):
                print(f"🎬 Processing Method: {data.get('processing_method', 'Unknown')}")
                print(f"\n📝 SUMMARY:")
                print("-" * 30)
                print(data.get('summary', 'No summary available'))
                
                if 'transcript' in data and data['transcript']:
                    print(f"\n📄 TRANSCRIPT (preview):")
                    print(data['transcript'][:200] + "..." if len(data['transcript']) > 200 else data['transcript'])
                
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_quick_video()
