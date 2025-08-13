#!/usr/bin/env python3
"""
Test to show current status and what needs to be configured
"""

import requests

def check_current_status():
    print("🔍 CURRENT DEPLOYMENT STATUS CHECK")
    print("=" * 50)
    
    api_url = "https://summabrowser-api.onrender.com"
    
    # Test 1: Basic endpoint
    print("1️⃣ Testing basic endpoint...")
    try:
        response = requests.post(f"{api_url}/process-video", data={"video_url": ""}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            error = data.get('error', '')
            print(f"✅ Endpoint exists: {error}")
        else:
            print(f"❌ Endpoint issue: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # Test 2: Check with actual video URL
    print("\n2️⃣ Testing with video URL...")
    try:
        response = requests.post(
            f"{api_url}/process-video", 
            data={"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}, 
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("🎉 SUCCESS: Video processed!")
                print(f"Summary: {data.get('summary', '')[:100]}...")
            else:
                error = data.get('error', '')
                print(f"❌ Processing failed: {error}")
                
                if "API key" in error:
                    print("\n💡 SOLUTION NEEDED:")
                    print("   Go to Render Dashboard → Your Service → Environment")
                    print("   Add environment variable:")
                    print("   Key: ASSEMBLYAI_API_KEY")
                    print("   Value: <hidden>")
                    print("   Then click 'Save Changes' to redeploy")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 3: Try a video with existing transcript (should work without API key)
    print("\n3️⃣ Testing video with built-in transcript...")
    try:
        # Popular video likely to have transcript
        test_url = "https://www.youtube.com/watch?v=kJQP7kiw5Fk"  # Despacito (has captions)
        response = requests.post(
            f"{api_url}/process-video", 
            data={"video_url": test_url}, 
            timeout=45
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("🎉 SUCCESS with built-in transcript!")
                print(f"Method: {data.get('processing_method', 'Unknown')}")
                print(f"Summary preview: {data.get('summary', '')[:150]}...")
                return True
            else:
                print(f"❌ Still failed: {data.get('error', '')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    success = check_current_status()
    
    print(f"\n{'='*50}")
    if success:
        print("✅ Some video processing is working!")
        print("💡 To enable ALL videos, add the AssemblyAI API key to Render")
    else:
        print("❌ Video processing needs configuration")
        print("💡 Add ASSEMBLYAI_API_KEY to your Render environment variables")
        print("🔑 Key: <hidden>")
