#!/usr/bin/env python3
"""
去重和过滤模块
- 基于标题+公司名称去重
- 按时间排序（如果有发布时间）
- 提取关键字段
"""

import re
import json
from datetime import datetime

def extract_company_from_title(title):
    """从标题中提取公司名称"""
    # 常见的标题格式："[公司名] 岗位名称" 或 "岗位名称 - 公司名"
    patterns = [
        r'^\[?([^\]]+?)\]?[：:\s]',  # [公司名] 岗位
        r'[-—]\s*([^-—]+)$',        # 岗位 - 公司名
        r'^([^\s]+?)\s+(?:招聘|实习生|实习)'  # 公司名 招聘...
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            company = match.group(1).strip()
            # 清理常见的前缀/后缀
            company = re.sub(r'^(招聘|实习|校招)\s*', '', company)
            company = re.sub(r'\s*(有限公司|有限责任公司|股份有限公司|科技|信息|网络)$', '', company)
            return company
    
    return "未知公司"

def extract_location(content):
    """从内容中提取工作地点"""
    # 优先匹配深圳的具体区域
    shenzhen_areas = ['南山区', '福田区', '罗湖区', '宝安区', '龙岗区', '盐田区', '龙华区', '坪山区', '光明区', '大鹏新区']
    
    for area in shenzhen_areas:
        if area in content:
            return area
    
    # 如果没有具体区域，返回深圳
    if '深圳' in content or '深圳市' in content:
        return '深圳市'
    
    return '深圳'

def extract_requirements(content):
    """提取核心要求（前100字）"""
    # 移除HTML标签和特殊字符
    clean_content = re.sub(r'<[^>]+>', '', content)
    clean_content = re.sub(r'\s+', ' ', clean_content).strip()
    
    # 取前100个字符
    return clean_content[:100] + ('...' if len(clean_content) > 100 else '')

def parse_job_result(result):
    """解析单个搜索结果为结构化数据"""
    title = result.get('title', '').strip()
    url = result.get('url', '').strip()
    content = result.get('content', '').strip()
    published_date = result.get('published_date', '')
    
    # 提取字段
    company = extract_company_from_title(title)
    location = extract_location(content)
    requirements = extract_requirements(content)
    
    return {
        'position': title,
        'company': company,
        'location': location,
        'requirements': requirements,
        'source': url,
        'published_date': published_date
    }

def deduplicate_and_sort(jobs):
    """去重并排序"""
    seen_jobs = set()
    unique_jobs = []
    
    for job in jobs:
        # 基于岗位名称+公司名称去重
        job_key = f"{job['position']}|{job['company']}"
        if job_key not in seen_jobs:
            seen_jobs.add(job_key)
            unique_jobs.append(job)
    
    # 按发布时间排序（如果有）
    def get_sort_key(job):
        date_str = job.get('published_date', '')
        try:
            # 尝试解析常见的时间格式
            if '小时前' in date_str:
                hours = int(re.search(r'(\d+)小时前', date_str).group(1))
                return datetime.now() - timedelta(hours=hours)
            elif '分钟前' in date_str:
                minutes = int(re.search(r'(\d+)分钟前', date_str).group(1))
                return datetime.now() - timedelta(minutes=minutes)
            elif '今天' in date_str:
                return datetime.now()
            elif '昨天' in date_str:
                return datetime.now() - timedelta(days=1)
            else:
                # 默认返回当前时间
                return datetime.now()
        except:
            return datetime.now()
    
    unique_jobs.sort(key=get_sort_key, reverse=True)
    return unique_jobs[:10]  # 返回最新的10个

if __name__ == "__main__":
    # 从stdin读取JSON数据
    import sys
    input_data = sys.stdin.read()
    
    try:
        data = json.loads(input_data)
        results = data.get('results', [])
        
        # 解析每个结果
        parsed_jobs = []
        for result in results:
            parsed_job = parse_job_result(result)
            parsed_jobs.append(parsed_job)
        
        # 去重和排序
        final_jobs = deduplicate_and_sort(parsed_jobs)
        
        # 输出结果
        output = {"jobs": final_jobs}
        print(json.dumps(output, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"处理失败: {e}", file=sys.stderr)
        print(json.dumps({"jobs": []}, ensure_ascii=False))