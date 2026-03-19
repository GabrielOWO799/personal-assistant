#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分布式搜索 - AI Agent 实习职位 (修复版)
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
    
    # 构建表单数据
    data = {
        'q': query,
        'category_general': '1',
        'language': 'zh-CN',
        'safesearch': '0'
    }
    
    # 添加时间范围
    if time_range == 'd':
        data['time_range'] = 'day'
    elif time_range == 'w':
        data['time_range'] = 'week'
    elif time_range == 'm':
        data['time_range'] = 'month'
    # 注意：SearXNG的时间范围参数可能是 'day', 'week', 'month', 'year'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=30)
        print(f"请求状态码: {response.status_code}")
        if response.status_code == 200:
            # SearXNG返回的是HTML，我们需要解析它
            return response.text
        else:
            print(f"搜索失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"搜索异常: {e}")
        return None

def parse_html_results(html_content):
    """解析HTML结果，提取职位信息"""
    # 这是一个简化的解析器，实际可能需要更复杂的HTML解析
    import re
    
    results = []
    
    # 尝试提取标题和链接
    # 这里使用正则表达式作为临时解决方案
    title_pattern = r'<h3 class="result_header">.*?<a href="(.*?)"[^>]*>(.*?)</a>'
    matches = re.findall(title_pattern, html_content, re.DOTALL | re.IGNORECASE)
    
    for url, title in matches[:15]:
        # 清理HTML标签
        clean_title = re.sub(r'<[^>]+>', '', title)
        results.append({
            'title': clean_title.strip(),
            'url': url.strip(),
            'content': '',
            'published_date': '',
            'source': 'searxng'
        })
    
    return results

def filter_results(results):
    """过滤结果，只保留包含关键词的职位"""
    if not results:
        return []
    
    filtered = []
    target_keywords = ['工程师', '实习生', '算法', '开发', '研发']
    exclude_keywords = ['校招', '汇总', '公司', '验证', '主页']
    
    for result in results:
        title = result.get('title', '').lower()
        url = result.get('url', '')
        
        # 检查是否包含目标关键词
        has_target = any(kw in title for kw in target_keywords)
        
        # 检查是否包含排除关键词
        has_exclude = any(kw in title for kw in exclude_keywords)
        
        # 检查URL是否来自招聘网站
        is_job_site = any(site in url for site in ['zhipin.com', 'liepin.com', 'shixiseng.com'])
        
        if has_target and not has_exclude and is_job_site:
            filtered.append(result)
    
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
    time_ranges = [None, 'w', 'm']  # 无限制, 过去7天, 过去30天
    
    for time_range in time_ranges:
        print(f"搜索时间范围: {time_range if time_range else '无限制'}")
        html_content = search_searxng(base_query, time_range)
        if html_content:
            parsed_results = parse_html_results(html_content)
            filtered = filter_results(parsed_results)
            # 避免重复
            for result in filtered:
                if result not in all_results:
                    all_results.append(result)
        
        if len(all_results) >= 15:
            break
        
        time.sleep(2)  # 避免请求过快
    
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