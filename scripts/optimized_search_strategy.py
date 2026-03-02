#!/usr/bin/env python3
"""
优化的深圳AI Agent实习岗位搜索策略
- 使用精确的site限定搜索
- 针对主要招聘网站进行定向搜索
- 实现关键词过滤和去重
"""

import json
import subprocess
import time
import re
from datetime import datetime, timedelta

# 优化的搜索关键词组合
SEARCH_QUERIES = [
    # BOSS直聘定向搜索
    '"深圳 AI Agent 实习" site:zhipin.com',
    '"深圳 智能体开发 实习" site:zhipin.com', 
    '"深圳 大模型应用 实习" site:zhipin.com',
    '"深圳 LangChain 实习" site:zhipin.com',
    '"深圳 AutoGen 实习" site:zhipin.com',
    '"深圳 RAG 实习" site:zhipin.com',
    
    # 拉勾网定向搜索
    '"深圳 AI Agent 实习" site:lagou.com',
    '"深圳 大模型 实习" site:lagou.com',
    '"深圳 Prompt Engineering 实习" site:lagou.com',
    
    # 猎聘定向搜索  
    '"深圳 AI Agent 实习" site:liepin.com',
    '"深圳 智能体 实习" site:liepin.com',
    '"深圳 LLM应用 实习" site:liepin.com',
    
    # 实习僧定向搜索
    '"深圳 AI 实习" site:shixiseng.com',
    '"深圳 人工智能 实习" site:shixiseng.com',
    
    # 通用搜索（作为备用）
    '深圳 "AI Agent" 实习',
    '深圳 "智能体开发" 实习',
    '深圳 "大模型应用" 实习',
    '深圳 "LangChain" 实习',
    '深圳 "AutoGen" 实习', 
    '深圳 "RAG" 实习',
    '深圳 "Prompt Engineering" 实习'
]

def execute_searxng_search(query):
    """执行SearXNG搜索"""
    try:
        result = subprocess.run([
            "python3", "scripts/searxng_search.py", 
            query, "jobs", "zh", "10"
        ], capture_output=True, text=True, cwd="/home/admin/.openclaw/workspace")
        
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return data.get('results', [])
            except json.JSONDecodeError:
                print(f"JSON解析失败: {result.stdout[:200]}")
                return []
        else:
            print(f"搜索失败 ({query}): {result.stderr}")
            return []
    except Exception as e:
        print(f"搜索异常 ({query}): {e}")
        return []

def filter_relevant_results(results):
    """过滤相关结果"""
    relevant_keywords = [
        'AI Agent', '智能体', '大模型', 'LangChain', 'AutoGen', 
        'CrewAI', 'RAG', '检索增强', 'Prompt', '提示工程',
        'LLM', '大语言模型', '实习', '实习生'
    ]
    
    filtered = []
    for result in results:
        title = result.get('title', '').lower()
        content = result.get('content', '').lower()
        url = result.get('url', '')
        
        # 检查是否包含相关关键词
        is_relevant = any(keyword.lower() in title or keyword.lower() in content 
                         for keyword in relevant_keywords)
        
        # 检查是否为招聘网站
        is_job_site = any(site in url for site in [
            'zhipin.com', 'lagou.com', 'liepin.com', 'shixiseng.com',
            '51job.com', 'yingjiesheng.com', 'nowcoder.com'
        ])
        
        if is_relevant or is_job_site:
            filtered.append(result)
    
    return filtered

def search_optimized_jobs():
    """执行优化的搜索"""
    all_results = []
    
    print("开始执行优化的深圳AI Agent实习岗位搜索...")
    
    for i, query in enumerate(SEARCH_QUERIES, 1):
        print(f"正在搜索 ({i}/{len(SEARCH_QUERIES)}): {query}")
        
        results = execute_searxng_search(query)
        filtered_results = filter_relevant_results(results)
        
        print(f"找到 {len(filtered_results)} 个相关结果")
        all_results.extend(filtered_results)
        
        # 避免请求过于频繁
        time.sleep(1)
    
    # 去重
    unique_results = remove_duplicates(all_results)
    print(f"去重后剩余 {len(unique_results)} 个结果")
    
    return unique_results[:15]  # 返回前15个，确保有足够候选

def remove_duplicates(results):
    """基于标题和URL去重"""
    seen_titles = set()
    seen_urls = set()
    unique_results = []
    
    for result in results:
        title = result.get('title', '').strip()
        url = result.get('url', '').strip()
        
        # 标准化URL（移除参数等）
        clean_url = re.sub(r'\?.*$', '', url)
        
        if title and title not in seen_titles and clean_url not in seen_urls:
            seen_titles.add(title)
            seen_urls.add(clean_url)
            unique_results.append(result)
    
    return unique_results

if __name__ == "__main__":
    results = search_optimized_jobs()
    
    # 输出为JSON格式
    output = {"results": results}
    print(json.dumps(output, ensure_ascii=False, indent=2))