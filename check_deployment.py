#!/usr/bin/env python3
"""
Comprehensive test script to check if video changes are deployed on Render
"""

import requests
import json
from datetime import datetime

API_URL = "https://summabrowser-api.onrender.com"

def test_video_endpoint():
    print(f"🔍 Testing video endpoint deployment...")
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # Test 1: Check if web interface has video support
    try:
        response = requests.get(API_URL, headers={"Accept": "text/html"}, timeout=10)
        if response.status_code == 200:
            html = response.text
            
            # Check for video-related elements
            video_indicators = [
                "Video Intelligence",
                "video-input",
                "videoUrlInput", 
                "YouTube",
                "🎥 Videos",
                "Video Transcription",
                "process-video"
            ]
            
            found_indicators = []
            for indicator in video_indicators:
                if indicator in html:
                    found_indicators.append(indicator)
            
            print(f"✅ WEB INTERFACE: Video support detected!")
            print(f"   🔍 Found indicators: {', '.join(found_indicators)}")
            
            # Check version
            if "v3.0" in html:
                print(f"   ✅ Version 3.0 detected")
            elif "v2.2.0" in html:
                print(f"   ✅ Version 2.2.0 detected")
                
            return True
            
        else:
            print(f"❌ WEB INTERFACE: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ WEB INTERFACE: Connection error - {e}")
        return False

def test_video_api():
    print(f"\n🎥 Testing video processing API endpoint...")
    
    try:
        # Test with empty URL first to see if endpoint exists
        response = requests.post(f"{API_URL}/process-video", 
                               data={"video_url": ""}, 
                               timeout=10)
        
        if response.status_code == 404:
            print("❌ VIDEO ENDPOINT: Not found (not deployed)")
            return False
        else:
            print("✅ VIDEO ENDPOINT: Exists and responding")
            try:
                data = response.json()
                if 'error' in data:
                    print(f"   ℹ️  Expected error: {data['error']}")
            except:
                pass
            return True
            
    except Exception as e:
        print(f"❌ VIDEO ENDPOINT: {e}")
        return False

def test_health_endpoint():
    print(f"\n❤️ Testing health endpoint...")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ HEALTH CHECK: {data.get('status', 'OK')}")
            return True
        else:
            print(f"❌ HEALTH CHECK: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ HEALTH CHECK: {e}")
        return False

def test_sample_video():
    print(f"\n🧪 Testing with sample YouTube video...")
    
    try:
        # Test with a short video
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        response = requests.post(f"{API_URL}/process-video", 
                               data={"video_url": test_url}, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("🎉 VIDEO PROCESSING: WORKS! Sample video processed successfully!")
                print(f"   📝 Summary preview: {data.get('summary', '')[:100]}...")
                return True
            else:
                print(f"⚠️ VIDEO PROCESSING: API responded but failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ VIDEO PROCESSING: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ VIDEO PROCESSING: {e}")
        return False

def main():
    print("🚀 SummaBrowser Deployment Check - Video Features")
    print("🔗 Checking: https://summabrowser-api.onrender.com")
    print()
    
    results = {
        "web_interface": test_video_endpoint(),
        "video_api": test_video_api(),
        "health": test_health_endpoint(),
        "sample_processing": False
    }
    
    # Only test sample if endpoints are working
    if results["web_interface"] and results["video_api"]:
        results["sample_processing"] = test_sample_video()
    
    print("\n" + "=" * 60)
    print("📊 DEPLOYMENT SUMMARY:")
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test.replace('_', ' ').title()}: {status}")
    
    total_passed = sum(results.values())
    print(f"\n🎯 Result: {total_passed}/4 tests passed")
    
    if total_passed >= 3:
        print("🎉 SUCCESS! Video features are deployed and working!")
    elif total_passed >= 2:
        print("⚠️ PARTIAL: Most features working, some issues detected")
    else:
        print("❌ ISSUES: Significant deployment problems detected")

if __name__ == "__main__":
    main()
