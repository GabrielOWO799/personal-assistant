#!/usr/bin/env python3
"""
改进的数据提取和解析
- 从搜索结果中提取公司名称、工作地点、核心要求等字段
- 针对不同招聘网站进行专门解析
- 处理各种格式的职位信息
"""

import re
import json
from urllib.parse import urlparse

def extract_company_name(title, url, content):
    """提取公司名称"""
    # 从URL中提取公司名
    domain = urlparse(url).netloc.lower()
    
    # 特定网站的公司名提取规则
    if 'zhipin.com' in domain:
        # BOSS直聘格式：职位名称-公司名称
        match = re.search(r'-\s*([^\-]+)$', title)
        if match:
            return match.group(1).strip()
    elif 'lagou.com' in domain:
        # 拉勾网格式：通常在标题前半部分
        match = re.search(r'^([^\-]+)\s*[-\u2014]', title)
        if match:
            return match.group(1).strip()
    elif 'liepin.com' in domain:
        # 猎聘格式：公司名称 - 职位
        match = re.search(r'^([^\-]+)\s*[-\u2014]', title)
        if match:
            return match.group(1).strip()
    
    # 通用规则：从内容中提取
    company_patterns = [
        r'公司[:：]\s*([^\n\r]+)',
        r'企业[:：]\s*([^\n\r]+)',
        r'雇主[:：]\s*([^\n\r]+)',
        r'([\u4e00-\u9fff]+(?:科技|网络|信息|智能|数据|软件|系统|电子|通信|互联网))'
    ]
    
    for pattern in company_patterns:
        match = re.search(pattern, content)
        if match:
            company = match.group(1).strip()
            # 过滤掉太短或太长的公司名
            if 2 <= len(company) <= 20:
                return company
    
    # 如果无法提取，返回"未知公司"
    return "未知公司"

def extract_location(title, content):
    """提取工作地点"""
    # 优先从标题中提取
    location_patterns = [
        r'深圳[^\u4e00-\u9fff]*([^\s\-]+)',  # 深圳后面跟着区名
        r'([^\s\-]+)深圳',  # 区名在深圳前面
        r'深圳\s*([^\s\-]+区)',  # 明确包含"区"字
        r'工作地点[:：]\s*([^\n\r]+)',
        r'地点[:：]\s*([^\n\r]+)'
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, title + ' ' + content)
        if match:
            location = match.group(1).strip()
            # 标准化深圳区域
            shenzhen_districts = ['南山', '福田', '罗湖', '宝安', '龙岗', '龙华', '盐田', '光明', '坪山', '大鹏']
            for district in shenzhen_districts:
                if district in location:
                    return f"深圳{district}区"
            
            # 如果没有具体区，至少返回深圳
            if '深圳' in location:
                return location
            else:
                return f"深圳{location}"
    
    # 默认返回深圳
    return "深圳"

def extract_core_requirements(content):
    """提取核心要求（前100字）"""
    # 清理内容，移除无关信息
    clean_content = re.sub(r'\s+', ' ', content)
    
    # 提取技术相关的要求
    tech_keywords = [
        'Python', 'Java', 'C++', 'JavaScript', 'Go', 'Rust',
        'LangChain', 'AutoGen', 'CrewAI', 'RAG', 'LLM',
        '大模型', '智能体', 'AI', '机器学习', '深度学习',
        'Prompt', '向量数据库', 'Redis', 'MySQL', 'MongoDB'
    ]
    
    # 查找包含技术关键词的句子
    sentences = re.split(r'[。！？\n]', clean_content)
    relevant_sentences = []
    
    for sentence in sentences:
        if any(keyword in sentence for keyword in tech_keywords):
            relevant_sentences.append(sentence.strip())
    
    if relevant_sentences:
        # 返回前100字
        combined = ' '.join(relevant_sentences)
        return combined[:100] + ('...' if len(combined) > 100 else '')
    
    # 如果没有找到技术相关句子，返回内容前100字
    return clean_content[:100] + ('...' if len(clean_content) > 100 else '')

def extract_job_title(title, content):
    """提取岗位名称"""
    # 清理标题
    clean_title = title.strip()
    
    # 移除公司名称（如果存在）
    patterns_to_remove = [
        r'\s*-\s*[^\-]+$',  # 移除 - 公司名
        r'\s*\u2014\s*[^\u2014]+$',  # 移除 — 公司名
        r'\s+[\u4e00-\u9fff]+(?:科技|网络|信息|智能|数据|软件|系统|电子|通信|互联网).*$',  # 移除公司名
    ]
    
    for pattern in patterns_to_remove:
        clean_title = re.sub(pattern, '', clean_title)
    
    # 如果清理后标题太短，从内容中提取
    if len(clean_title) < 3:
        job_patterns = [
            r'职位[:：]\s*([^\n\r]+)',
            r'岗位[:：]\s*([^\n\r]+)',
            r'招聘[:：]\s*([^\n\r]+)',
            r'((?:AI|人工智能|大模型|智能体|Agent|工程师|开发|算法|实习生?)[^\n\r]{5,30})'
        ]
        
        for pattern in job_patterns:
            match = re.search(pattern, content)
            if match:
                extracted = match.group(1).strip()
                if len(extracted) >= 3:
                    return extracted
    
    return clean_title if clean_title else "未知岗位"

def parse_job_listing(job_result):
    """解析单个职位信息"""
    title = job_result.get('title', '')
    url = job_result.get('url', '')
    content = job_result.get('content', '')
    
    parsed_job = {
        'position': extract_job_title(title, content),
        'company': extract_company_name(title, url, content),
        'location': extract_location(title, content),
        'requirements': extract_core_requirements(content),
        'source': url
    }
    
    return parsed_job

def batch_parse_jobs(job_results):
    """批量解析职位信息"""
    parsed_jobs = []
    
    for job_result in job_results:
        try:
            parsed_job = parse_job_listing(job_result)
            # 验证必要字段
            if parsed_job['position'] != '未知岗位' and parsed_job['company'] != '未知公司':
                parsed_jobs.append(parsed_job)
        except Exception as e:
            print(f"解析职位时出错: {e}")
            continue
    
    return parsed_jobs