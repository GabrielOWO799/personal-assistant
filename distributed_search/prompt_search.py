#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分布式搜索 - 提示词工程实习岗位
搜索深圳地区的Prompt Engineer相关实习岗位
"""

import json
import os
import sys
import time
from datetime import datetime
import requests
from urllib.parse import quote_plus

def search_searxng(query, time_range=None, timeout=30):
    """
    使用本地SearXNG实例进行搜索
    """
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
        if time_range == 'past_week':
            params['time_range'] = 'week'
        elif time_range == 'past_month':
            params['time_range'] = 'month'
        elif time_range == 'past_6months':
            params['time_range'] = '6months'
        
        print(f"Searching with query: {query}")
        print(f"Time range: {time_range}")
        
        response = requests.get(
            searxng_url, 
            params=params, 
            timeout=timeout,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Search failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Search error: {e}")
        return None

def extract_relevant_results(results, max_results=15):
    """
    从搜索结果中提取相关的实习岗位信息
    """
    if not results or 'results' not in results:
        return []
    
    extracted = []
    seen_urls = set()
    
    for result in results['results']:
        url = result.get('url', '')
        title = result.get('title', '')
        content = result.get('content', '')
        
        # 跳过重复URL
        if url in seen_urls:
            continue
        
        # 检查是否包含必要的关键词
        required_keywords = ['实习生', '实习', 'Prompt Engineer', '提示词工程师', '提示词工程']
        has_required = any(keyword in title or keyword in content for keyword in required_keywords)
        
        # 检查是否来自目标招聘网站
        target_sites = ['interns.com.cn', 'shixiseng.com', 'liepin.com']
        from_target_site = any(site in url for site in target_sites)
        
        # 排除模糊内容（校招汇总页、公司主页、验证页面等）
        exclude_patterns = ['校招', '校园招聘', '公司简介', '关于我们', 'verification', 'captcha', 'verify']
        should_exclude = any(pattern in title or pattern in content or pattern in url for pattern in exclude_patterns)
        
        if has_required and from_target_site and not should_exclude:
            extracted.append({
                'title': title,
                'url': url,
                'content': content[:200] + '...' if len(content) > 200 else content,
                'source': next((site for site in target_sites if site in url), 'unknown')
            })
            seen_urls.add(url)
            
            if len(extracted) >= max_results:
                break
    
    return extracted

def main():
    """主函数"""
    # 创建保存目录
    buffer_dir = "/home/admin/.openclaw/workspace/distributed_search/search_buffer"
    os.makedirs(buffer_dir, exist_ok=True)
    
    # 获取当前日期用于文件名
    current_date = datetime.now().strftime("%Y%m%d")
    output_file = f"{buffer_dir}/prompt_{current_date}.json"
    
    # 搜索关键词
    base_query = '"深圳 提示词工程 实习 Prompt Engineer site:interns.com.cn OR site:shixiseng.com OR site:liepin.com"'
    
    all_results = []
    
    # 按时间优先级搜索：过去7天 > 过去30天 > 过去180天
    time_ranges = [
        ('past_week', '过去7天内'),
        ('past_month', '过去30天内'), 
        ('past_6months', '过去180天内')
    ]
    
    for time_range_key, time_range_desc in time_ranges:
        print(f"\n=== 搜索 {time_range_desc} ===")
        
        results = search_searxng(base_query, time_range=time_range_key, timeout=30)
        
        if results:
            extracted = extract_relevant_results(results, max_results=15-len(all_results))
            all_results.extend(extracted)
            print(f"找到 {len(extracted)} 条相关结果")
        else:
            print("搜索失败或无结果")
        
        # 如果已经找到足够结果，提前结束
        if len(all_results) >= 15:
            all_results = all_results[:15]
            break
        
        # 避免请求过于频繁
        time.sleep(1)
    
    # 保存结果
    result_data = {
        'search_time': datetime.now().isoformat(),
        'query': base_query,
        'total_results': len(all_results),
        'results': all_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n搜索完成！结果已保存到: {output_file}")
    print(f"总共找到 {len(all_results)} 条相关岗位信息")

if __name__ == "__main__":
    main()