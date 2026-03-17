#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分布式搜索 - AI Agent 实习职位
使用SearXNG本地实例搜索深圳AI Agent相关实习职位
"""

import requests
import json
import time
from datetime import datetime
import os

def search_searxng(query, time_range=None):
    """使用SearXNG搜索"""
    url = "http://localhost:8080/search"
    
    # 构建搜索参数
    params = {
        'q': query,
        'format': 'json',
        'language': 'zh-CN',
        'safesearch': '0'
    }
    
    if time_range:
        params['time_range'] = time_range
    
    try:
        response = requests.post(url, data=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"搜索失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"搜索异常: {e}")
        return None

def filter_results(results):
    """过滤结果，只保留包含关键词的职位"""
    if not results or 'results' not in results:
        return []
    
    filtered = []
    target_keywords = ['工程师', '实习生', '算法', '开发', '研发']
    exclude_keywords = ['校招', '汇总', '公司', '验证', '主页']
    
    for result in results['results']:
        title = result.get('title', '').lower()
        content = result.get('content', '').lower()
        url = result.get('url', '')
        
        # 检查是否包含目标关键词
        has_target = any(kw in title or kw in content for kw in target_keywords)
        
        # 检查是否包含排除关键词
        has_exclude = any(kw in title or kw in content for kw in exclude_keywords)
        
        # 检查URL是否来自招聘网站
        is_job_site = any(site in url for site in ['zhipin.com', 'liepin.com', 'shixiseng.com'])
        
        if has_target and not has_exclude and is_job_site:
            filtered.append({
                'title': result.get('title', ''),
                'url': url,
                'content': result.get('content', ''),
                'published_date': result.get('publishedDate', ''),
                'source': result.get('engine', '')
            })
    
    return filtered[:15]  # 最多返回15条

def main():
    # 创建输出目录
    output_dir = "/home/admin/.openclaw/workspace/distributed_search/search_buffer"
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取当前日期
    today = datetime.now().strftime("%Y%m%d")
    output_file = f"{output_dir}/ai_agent_{today}.json"
    
    # 搜索查询
    base_query = "深圳 AI Agent 实习 职位 工程师 算法 site:zhipin.com OR site:liepin.com OR site:shixiseng.com"
    
    all_results = []
    
    # 按时间范围优先级搜索
    time_ranges = ['d', 'w', 'm']  # 过去24小时, 过去7天, 过去30天
    
    for time_range in time_ranges:
        print(f"搜索时间范围: {time_range}")
        results = search_searxng(base_query, time_range)
        if results:
            filtered = filter_results(results)
            # 避免重复
            for result in filtered:
                if result not in all_results:
                    all_results.append(result)
        
        if len(all_results) >= 15:
            break
        
        time.sleep(1)  # 避免请求过快
    
    # 如果还没有足够结果，搜索更长时间范围
    if len(all_results) < 15:
        print("搜索无时间限制的结果")
        results = search_searxng(base_query)
        if results:
            filtered = filter_results(results)
            for result in filtered:
                if result not in all_results:
                    all_results.append(result)
    
    # 保存结果
    final_results = all_results[:15]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'search_time': datetime.now().isoformat(),
            'query': base_query,
            'total_results': len(final_results),
            'results': final_results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"搜索完成，找到 {len(final_results)} 条结果，保存到 {output_file}")

if __name__ == "__main__":
    main()