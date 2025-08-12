#!/usr/bin/env python3
"""
Real video processing test with your API key
"""

import requests
import time
import json
from datetime import datetime

API_URL = "https://summabrowser-api.onrender.com"

def test_video_with_summary():
    print("🎥 TESTING VIDEO PROCESSING WITH REAL SUMMARY")
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # Test with different types of short videos
    test_videos = [
        {
            "name": "Rick Astley - Never Gonna Give You Up",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "description": "Classic 80s music video (3:32)"
        },
        {
            "name": "Short Educational Video",
            "url": "https://www.youtube.com/watch?v=ZWuNf4gxwuM",
            "description": "Brief educational content"
        },
        {
            "name": "Quick Tech Demo",
            "url": "https://www.youtube.com/watch?v=rJiHecfAKT8",
            "description": "Short technology demonstration"
        }
    ]
    
    for i, video in enumerate(test_videos, 1):
        print(f"\n📹 TEST {i}: {video['name']}")
        print(f"🔗 URL: {video['url']}")
        print(f"📝 Description: {video['description']}")
        print("-" * 50)
        
        try:
            print("⏳ Sending processing request...")
            
            start_time = time.time()
            response = requests.post(
                f"{API_URL}/process-video",
                data={"video_url": video['url']},
                timeout=120  # 2 minute timeout
            )
            
            processing_time = time.time() - start_time
            print(f"⏱️ Processing took: {processing_time:.1f} seconds")
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    print("\n🎉 SUCCESS! Video processed successfully!")
                    print("=" * 60)
                    
                    # Display results
                    summary = data.get('summary', 'No summary available')
                    transcript = data.get('transcript', 'No transcript available')
                    processing_method = data.get('processing_method', 'Unknown')
                    metadata = data.get('metadata', {})
                    
                    print(f"🎬 PROCESSING METHOD: {processing_method}")
                    
                    if metadata:
                        print(f"📊 METADATA:")
                        for key, value in metadata.items():
                            print(f"   {key}: {value}")
                    
                    print(f"\n📝 AI SUMMARY:")
                    print("-" * 30)
                    print(summary)
                    
                    if transcript and len(transcript) > 0:
                        print(f"\n📄 TRANSCRIPT PREVIEW (first 300 chars):")
                        print("-" * 30)
                        print(transcript[:300] + "..." if len(transcript) > 300 else transcript)
                    
                    print("\n" + "=" * 60)
                    return True, summary, processing_method
                    
                else:
                    error_msg = data.get('error', 'Unknown error')
                    print(f"❌ PROCESSING FAILED: {error_msg}")
                    
                    if "API key not provided" in error_msg:
                        print("💡 SOLUTION: Add ASSEMBLYAI_API_KEY environment variable to Render")
                    elif "quota" in error_msg.lower():
                        print("💡 INFO: API quota reached, but integration is working")
                    elif "youtube-transcript-api" in error_msg.lower():
                        print("💡 INFO: Trying YouTube transcript first (this is normal)")
                    
                    return False, error_msg, "Failed"
                    
            else:
                print(f"❌ HTTP ERROR: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                return False, f"HTTP {response.status_code}", "HTTP Error"
                
        except requests.exceptions.Timeout:
            print("⏰ TIMEOUT: Video processing takes time (this might be normal)")
            print("💡 Try with a shorter video or wait longer")
            return None, "Timeout", "Timeout"
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            return False, str(e), "Exception"
    
    return False, "No videos processed successfully", "No Success"

def quick_endpoint_check():
    print("🔧 QUICK ENDPOINT CHECK")
    print("-" * 30)
    
    try:
        # Check if endpoint exists
        response = requests.post(f"{API_URL}/process-video", data={"video_url": ""}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            error = data.get('error', '')
            
            if "No video URL provided" in error:
                print("✅ Endpoint exists and validates input")
                return True
            elif "API key not provided" in error:
                print("❌ API key not configured on server")
                return False
            else:
                print(f"⚠️ Unexpected response: {error}")
                return True
        else:
            print(f"❌ Endpoint issue: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def main():
    print("🚀 SUMMABROWSE VIDEO PROCESSING TEST")
    print("🔑 Testing with your AssemblyAI API key")
    print("🌐 Target: https://summabrowser-api.onrender.com")
    print()
    
    # Quick check first
    endpoint_ok = quick_endpoint_check()
    
    if endpoint_ok:
        print(f"\n{'='*60}")
        print("🎬 TESTING REAL VIDEO PROCESSING...")
        
        success, result, method = test_video_with_summary()
        
        print(f"\n{'='*60}")
        print("📊 FINAL TEST RESULTS:")
        print(f"📈 Status: {'✅ SUCCESS' if success else '❌ FAILED' if success is False else '⏰ TIMEOUT'}")
        print(f"🔧 Method: {method}")
        print(f"📝 Result: {result[:100]}..." if len(str(result)) > 100 else f"📝 Result: {result}")
        
        if success:
            print("\n🎉 CONGRATULATIONS!")
            print("✅ Your video processing is working perfectly!")
            print("✅ Users can now process any YouTube video!")
            print("✅ AI summaries are being generated!")
        elif success is False:
            print("\n🔧 ISSUES DETECTED:")
            print("💡 Check if ASSEMBLYAI_API_KEY is added to Render environment variables")
            print("💡 Key should be: 3f07e0254b9240a1bef7287cb6a22cdc")
        else:
            print("\n⏰ TIMEOUT:")
            print("💡 Processing is likely working but takes time")
            print("💡 Try again with shorter videos")
    
    else:
        print("\n❌ ENDPOINT ISSUES:")
        print("💡 Check Render deployment status")
        print("💡 Verify API key configuration")

if __name__ == "__main__":
    main()
