#!/usr/bin/env python3
"""
改进的深圳AI Agent实习岗位搜索脚本
专门针对招聘网站和职位信息进行优化
"""
import requests
import sys
import json
import re
from datetime import datetime, timedelta

def extract_time_from_content(content):
    """尝试从内容中提取时间信息"""
    if not content:
        return "未知时间"
    
    # 常见的时间模式
    patterns = [
        r'(\d{1,2}小时前)',
        r'(\d{1,2}分钟前)',
        r'(\d{4}年\d{1,2}月\d{1,2}日)',
        r'(\d{1,2}月\d{1,2}日)',
        r'(\d{1,2}:\d{2})',
        r'(今天)',
        r'(昨天)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    
    return "未知时间"

def is_job_related(title, content):
    """判断是否为职位相关信息"""
    job_keywords = ['实习', '招聘', '职位', '岗位', '工程师', '开发', '算法', '实习生']
    text = (title + ' ' + content).lower()
    return any(keyword in text for keyword in job_keywords)

def search_job_positions(query, language='zh', results=10):
    """专门搜索职位信息"""
    url = "http://localhost:8080/search"
    
    # 尝试多个类别组合
    categories_list = ['general', 'jobs', 'news']
    all_results = []
    
    for category in categories_list:
        params = {
            'q': query,
            'format': 'json',
            'language': language,
            'safesearch': '0',
            'time_range': 'week',  # 扩大到一周内
            'categories': category
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for result in data.get('results', []):
                    # 过滤出职位相关的结果
                    if is_job_related(result.get('title', ''), result.get('content', '')):
                        time_info = extract_time_from_content(result.get('content', ''))
                        all_results.append({
                            'title': result.get('title', ''),
                            'url': result.get('url', ''),
                            'content': result.get('content', ''),
                            'engine': result.get('engine', ''),
                            'published_date': time_info,
                            'category': category
                        })
        except Exception as e:
            continue
    
    # 去重并返回结果
    unique_results = []
    seen_titles = set()
    for result in all_results:
        title = result.get('title', '')
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_results.append(result)
            if len(unique_results) >= results:
                break
    
    return unique_results[:results]

def extract_job_details(result):
    """从搜索结果中提取职位详情"""
    title = result.get('title', '')
    content = result.get('content', '')
    url = result.get('url', '')
    
    # 尝试提取公司名称
    company = "未知公司"
    # 常见的公司名模式
    company_patterns = [
        r'(.+?)招聘',
        r'(.+?)诚聘',
        r'(.+?)[\s\-—]实习',
        r'(.+?)实习生'
    ]
    
    for pattern in company_patterns:
        match = re.search(pattern, title)
        if match:
            company = match.group(1).strip()
            break
    
    # 尝试提取工作地点
    location = "深圳"
    location_patterns = ['南山区', '福田区', '罗湖区', '宝安区', '龙岗区', '龙华区', '坪山区', '光明区', '盐田区', '大鹏新区']
    for loc in location_patterns:
        if loc in title or loc in content:
            location = loc
            break
    
    # 提取核心要求（简化版）
    requirements = "查看职位详情"
    tech_keywords = ['Python', 'Java', 'AI', '机器学习', '深度学习', '大模型', 'LLM', 'LangChain', 'AutoGen', 'RAG', 'Prompt']
    found_tech = []
    text = title + ' ' + content
    for tech in tech_keywords:
        if tech in text:
            found_tech.append(tech)
    
    if found_tech:
        requirements = "、".join(found_tech[:2]) + "等"
    
    return {
        'position': title,
        'company': company,
        'location': location,
        'requirements': requirements,
        'source': url
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: job_search_improved.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    raw_results = search_job_positions(query, 'zh', 15)
    
    # 提取详细的职位信息
    job_details = []
    for result in raw_results:
        details = extract_job_details(result)
        job_details.append(details)
    
    output = {
        'query': query,
        'jobs': job_details[:10]  # 返回最多10个职位
    }
    
    print(json.dumps(output, indent=2, ensure_ascii=False))