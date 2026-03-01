#!/usr/bin/env python3
"""
Local SearXNG search script with timestamp extraction
"""
import requests
import sys
import json
import re
from datetime import datetime, timedelta

def extract_time_from_content(content):
    """尝试从内容中提取时间信息"""
    if not content:
        return "未知时间"
    
    # 常见的时间模式
    patterns = [
        r'(\d{1,2}小时前)',
        r'(\d{1,2}分钟前)',
        r'(\d{4}年\d{1,2}月\d{1,2}日)',
        r'(\d{1,2}月\d{1,2}日)',
        r'(\d{1,2}:\d{2})',
        r'(今天)',
        r'(昨天)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    
    return "未知时间"

def search(query, categories=None, language='zh', results=10):
    """Search using local SearXNG instance"""
    url = "http://localhost:8080/search"
    
    params = {
        'q': query,
        'format': 'json',
        'language': language,
        'safesearch': '0',
        'time_range': 'day',  # 限制为24小时内
        'categories': categories or 'news'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            # Extract relevant results
            results_list = []
            for result in data.get('results', [])[:results]:
                time_info = extract_time_from_content(result.get('content', ''))
                results_list.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'content': result.get('content', ''),
                    'engine': result.get('engine', ''),
                    'published_date': time_info
                })
            return {'results': results_list, 'query': query}
        else:
            return {'error': f'HTTP {response.status_code}'}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: searxng_search.py <query> [categories] [language] [results]")
        sys.exit(1)
    
    query = sys.argv[1]
    categories = sys.argv[2] if len(sys.argv) > 2 else None
    language = sys.argv[3] if len(sys.argv) > 3 else 'zh'
    results = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    
    result = search(query, categories, language, results)
    print(json.dumps(result, indent=2, ensure_ascii=False))