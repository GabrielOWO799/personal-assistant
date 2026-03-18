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
import re
from urllib.parse import urlparse

def search_searxng(query, time_range="", timeout=30):
    """使用SearXNG搜索"""
    try:
        url = "http://localhost:8080/search"
        data = {
            'q': query,
            'format': 'json',
            'language': 'zh-CN',
            'time_range': time_range,
            'safesearch': '0'
        }
        
        response = requests.post(url, data=data, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"搜索失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"搜索异常: {e}")
        return None

def is_valid_job_url(url):
    """检查是否为有效的职位URL"""
    parsed = urlparse(url)
    # 检查是否来自指定的招聘网站
    valid_domains = ['zhipin.com', 'liepin.com', 'shixiseng.com']
    if not any(domain in parsed.netloc for domain in valid_domains):
        return False
    
    # 排除校招汇总页、公司主页、验证页面等
    invalid_patterns = [
        r'/company/', r'/corp/', r'/validate', r'/verify', 
        r'/campus', r'/xiaozhao', r'/school', r'/login',
        r'/register', r'/user/', r'/account/'
    ]
    
    for pattern in invalid_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return False
    
    return True

def contains_job_keywords(title, content):
    """检查是否包含职位关键词"""
    job_keywords = ['工程师', '实习生', '算法', '开发', '研发', '程序员', '软件', '数据', 'AI', '人工智能', '机器学习', '深度学习']
    text = (title or '') + ' ' + (content or '')
    return any(keyword in text for keyword in job_keywords)

def extract_job_info(result):
    """提取职位信息"""
    return {
        'title': result.get('title', ''),
        'url': result.get('url', ''),
        'content': result.get('content', ''),
        'source': result.get('engine', ''),
        'published_date': result.get('publishedDate', ''),
        'timestamp': time.time()
    }

def main():
    # 获取当前日期用于文件名
    current_date = datetime.now().strftime("%Y%m%d")
    output_file = f"/home/admin/.openclaw/workspace/distributed_search/search_buffer/ai_agent_{current_date}.json"
    
    all_results = []
    seen_urls = set()
    
    # 时间范围优先级：过去7天 > 过去30天 > 过去180天
    time_ranges = [
        ('day', '过去7天内'),
        ('week', '过去30天内'), 
        ('month', '过去180天内')
    ]
    
    base_query = "深圳 AI Agent 实习 职位 工程师 算法 site:zhipin.com OR site:liepin.com OR site:shixiseng.com"
    
    for time_range_key, description in time_ranges:
        print(f"搜索 {description}...")
        
        results = search_searxng(base_query, time_range=time_range_key, timeout=30)
        
        if results and 'results' in results:
            for result in results['results']:
                url = result.get('url', '')
                
                # 去重和过滤
                if url in seen_urls:
                    continue
                
                if not is_valid_job_url(url):
                    continue
                
                if not contains_job_keywords(result.get('title', ''), result.get('content', '')):
                    continue
                
                job_info = extract_job_info(result)
                all_results.append(job_info)
                seen_urls.add(url)
                
                # 最多提取15条
                if len(all_results) >= 15:
                    break
        
        if len(all_results) >= 15:
            break
        
        # 避免请求过于频繁
        time.sleep(1)
    
    # 保存结果
    output_data = {
        'search_time': datetime.now().isoformat(),
        'query': base_query,
        'total_results': len(all_results),
        'results': all_results[:15]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"搜索完成！找到 {len(all_results)} 条相关职位信息")
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main()