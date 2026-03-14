#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分布式搜索脚本 - 大模型关键词
执行深圳地区大模型相关实习岗位搜索
"""

import json
import time
import requests
from datetime import datetime
import os

def search_searxng(query, time_range=None):
    """使用本地SearXNG实例进行搜索"""
    try:
        # 本地SearXNG实例地址
        searxng_url = "http://localhost:8080/search"
        
        params = {
            'q': query,
            'format': 'json',
            'language': 'zh-CN',
            'safesearch': '0'
        }
        
        # 添加时间范围参数（如果指定）
        if time_range == '7d':
            params['time_range'] = 'week'
        elif time_range == '30d':
            params['time_range'] = 'month'
        elif time_range == '180d':
            params['time_range'] = 'year'
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(searxng_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        print(f"搜索错误: {e}")
        return None

def filter_results(results, keywords_to_include, keywords_to_exclude):
    """过滤搜索结果"""
    if not results or 'results' not in results:
        return []
    
    filtered = []
    for result in results['results']:
        title = result.get('title', '').lower()
        content = result.get('content', '').lower()
        url = result.get('url', '')
        
        # 检查是否包含必需关键词
        has_required = any(keyword in title or keyword in content for keyword in keywords_to_include)
        
        # 检查是否包含排除关键词
        has_excluded = any(exclude in url for exclude in keywords_to_exclude)
        
        if has_required and not has_excluded:
            filtered.append({
                'title': result.get('title', ''),
                'url': url,
                'content': result.get('content', ''),
                'published_date': result.get('publishedDate', ''),
                'source': result.get('url', '').split('/')[2] if len(result.get('url', '').split('/')) > 2 else ''
            })
    
    return filtered[:15]  # 最多返回15条

def main():
    # 创建目录
    buffer_dir = "/home/admin/.openclaw/workspace/distributed_search/search_buffer"
    os.makedirs(buffer_dir, exist_ok=True)
    
    # 搜索关键词
    base_query = '"深圳 大模型 实习 算法工程师 LLM 微调 site:bosszhipin.com OR site:lagou.com OR site:nowcoder.com"'
    
    # 必需包含的关键词
    required_keywords = ['算法工程师', '实习生', '微调', '大模型', 'llm']
    
    # 排除的URL模式
    exclude_patterns = ['/company/', '/validate', '/campus', '/school', '/summary']
    
    all_results = []
    
    # 按时间优先级搜索：7天 > 30天 > 180天
    time_ranges = [('7d', '过去7天'), ('30d', '过去30天'), ('180d', '过去180天')]
    
    for time_range, desc in time_ranges:
        print(f"搜索 {desc}...")
        results = search_searxng(base_query, time_range)
        if results:
            filtered = filter_results(results, required_keywords, exclude_patterns)
            # 避免重复
            for item in filtered:
                if item['url'] not in [r['url'] for r in all_results]:
                    all_results.append(item)
        
        # 如果已经找到足够结果，可以提前结束
        if len(all_results) >= 15:
            all_results = all_results[:15]
            break
    
    # 保存结果
    output_file = f"{buffer_dir}/large_model_20260314.json"
    result_data = {
        'search_time': datetime.now().isoformat(),
        'query': base_query,
        'total_results': len(all_results),
        'results': all_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print(f"搜索完成，找到 {len(all_results)} 条结果，已保存到 {output_file}")

if __name__ == "__main__":
    main()