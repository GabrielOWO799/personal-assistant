#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分布式搜索 - 智能体实习岗位
搜索深圳智能体相关实习开发工程师岗位
"""

import json
import os
import sys
import time
from datetime import datetime
import requests
from urllib.parse import quote_plus

def search_searxng(query, time_range=None):
    """
    使用本地SearXNG实例进行搜索
    """
    try:
        # 本地SearXNG实例地址
        searxng_url = "http://localhost:8080/search"
        
        params = {
            'q': query,
            'format': 'json',
            'safesearch': '0',
            'language': 'zh-CN'
        }
        
        # 添加时间范围参数（如果指定）
        if time_range == 'past_week':
            params['time_range'] = 'week'
        elif time_range == 'past_month':
            params['time_range'] = 'month'
        elif time_range == 'past_6months':
            params['time_range'] = '6months'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(searxng_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    
    except Exception as e:
        print(f"搜索错误: {e}")
        return None

def is_valid_job_result(result):
    """
    验证搜索结果是否为有效的职位信息
    """
    title = result.get('title', '').lower()
    url = result.get('url', '').lower()
    
    # 必须包含的关键词
    required_keywords = ['开发工程师', '实习生', 'multi-agent', '智能体']
    
    # 排除的页面类型
    exclude_patterns = [
        '校招汇总', '校园招聘', '公司主页', '验证', 'captcha',
        'verification', 'login', 'signin', '注册'
    ]
    
    # 检查是否包含必要关键词
    has_required = any(kw in title for kw in required_keywords)
    
    # 检查是否包含排除模式
    has_exclude = any(pattern in title or pattern in url for pattern in exclude_patterns)
    
    # 检查是否来自指定的招聘网站
    valid_sites = ['zhaopin.com', '51job.com', 'yingjiesheng.com']
    from_valid_site = any(site in url for site in valid_sites)
    
    return has_required and from_valid_site and not has_exclude

def main():
    """主函数"""
    current_date = datetime.now().strftime('%Y%m%d')
    output_dir = '/home/admin/.openclaw/workspace/distributed_search/search_buffer'
    os.makedirs(output_dir, exist_ok=True)
    output_file = f'{output_dir}/intelligent_agent_{current_date}.json'
    
    # 搜索关键词
    base_query = '"深圳 智能体 实习 开发工程师 Multi-Agent" (site:zhaopin.com OR site:51job.com OR site:yingjiesheng.com)'
    
    # 时间范围优先级：过去7天 > 过去30天 > 过去180天
    time_ranges = [
        ('past_week', '过去7天内'),
        ('past_month', '过去30天内'), 
        ('past_6months', '过去180天内')
    ]
    
    all_results = []
    seen_urls = set()
    
    for time_range_code, time_range_name in time_ranges:
        print(f"搜索 {time_range_name} 的职位...")
        
        results = search_searxng(base_query, time_range_code)
        if not results or 'results' not in results:
            continue
            
        for result in results['results']:
            if len(all_results) >= 15:
                break
                
            # 去重检查
            url = result.get('url', '')
            if url in seen_urls:
                continue
                
            # 验证结果有效性
            if is_valid_job_result(result):
                result['search_time_range'] = time_range_name
                result['collected_at'] = datetime.now().isoformat()
                all_results.append(result)
                seen_urls.add(url)
                
        if len(all_results) >= 15:
            break
    
    # 保存结果
    output_data = {
        'search_query': base_query,
        'total_results': len(all_results),
        'search_date': datetime.now().isoformat(),
        'results': all_results[:15]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"搜索完成！找到 {len(all_results)} 个相关职位")
    print(f"结果已保存到: {output_file}")

if __name__ == '__main__':
    main()