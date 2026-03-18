#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分布式搜索 - 智能体实习岗位
搜索关键词：深圳 智能体 实习 开发工程师 Multi-Agent
时间范围优先级：过去7天 > 过去30天 > 过去180天
"""

import requests
import json
import time
from datetime import datetime
import os

# 创建目录
buffer_dir = "/home/admin/.openclaw/workspace/distributed_search/search_buffer"
os.makedirs(buffer_dir, exist_ok=True)

# SearXNG本地实例URL
SEARXNG_URL = "http://localhost:8080"

# 搜索关键词和时间范围配置
search_configs = [
    {
        "query": '深圳 智能体 实习 开发工程师 Multi-Agent site:zhaopin.com OR site:51job.com OR site:yingjiesheng.com',
        "time_range": "day",  # 过去24小时（近似7天内）
        "priority": 1
    },
    {
        "query": '深圳 智能体 实习 开发工程师 Multi-Agent site:zhaopin.com OR site:51job.com OR site:yingjiesheng.com',
        "time_range": "week",  # 过去一周
        "priority": 2
    },
    {
        "query": '深圳 智能体 实习 开发工程师 Multi-Agent site:zhaopin.com OR site:51job.com OR site:yingjiesheng.com',
        "time_range": "month",  # 过去一个月
        "priority": 3
    },
    {
        "query": '深圳 智能体 实习 开发工程师 Multi-Agent site:zhaopin.com OR site:51job.com OR site:yingjiesheng.com',
        "time_range": "year",  # 过去一年（近似180天）
        "priority": 4
    }
]

def search_searxng(query, time_range=None, timeout=30):
    """使用SearXNG进行搜索"""
    params = {
        'q': query,
        'format': 'json',
        'language': 'zh-CN',
        'safesearch': '0'
    }
    
    if time_range:
        params['time_range'] = time_range
    
    try:
        response = requests.get(SEARXNG_URL, params=params, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"搜索失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"搜索异常: {e}")
        return None

def filter_results(results):
    """过滤结果，只保留包含关键职位信息的条目"""
    filtered = []
    keywords = ['开发工程师', '实习生', 'Multi-Agent', '智能体', 'agent']
    
    if not results or 'results' not in results:
        return filtered
    
    for result in results['results']:
        title = result.get('title', '').lower()
        content = result.get('content', '').lower()
        url = result.get('url', '')
        
        # 检查是否包含必要的关键词
        has_required_keywords = any(kw in title or kw in content for kw in keywords)
        
        # 排除校招汇总页、公司主页等
        exclude_patterns = ['校招汇总', '公司介绍', '验证', '验证码', 'login', 'signin']
        should_exclude = any(pattern in url.lower() or pattern in title for pattern in exclude_patterns)
        
        # 检查是否是具体的招聘网站职位页面
        is_job_page = any(domain in url for domain in ['zhaopin.com', '51job.com', 'yingjiesheng.com'])
        
        if has_required_keywords and not should_exclude and is_job_page:
            filtered.append({
                'title': result.get('title', ''),
                'url': url,
                'content': result.get('content', ''),
                'source': result.get('engine', ''),
                'timestamp': datetime.now().isoformat()
            })
    
    return filtered

def main():
    """主函数"""
    all_results = []
    seen_urls = set()
    
    print("开始执行分布式搜索任务...")
    
    # 按优先级顺序执行搜索
    for config in search_configs:
        print(f"搜索时间范围: {config['time_range']}, 优先级: {config['priority']}")
        
        results = search_searxng(config['query'], config['time_range'], timeout=25)
        if results:
            filtered = filter_results(results)
            
            # 去重
            for item in filtered:
                if item['url'] not in seen_urls:
                    item['search_priority'] = config['priority']
                    all_results.append(item)
                    seen_urls.add(item['url'])
        
        # 避免过于频繁的请求
        time.sleep(2)
    
    # 限制结果数量
    final_results = all_results[:15]
    
    # 保存结果
    output_file = f"{buffer_dir}/intelligent_agent_{datetime.now().strftime('%Y%m%d')}.json"
    
    result_data = {
        'search_time': datetime.now().isoformat(),
        'total_found': len(final_results),
        'results': final_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print(f"搜索完成！找到 {len(final_results)} 个相关岗位")
    print(f"结果已保存到: {output_file}")
    
    return len(final_results)

if __name__ == "__main__":
    main()