#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from datetime import datetime

# 设置SearXNG URL环境变量
os.environ['SEARXNG_URL'] = 'http://localhost:8080'

def search_news(query, limit=15, time_range='week'):
    """使用SearXNG搜索新闻"""
    try:
        # 构建命令
        cmd = [
            sys.executable,
            '/home/admin/.openclaw/workspace/skills/searxng/scripts/searxng.py',
            'search',
            query,
            '-n', str(limit),
            '-c', 'news',
            '-t', time_range,
            '-f', 'json'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('results', [])
        else:
            print(f"Error running search: {result.stderr}")
            return []
    except Exception as e:
        print(f"Exception during search: {e}")
        return []

def search_general(query, limit=10):
    """使用SearXNG进行通用搜索"""
    try:
        cmd = [
            sys.executable,
            '/home/admin/.openclaw/workspace/skills/searxng/scripts/searxng.py',
            'search',
            query,
            '-n', str(limit),
            '-c', 'general',
            '-f', 'json'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('results', [])
        else:
            print(f"Error running general search: {result.stderr}")
            return []
    except Exception as e:
        print(f"Exception during general search: {e}")
        return []

def extract_relevant_results(results, keywords):
    """从结果中提取相关的内容"""
    relevant = []
    for result in results:
        title = result.get('title', '').lower()
        content = result.get('content', '').lower()
        url = result.get('url', '')
        
        # 检查是否包含关键词
        if any(keyword.lower() in title or keyword.lower() in content for keyword in keywords):
            # 过滤掉不相关的网站
            if not any(domain in url for domain in ['youtube.com', 'facebook.com', 'twitter.com', 'instagram.com']):
                relevant.append(result)
    
    return relevant[:8]  # 最多返回8条

def main():
    # 搜索关键词
    ai_agent_results = search_news('"AI Agent"', limit=20, time_range='week')
    large_model_results = search_news('"大模型"', limit=20, time_range='week')
    
    # 如果新闻搜索结果不足，尝试通用搜索
    if len(ai_agent_results) < 5:
        ai_agent_general = search_general('"AI Agent"', limit=15)
        ai_agent_results.extend(ai_agent_general)
    
    if len(large_model_results) < 5:
        large_model_general = search_general('"大模型"', limit=15)
        large_model_results.extend(large_model_general)
    
    # 合并结果并去重
    all_results = []
    seen_urls = set()
    
    for result in ai_agent_results + large_model_results:
        url = result.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            all_results.append(result)
    
    # 提取最相关的8条结果
    relevant_results = extract_relevant_results(all_results, ['AI Agent', '大模型', '人工智能', '智能体'])
    
    # 确保至少有8条结果
    if len(relevant_results) < 8:
        # 添加更多通用结果
        additional_results = search_general('AI Agent OR "large language model"', limit=20)
        for result in additional_results:
            url = result.get('url', '')
            if url and url not in seen_urls and len(relevant_results) < 8:
                seen_urls.add(url)
                relevant_results.append(result)
    
    # 输出结果
    for i, result in enumerate(relevant_results[:8], 1):
        title = result.get('title', 'No title')
        url = result.get('url', '')
        content = result.get('content', '')
        published_date = result.get('publishedDate', '')
        source = result.get('url', '').split('/')[2] if result.get('url', '') else 'Unknown'
        
        print(f"--- Result {i} ---")
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Published: {published_date}")
        print(f"Source: {source}")
        print(f"Content: {content[:200]}...")
        print()

if __name__ == "__main__":
    main()