#!/usr/bin/env python3
import requests
import json
import sys

def search_searxng(query, categories=None, time_range=None):
    """
    Search using local SearXNG instance
    """
    url = "http://172.19.15.210:8080/search"
    
    params = {
        'q': query,
        'format': 'json',
        'language': 'zh-CN'
    }
    
    if categories:
        params['categories'] = categories
    if time_range:
        params['time_range'] = time_range
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error searching SearXNG: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_searxng.py <query> [categories] [time_range]")
        sys.exit(1)
    
    query = sys.argv[1]
    categories = sys.argv[2] if len(sys.argv) > 2 else None
    time_range = sys.argv[3] if len(sys.argv) > 3 else None
    
    results = search_searxng(query, categories, time_range)
    if results:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("No results or error occurred")