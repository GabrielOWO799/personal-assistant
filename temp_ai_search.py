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
        
        # 使用兼容Python 3.6.8的方式
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=60)
        
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
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=60)
        
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
    seen_urls = set()
    
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
    print("🔍 正在搜索 AI Agent 相关资讯...")
    ai_agent_results = search_news('"AI Agent"', limit=20, time_range='week')
    print(f"找到 {len(ai_agent_results)} 条 AI Agent 新闻")
    
    print("🔍 正在搜索 大模型 相关资讯...")
    large_model_results = search_news('"大模型"', limit=20, time_range='week')
    print(f"找到 {len(large_model_results)} 条 大模型 新闻")
    
    # 如果新闻搜索结果不足，尝试通用搜索
    if len(ai_agent_results) < 5:
        print("🔄 补充搜索 AI Agent 通用内容...")
        ai_agent_general = search_general('"AI Agent"', limit=15)
        ai_agent_results.extend(ai_agent_general)
        print(f"补充了 {len(ai_agent_general)} 条通用结果")
    
    if len(large_model_results) < 5:
        print("🔄 补充搜索 大模型 通用内容...")
        large_model_general = search_general('"大模型"', limit=15)
        large_model_results.extend(large_model_general)
        print(f"补充了 {len(large_model_general)} 条通用结果")
    
    # 合并结果并去重
    all_results = []
    seen_urls = set()
    
    for result in ai_agent_results + large_model_results:
        url = result.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            all_results.append(result)
    
    print(f"📊 合并后总共有 {len(all_results)} 条唯一结果")
    
    # 提取最相关的8条结果
    relevant_results = extract_relevant_results(all_results, ['AI Agent', '大模型', '人工智能', '智能体'])
    
    # 确保至少有8条结果
    if len(relevant_results) < 8:
        print(f"⚠️  只找到 {len(relevant_results)} 条相关结果，尝试补充更多...")
        additional_results = search_general('AI Agent OR "large language model"', limit=20)
        for result in additional_results:
            url = result.get('url', '')
            if url and url not in seen_urls and len(relevant_results) < 8:
                seen_urls.add(url)
                relevant_results.append(result)
    
    print(f"✅ 最终筛选出 {len(relevant_results)} 条高质量资讯")
    
    # 输出JSON格式结果
    output = {
        "results": relevant_results[:8],
        "timestamp": datetime.now().isoformat(),
        "query_keywords": ["AI Agent", "大模型"]
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()