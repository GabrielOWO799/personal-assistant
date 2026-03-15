#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分布式搜索 - AI Agent 实习岗位
使用本地SearXNG实例搜索深圳地区AI Agent相关实习职位
"""

import requests
import json
import time
from datetime import datetime
import os
import sys

# SearXNG本地实例URL
SEARXNG_URL = "http://localhost:8080/search"

# 搜索关键词配置
QUERY_TEMPLATE = '"深圳" "AI Agent" ("实习" OR "实习生") ("工程师" OR "算法" OR "开发") site:zhipin.com OR site:liepin.com OR site:shixiseng.com'

# 时间范围映射
TIME_RANGES = {
    'past_week': 'd',
    'past_month': 'm',
    'past_6months': 'y'
}

def search_searxng(query, time_range=None, timeout=30):
    """执行SearXNG搜索"""
    params = {
        'q': query,
        'format': 'json',
        'language': 'zh-CN',
        'safesearch': '0'
    }
    
    # 添加时间范围参数（如果指定）
    if time_range and time_range in TIME_RANGES:
        params['time_range'] = TIME_RANGES[time_range]
    
    try:
        response = requests.get(
            SEARXNG_URL,
            params=params,
            timeout=timeout,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"搜索失败: {e}")
        return None

def extract_job_info(result):
    """提取岗位信息"""
    title = result.get('title', '')
    url = result.get('url', '')
    content = result.get('content', '')
    
    # 检查是否包含必要的职位关键词
    required_keywords = ['工程师', '实习生', '算法', '开发']
    has_required = any(keyword in title or keyword in content for keyword in required_keywords)
    
    # 排除模糊内容
    exclude_patterns = ['校招', '汇总', '主页', '验证', '公司介绍']
    should_exclude = any(pattern in title or pattern in content for pattern in exclude_patterns)
    
    if has_required and not should_exclude:
        return {
            'title': title,
            'url': url,
            'content': content[:200],  # 截取前200字符
            'source': result.get('engine', ''),
            'published_date': result.get('publishedDate', '')
        }
    return None

def main():
    """主函数"""
    today = datetime.now().strftime('%Y%m%d')
    output_path = f'/home/admin/.openclaw/workspace/distributed_search/search_buffer/ai_agent_{today}.json'
    
    all_results = []
    
    # 按时间优先级搜索
    for time_range in ['past_week', 'past_month', 'past_6months']:
        print(f"搜索 {time_range} 范围...")
        
        results = search_searxng(QUERY_TEMPLATE, time_range, timeout=25)  # 留5秒缓冲
        
        if results and 'results' in results:
            for result in results['results']:
                job_info = extract_job_info(result)
                if job_info and job_info not in all_results:
                    all_results.append(job_info)
                    
        # 避免请求过于频繁
        time.sleep(2)
        
        # 如果已经找到足够结果，可以提前结束
        if len(all_results) >= 15:
            break
    
    # 限制结果数量
    final_results = all_results[:15]
    
    # 保存结果
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'search_time': datetime.now().isoformat(),
            'query': QUERY_TEMPLATE,
            'total_found': len(final_results),
            'results': final_results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"搜索完成！结果已保存到: {output_path}")
    print(f"总共找到 {len(final_results)} 条相关岗位信息")
    
    return len(final_results)

if __name__ == '__main__':
    try:
        result_count = main()
        sys.exit(0 if result_count >= 0 else 1)
    except Exception as e:
        print(f"脚本执行出错: {e}")
        sys.exit(1)