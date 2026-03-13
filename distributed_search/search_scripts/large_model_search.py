#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分布式搜索 - 大模型实习岗位
搜索关键词：深圳 大模型 实习 算法工程师 LLM 微调
时间范围优先级：过去7天内 > 过去30天内 > 过去180天内
"""

import requests
import json
import time
from datetime import datetime
import os
import sys

# SearXNG本地实例URL
SEARXNG_URL = "http://localhost:8080/search"

# 搜索关键词
QUERY = '"深圳 大模型 实习 算法工程师 LLM 微调 site:bosszhipin.com OR site:lagou.com OR site:nowcoder.com"'

# 时间范围配置（按优先级）
TIME_RANGES = [
    {"range": "day", "label": "past_day"},
    {"range": "week", "label": "past_week"}, 
    {"range": "month", "label": "past_month"},
    {"range": "year", "label": "past_year"}
]

def search_with_time_range(query, time_range=None):
    """使用指定时间范围进行搜索"""
    params = {
        'q': query,
        'format': 'json',
        'language': 'zh-CN',
        'safesearch': '0'
    }
    
    if time_range:
        params['time_range'] = time_range
    
    try:
        response = requests.post(SEARXNG_URL, data=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"搜索失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"搜索异常: {e}")
        return None

def filter_results(results):
    """过滤结果，只保留包含关键职位词的条目"""
    if not results or 'results' not in results:
        return []
    
    filtered = []
    keywords = ['算法工程师', '实习生', '微调', '实习', '大模型', 'LLM']
    
    for result in results['results']:
        title = result.get('title', '').lower()
        content = result.get('content', '').lower()
        
        # 检查是否包含职位关键词
        has_keyword = any(kw in title or kw in content for kw in keywords)
        
        # 排除校招汇总页、公司主页等模糊内容
        exclude_patterns = ['校招汇总', '校园招聘', '公司首页', '验证', '验证码', '登录']
        is_excluded = any(pattern in title or pattern in content for pattern in exclude_patterns)
        
        # 只保留具体的职位页面
        if has_keyword and not is_excluded:
            # 检查URL是否来自目标招聘网站
            url = result.get('url', '')
            if any(domain in url for domain in ['bosszhipin.com', 'lagou.com', 'nowcoder.com']):
                filtered.append(result)
    
    return filtered

def main():
    """主函数"""
    all_results = []
    
    # 按时间范围优先级搜索
    for time_config in TIME_RANGES:
        print(f"搜索时间范围: {time_config['label']}")
        results = search_with_time_range(QUERY, time_config['range'])
        
        if results:
            filtered_results = filter_results(results)
            print(f"找到 {len(filtered_results)} 条相关结果")
            
            # 去重（基于URL）
            existing_urls = {r['url'] for r in all_results}
            new_results = [r for r in filtered_results if r['url'] not in existing_urls]
            all_results.extend(new_results)
            
            # 如果已经找到足够多的结果，可以提前结束
            if len(all_results) >= 15:
                break
        
        time.sleep(1)  # 避免请求过于频繁
    
    # 限制结果数量
    final_results = all_results[:15]
    
    # 保存结果
    today = datetime.now().strftime("%Y%m%d")
    output_dir = "/home/admin/.openclaw/workspace/distributed_search/search_buffer"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/large_model_{today}.json"
    
    result_data = {
        "query": QUERY,
        "search_time": datetime.now().isoformat(),
        "total_found": len(final_results),
        "results": final_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print(f"搜索完成！结果已保存到: {output_file}")
    print(f"总共找到 {len(final_results)} 条相关岗位信息")

if __name__ == "__main__":
    main()