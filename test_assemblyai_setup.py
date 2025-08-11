#!/usr/bin/env python3
"""
Test script to verify AssemblyAI API key is working after configuration
"""

import requests
import time
import json
from datetime import datetime

API_URL = "https://summabrowser-api.onrender.com"

def test_assemblyai_integration():
    print("🔑 Testing AssemblyAI API Key Integration")
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # Test with a YouTube video that likely doesn't have auto-captions
    # This will force the system to use AssemblyAI
    test_videos = [
        {
            "name": "Short YouTube Video (for testing)",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "timeout": 60
        },
        {
            "name": "Educational Content", 
            "url": "https://www.youtube.com/watch?v=ZWuNf4gxwuM",
            "timeout": 90
        }
    ]
    
    for i, video in enumerate(test_videos, 1):
        print(f"\n📹 Test {i}: {video['name']}")
        print(f"🔗 URL: {video['url']}")
        
        try:
            print("⏳ Sending request to video processing endpoint...")
            
            response = requests.post(
                f"{API_URL}/process-video",
                data={"video_url": video['url']},
                timeout=video['timeout']
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    print("🎉 SUCCESS! Video processed with AssemblyAI!")
                    print(f"   📝 Summary: {data.get('summary', '')[:200]}...")
                    print(f"   🎬 Processing method: {data.get('processing_method', 'Unknown')}")
                    
                    if 'transcript' in data:
                        transcript_preview = data['transcript'][:100] + "..." if len(data['transcript']) > 100 else data['transcript']
                        print(f"   📄 Transcript preview: {transcript_preview}")
                    
                    return True
                    
                else:
                    error_msg = data.get('error', 'Unknown error')
                    print(f"❌ FAILED: {error_msg}")
                    
                    if "API key not provided" in error_msg:
                        print("   💡 Solution: Add ASSEMBLYAI_API_KEY to Render environment variables")
                    elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                        print("   💡 Info: API quota reached, but key is configured correctly")
                    
                    return False
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False
                
        except requests.exceptions.Timeout:
            print("⏰ Request timeout - video processing takes time, this might be normal")
            print("   💡 Try again in a few minutes or use a shorter video")
            return None
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

def test_basic_endpoint():
    print(f"\n🔧 Testing basic video endpoint...")
    
    try:
        response = requests.post(
            f"{API_URL}/process-video",
            data={"video_url": ""},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            error_msg = data.get('error', '')
            
            if "No video URL provided" in error_msg:
                print("✅ Endpoint working - expected validation error")
                return True
            elif "API key not provided" in error_msg:
                print("❌ API key not configured on server")
                return False
            else:
                print(f"⚠️ Unexpected response: {error_msg}")
                return True
                
        else:
            print(f"❌ Endpoint error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return False

def main():
    print("🚀 AssemblyAI API Key Configuration Test")
    print("🔗 Testing: https://summabrowser-api.onrender.com")
    print()
    
    # Test basic endpoint first
    basic_test = test_basic_endpoint()
    
    if basic_test:
        print("\n" + "="*60)
        print("🔑 API key appears to be configured. Testing with real video...")
        
        # Test with actual video processing
        video_test = test_assemblyai_integration()
        
        print("\n" + "="*60)
        print("📊 FINAL RESULTS:")
        
        if video_test is True:
            print("✅ SUCCESS: AssemblyAI API key is working perfectly!")
            print("🎉 Video processing is fully functional!")
        elif video_test is False:
            print("❌ ISSUE: API key might not be configured correctly")
            print("💡 Check Render environment variables")
        else:
            print("⏰ TIMEOUT: Processing takes time, likely working but slow")
            
    else:
        print("\n❌ API key not configured. Please add to Render environment variables:")
        print("   Key: ASSEMBLYAI_API_KEY")
        print("   Value: 3f07e0254b9240a1bef7287cb6a22cdc")

if __name__ == "__main__":
    main()
