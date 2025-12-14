#!/usr/bin/env python3
"""
Deployment Test Script for EmotionEye
Tests all API endpoints to ensure proper deployment
"""

import requests
import json
import sys
import time

def test_api(base_url="http://localhost:5000"):
    """Test all API endpoints"""
    print(f"🧪 Testing EmotionEye API at {base_url}")
    print("=" * 50)
    
    # Test 1: Health Check
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check: PASSED")
        else:
            print(f"❌ Health check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Health check: FAILED ({e})")
        return False
    
    # Test 2: Home endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Home endpoint: PASSED (v{data.get('version', 'unknown')})")
        else:
            print(f"❌ Home endpoint: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Home endpoint: FAILED ({e})")
        return False
    
    # Test 3: Emotion Analysis
    test_messages = [
        "I am feeling very happy today!",
        "I'm not feeling good right now",
        "This is amazing news!"
    ]
    
    for i, message in enumerate(test_messages, 1):
        try:
            response = requests.post(
                f"{base_url}/analyze",
                json={"message": message},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                emotion = data.get('emotion', 'unknown')
                confidence = data.get('confidence', 0)
                print(f"✅ Analysis {i}: PASSED ({emotion}, {confidence:.2f})")
            else:
                print(f"❌ Analysis {i}: FAILED ({response.status_code})")
                return False
        except Exception as e:
            print(f"❌ Analysis {i}: FAILED ({e})")
            return False
    
    # Test 4: Sentiment Trend
    try:
        response = requests.get(f"{base_url}/sentiment-trend", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sentiment trend: PASSED ({len(data)} emotions tracked)")
        else:
            print(f"❌ Sentiment trend: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Sentiment trend: FAILED ({e})")
        return False
    
    print("=" * 50)
    print("🎉 All tests PASSED! EmotionEye is ready for production.")
    return True

def wait_for_service(base_url="http://localhost:5000", max_attempts=30):
    """Wait for service to be available"""
    print(f"⏳ Waiting for service at {base_url}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code in [200, 503]:  # Service is responding
                print(f"✅ Service is responding after {attempt + 1} attempts")
                return True
        except:
            pass
        
        time.sleep(2)
        print(f"   Attempt {attempt + 1}/{max_attempts}...")
    
    print(f"❌ Service did not respond after {max_attempts} attempts")
    return False

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    # Wait for service to be available
    if not wait_for_service(base_url):
        sys.exit(1)
    
    # Run tests
    if test_api(base_url):
        sys.exit(0)
    else:
        sys.exit(1)