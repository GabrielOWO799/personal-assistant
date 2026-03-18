#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分布式搜索 - 智能体实习岗位 (改进版)
使用本地SearXNG实例进行搜索，添加请求头避免403错误
"""

import requests
import json
import time
from datetime import datetime
import os

# 创建目录
os.makedirs('/home/admin/.openclaw/workspace/distributed_search/search_buffer', exist_ok=True)

def search_searxng(query, time_range=None):
    """使用SearXNG进行搜索"""
    url = "http://localhost:8080/search"
    
    params = {
        'q': query,
        'format': 'json',
        'language': 'zh-CN',
        'safesearch': '0'
    }
    
    if time_range:
        params['time_range'] = time_range
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Referer': 'http://localhost:8080/'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        print(f"搜索参数: {params}")
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"搜索失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"搜索异常: {e}")
        return None

def extract_relevant_jobs(results, max_results=15):
    """提取相关岗位信息"""
    if not results or 'results' not in results:
        return []
    
    relevant_jobs = []
    target_keywords = ['开发工程师', '实习生', 'Multi-Agent', '智能体', 'agent']
    exclude_keywords = ['校招', '汇总', '主页', '验证', '公司介绍']
    
    for result in results['results']:
        title = result.get('title', '').lower()
        content = result.get('content', '').lower()
        url = result.get('url', '')
        
        # 检查是否包含目标关键词
        has_target = any(keyword.lower() in title or keyword.lower() in content for keyword in target_keywords)
        
        # 检查是否包含排除关键词
        has_exclude = any(keyword.lower() in title or keyword.lower() in content for keyword in exclude_keywords)
        
        # 检查是否是招聘网站的具体职位页面
        is_job_page = any(domain in url for domain in ['zhaopin.com', '51job.com', 'yingjiesheng.com'])
        is_specific = any(keyword in url for keyword in ['job', 'position', 'detail'])
        
        if has_target and not has_exclude and (is_job_page or is_specific):
            job_info = {
                'title': result.get('title', ''),
                'url': url,
                'content_snippet': result.get('content', '')[:200],
                'source': result.get('engine', ''),
                'published_date': result.get('publishedDate', '')
            }
            relevant_jobs.append(job_info)
            
            if len(relevant_jobs) >= max_results:
                break
    
    return relevant_jobs

def main():
    print("开始执行分布式搜索任务...")
    
    # 搜索关键词
    base_query = '"深圳 智能体 实习 开发工程师 Multi-Agent" (site:zhaopin.com OR site:51job.com OR site:yingjiesheng.com)'
    
    # 时间范围优先级：过去7天 > 过去30天 > 过去180天
    time_ranges = [
        ('day', '过去24小时'),
        ('week', '过去7天'),
        ('month', '过去30天'),
        ('year', '过去180天')
    ]
    
    all_results = []
    
    for time_range, description in time_ranges:
        print(f"搜索时间范围: {description}, 优先级: {time_ranges.index((time_range, description)) + 1}")
        
        results = search_searxng(base_query, time_range)
        if results:
            jobs = extract_relevant_jobs(results)
            all_results.extend(jobs)
            print(f"找到 {len(jobs)} 个相关岗位")
        else:
            print("搜索失败或无结果")
        
        # 避免请求过于频繁
        time.sleep(2)
    
    # 去重（基于URL）
    unique_results = []
    seen_urls = set()
    for job in all_results:
        if job['url'] not in seen_urls:
            unique_results.append(job)
            seen_urls.add(job['url'])
    
    # 限制结果数量
    final_results = unique_results[:15]
    
    # 保存结果
    today = datetime.now().strftime('%Y%m%d')
    output_file = f'/home/admin/.openclaw/workspace/distributed_search/search_buffer/intelligent_agent_{today}.json'
    
    result_data = {
        'search_time': datetime.now().isoformat(),
        'total_found': len(final_results),
        'results': final_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print(f"搜索完成！找到 {len(final_results)} 个相关岗位")
    print(f"结果已保存到: {output_file}")

if __name__ == '__main__':
    main()