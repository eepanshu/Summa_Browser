#!/usr/bin/env python3
"""
Quick deployment test script for SummaBrowser video support
Run this to check if video support has been deployed
"""

import requests
import time
import json
from datetime import datetime

API_URL = "https://summabrowser-api.onrender.com"

def test_deployment():
    print(f"🔍 Testing SummaBrowser deployment at: {API_URL}")
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # Test 1: Check web interface
    try:
        response = requests.get(API_URL, headers={"Accept": "text/html"}, timeout=10)
        if response.status_code == 200:
            html = response.text
            
            # Check for video support indicators
            has_video = any(keyword in html for keyword in [
                "Video", "video", "YouTube", "videoUrlInput", "v2.2.0"
            ])
            
            if has_video:
                print("✅ WEB INTERFACE: Video support detected!")
                
                # Look for specific video elements
                if "videoUrlInput" in html:
                    print("   ✅ Video URL input field found")
                if "YouTube" in html:
                    print("   ✅ YouTube references found")
                if "v2.2.0" in html:
                    print("   ✅ Version 2.2.0 detected")
                    
            else:
                print("❌ WEB INTERFACE: Video support not found")
                print("   ℹ️  Still showing old version")
        else:
            print(f"❌ WEB INTERFACE: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ WEB INTERFACE: Connection error - {e}")
    
    # Test 2: Check video endpoint
    try:
        response = requests.post(f"{API_URL}/process-video", 
                               data={"video_url": ""}, 
                               timeout=10)
        if response.status_code == 404:
            print("❌ VIDEO ENDPOINT: Not found (deployment not complete)")
        elif response.status_code == 200:
            data = response.json()
            print("✅ VIDEO ENDPOINT: Exists and responding")
        else:
            print(f"⚠️ VIDEO ENDPOINT: HTTP {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ VIDEO ENDPOINT: Connection error")
    except Exception as e:
        print(f"⚠️ VIDEO ENDPOINT: {e}")
    
    # Test 3: Check health endpoint
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ HEALTH CHECK: {data.get('status', 'OK')}")
        else:
            print(f"❌ HEALTH CHECK: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ HEALTH CHECK: {e}")
    
    print("=" * 60)
    return has_video if 'has_video' in locals() else False

def main():
    print("🎥 SummaBrowser Video Support Deployment Test")
    print("🚀 Checking if video processing is deployed...")
    print()
    
    # Initial test
    video_support = test_deployment()
    
    if video_support:
        print("🎉 SUCCESS! Video support is deployed and working!")
        return
    
    print()
    print("⏳ Video support not detected yet. This is normal for new deployments.")
    print("💡 Render deployments can take 10-20 minutes, especially with new dependencies.")
    print()
    print("📊 Monitoring deployment progress...")
    print("   - Will check every 60 seconds")
    print("   - Press Ctrl+C to stop")
    print()
    
    # Monitor deployment
    attempt = 1
    max_attempts = 20  # 20 minutes max
    
    while attempt <= max_attempts:
        print(f"🔄 Check #{attempt} of {max_attempts}")
        time.sleep(60)  # Wait 1 minute
        
        video_support = test_deployment()
        if video_support:
            print()
            print("🎉 SUCCESS! Video support is now deployed!")
            print("🌐 Visit: https://summabrowser-api.onrender.com")
            print("🎥 Look for the YouTube URL input field")
            break
        
        attempt += 1
        print(f"⏳ Still waiting... (will check {max_attempts - attempt} more times)")
        print()
    
    if not video_support:
        print("⚠️ Video support not detected after 20 minutes.")
        print("🔧 There may be a deployment issue that needs manual investigation.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
