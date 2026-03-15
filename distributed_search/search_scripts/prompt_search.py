#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分布式搜索 - 提示词工程实习岗位
搜索深圳地区 Prompt Engineer 相关实习岗位
"""

import json
import os
import sys
import time
from datetime import datetime
import requests

def search_searxng(query, time_range=None):
    """使用本地SearXNG实例搜索"""
    try:
        url = "http://localhost:8080/search"
        params = {
            'q': query,
            'format': 'json',
            'language': 'zh-CN',
            'time_range': time_range,
            'safesearch': '0'
        }
        
        response = requests.get(url, params=params, timeout=25)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"搜索失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"搜索异常: {e}")
        return None

def is_valid_job_result(result):
    """验证是否为有效的职位结果"""
    title = result.get('title', '').lower()
    content = result.get('content', '').lower()
    url = result.get('url', '').lower()
    
    # 必须包含的关键词
    required_keywords = ['prompt', '提示词', '实习生', '实习']
    has_required = any(kw in title or kw in content for kw in required_keywords)
    
    # 排除模糊内容
    exclude_patterns = [
        '校招汇总', '校园招聘', '公司主页', '验证', 'captcha',
        'verification', 'login', '注册', 'signup', 'sign up'
    ]
    
    is_excluded = any(pattern in title or pattern in content or pattern in url 
                     for pattern in exclude_patterns)
    
    # 必须是具体的职位页面（不是列表页）
    is_specific_page = ('interns.com.cn' in url or 'shixiseng.com' in url or 
                       'liepin.com' in url) and ('detail' in url or 'job' in url)
    
    return has_required and not is_excluded and is_specific_page

def extract_job_info(result):
    """提取职位信息"""
    return {
        'title': result.get('title', ''),
        'url': result.get('url', ''),
        'content_snippet': result.get('content', '')[:200],
        'source': result.get('url', '').split('/')[2] if result.get('url') else '',
        'published_date': result.get('publishedDate', ''),
        'score': result.get('score', 0)
    }

def main():
    # 创建输出目录
    buffer_dir = "/home/admin/.openclaw/workspace/distributed_search/search_buffer"
    os.makedirs(buffer_dir, exist_ok=True)
    
    today_str = datetime.now().strftime("%Y%m%d")
    output_file = f"{buffer_dir}/prompt_{today_str}.json"
    
    # 搜索查询
    base_query = '"深圳 提示词工程 实习 Prompt Engineer site:interns.com.cn OR site:shixiseng.com OR site:liepin.com"'
    
    all_results = []
    job_info_list = []
    
    # 按时间优先级搜索：7天 > 30天 > 180天
    time_ranges = ['day', 'week', 'month', 'year']
    
    for time_range in time_ranges:
        print(f"搜索时间范围: {time_range}")
        results = search_searxng(base_query, time_range)
        
        if results and 'results' in results:
            valid_results = [r for r in results['results'] if is_valid_job_result(r)]
            all_results.extend(valid_results)
            
            # 去重
            seen_urls = set()
            unique_results = []
            for r in all_results:
                if r.get('url') not in seen_urls:
                    unique_results.append(r)
                    seen_urls.add(r.get('url'))
            
            all_results = unique_results
            
            if len(all_results) >= 15:
                break
    
    # 提取最多15条结果
    final_results = all_results[:15]
    
    # 转换为职位信息格式
    for result in final_results:
        job_info = extract_job_info(result)
        if job_info['title']:  # 确保有标题
            job_info_list.append(job_info)
    
    # 保存结果
    output_data = {
        'search_time': datetime.now().isoformat(),
        'query': base_query,
        'total_found': len(job_info_list),
        'jobs': job_info_list
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"搜索完成，找到 {len(job_info_list)} 个相关职位")
    print(f"结果已保存到: {output_file}")
    
    return len(job_info_list)

if __name__ == "__main__":
    try:
        count = main()
        sys.exit(0 if count >= 0 else 1)
    except Exception as e:
        print(f"执行异常: {e}")
        sys.exit(1)