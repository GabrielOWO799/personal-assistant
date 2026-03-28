#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词相关岗位分布式搜索 - 2026-03-28
"""
import json
import requests
import re
from datetime import datetime

# 搜索配置
SEARCH_KEYWORDS = [
    "深圳 Prompt Engineer 实习 2026",
    "深圳 提示词工程师 实习 春招",
    "深圳 Prompt 实习 校招"
]

# 实习/春招关键词
INTERN_KEYWORDS = ['实习', '实习生', '校招', '春招', '2026届', '应届生']

# 排除关键词
EXCLUDE_KEYWORDS = ['全职', '社招', '3年以上', '5年以上', '资深', '专家']

def search_searxng(query, timeout=120):
    """使用SearXNG搜索"""
    try:
        url = "http://localhost:8080/search"
        params = {
            'q': query,
            'format': 'json',
            'language': 'zh-CN',
            'time_range': 'month'  # 最近一个月
        }
        response = requests.get(url, params=params, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"搜索失败: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"搜索异常: {e}")
        return None

def is_intern_or_campus(title, content=''):
    """判断是否为实习或春招岗位"""
    text = (title + ' ' + content).lower()
    
    # 检查是否包含实习/春招关键词
    has_intern = any(kw in text for kw in INTERN_KEYWORDS)
    
    # 检查是否包含排除关键词（社招）
    has_exclude = any(kw in text for kw in EXCLUDE_KEYWORDS)
    
    return has_intern and not has_exclude

def extract_job_info(result):
    """提取岗位信息"""
    title = result.get('title', '')
    url = result.get('url', '')
    content = result.get('content', '') or result.get('abstract', '')
    
    # 提取公司名称（从标题或内容）
    company = '未知公司'
    company_patterns = [
        r'([\u4e00-\u9fa5]+?)(?:招聘|校招|实习)',
        r'([\u4e00-\u9fa5]+?)(?:\s*[-|]\s*)',
        r'([A-Za-z]+(?:\s+[A-Za-z]+)*)'  # 英文公司名
    ]
    for pattern in company_patterns:
        match = re.search(pattern, title)
        if match:
            company = match.group(1).strip()
            if company and len(company) > 1:
                break
    
    # 提取岗位类型
    job_type = '实习'
    if any(kw in title for kw in ['校招', '春招', '2026届']):
        job_type = '校招/春招'
    elif '实习' in title:
        job_type = '实习'
    
    return {
        'title': title,
        'company': company,
        'url': url,
        'type': job_type,
        'description': content[:200] + '...' if len(content) > 200 else content,
        'source': result.get('engine', 'unknown')
    }

def main():
    print("=" * 50)
    print("提示词相关岗位分布式搜索")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    all_results = []
    seen_urls = set()
    
    for keyword in SEARCH_KEYWORDS:
        print(f"\n🔍 搜索: {keyword}")
        
        data = search_searxng(keyword, timeout=120)
        
        if data and 'results' in data:
            results = data['results']
            print(f"   找到 {len(results)} 条结果")
            
            for result in results:
                title = result.get('title', '')
                url = result.get('url', '')
                content = result.get('content', '') or result.get('abstract', '')
                
                # 去重
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                
                # 筛选实习/春招岗位
                if is_intern_or_campus(title, content):
                    job_info = extract_job_info(result)
                    all_results.append(job_info)
                    print(f"   ✅ {job_info['title'][:50]}...")
                else:
                    print(f"   ⏭️  跳过（非实习/春招）: {title[:40]}...")
        else:
            print(f"   ⚠️ 搜索失败或无结果")
    
    # 去重后最多保留5条
    unique_results = all_results[:5]
    
    print(f"\n📊 搜索结果汇总:")
    print(f"   共找到 {len(unique_results)} 条有效岗位")
    
    # 保存结果
    output_file = '/home/admin/.openclaw/workspace/distributed_search/search_buffer/prompt_20260328.json'
    output_data = {
        'search_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'keywords': SEARCH_KEYWORDS,
        'total_found': len(unique_results),
        'jobs': unique_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 结果已保存: {output_file}")
    
    # 打印摘要
    if unique_results:
        print("\n📋 岗位列表:")
        for i, job in enumerate(unique_results, 1):
            print(f"\n{i}. {job['title']}")
            print(f"   公司: {job['company']}")
            print(f"   类型: {job['type']}")
            print(f"   链接: {job['url']}")
    else:
        print("\n⚠️ 未找到符合条件的岗位")
    
    print("\n✅ 搜索完成!")

if __name__ == '__main__':
    main()
