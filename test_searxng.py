#!/usr/bin/env python3
import requests
import json

def test_searxng():
    url = "http://localhost:8080/search"
    params = {
        'q': 'AI Agent',
        'format': 'json',
        'language': 'zh'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        print(f"Status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Found {len(data.get('results', []))} results")
                if data.get('results'):
                    print("First result:", data['results'][0].get('title', 'No title'))
            except json.JSONDecodeError:
                print("Response is not JSON, showing first 200 chars:")
                print(response.text[:200])
        else:
            print(f"Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_searxng()