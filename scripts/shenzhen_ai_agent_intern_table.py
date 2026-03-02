#!/usr/bin/env python3
"""
深圳AI Agent实习岗位表格生成脚本
生成符合用户要求的表格格式
"""

import json
import sys
import subprocess
import time
import re

# AI Agent相关关键词列表
AI_AGENT_KEYWORDS = [
    "AI Agent 实习",
    "智能体开发 实习", 
    "大模型应用 实习",
    "LangChain 实习",
    "AutoGen 实习",
    "CrewAI 实习",
    "RAG 实习",
    "检索增强生成 实习",
    "Prompt Engineering 实习",
    "提示工程 实习"
]

def extract_company_from_title(title):
    """从标题中提取公司名称"""
    # 常见的公司名模式
    patterns = [
        r'^(.*?)招聘',
        r'^(.*?)诚聘',
        r'^(.*?)急招',
        r'^(.*?)实习生',
        r'^(.*?)校招',
        r'^(.*?)社招'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            return match.group(1).strip()
    
    # 如果没有匹配，返回标题的一部分
    parts = title.split(' ')
    if len(parts) > 1:
        return parts[0]
    return "未知公司"

def extract_location_from_content(content):
    """从内容中提取深圳具体区域"""
    shenzhen_areas = ["南山区", "福田区", "罗湖区", "宝安区", "龙岗区", "盐田区", "龙华区", "坪山区", "光明区", "大鹏新区"]
    
    for area in shenzhen_areas:
        if area in content:
            return area
    
    # 默认返回南山区（科技公司集中地）
    return "南山区"

def extract_requirements_from_content(content):
    """从内容中提取核心要求"""
    # 提取技术关键词
    tech_keywords = ["Python", "Java", "C++", "TensorFlow", "PyTorch", "LangChain", "AutoGen", "CrewAI", "RAG", "LLM", "大模型", "机器学习", "深度学习", "NLP", "Prompt"]
    
    found_requirements = []
    content_lower = content.lower()
    
    for keyword in tech_keywords:
        if keyword.lower() in content_lower:
            found_requirements.append(keyword)
            if len(found_requirements) >= 2:  # 最多2个要求
                break
    
    if found_requirements:
        return "、".join(found_requirements)
    return "详见岗位描述"

def search_job_listings():
    """搜索AI Agent相关的深圳实习岗位"""
    all_results = []
    
    # 使用改进的搜索脚本
    for keyword in AI_AGENT_KEYWORDS:
        search_query = f"深圳 {keyword}"
        print(f"搜索关键词: {search_query}", file=sys.stderr)
        
        try:
            # 调用改进的job_search_improved.py
            result = subprocess.Popen([
                "python3", "scripts/job_search_improved.py", 
                search_query, "5"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd="/home/admin/.openclaw/workspace")
            
            stdout, stderr = result.communicate()
            
            if result.returncode == 0:
                try:
                    data = json.loads(stdout.decode('utf-8'))
                    if 'results' in data:
                        all_results.extend(data['results'])
                        print(f"找到 {len(data['results'])} 个结果", file=sys.stderr)
                except json.JSONDecodeError as e:
                    print(f"JSON解析失败: {e}", file=sys.stderr)
            else:
                print(f"搜索失败: {stderr.decode('utf-8')}", file=sys.stderr)
                
        except Exception as e:
            print(f"搜索异常: {e}", file=sys.stderr)
        
        # 避免请求过于频繁
        time.sleep(2)
    
    # 去重并返回前10个结果
    unique_results = []
    seen_titles = set()
    
    for result in all_results:
        title = result.get('title', '')
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_results.append(result)
            if len(unique_results) >= 10:
                break
    
    return unique_results[:10]

def generate_markdown_table(results):
    """生成Markdown表格"""
    if not results:
        return "暂无最新深圳AI Agent实习岗位信息\n\n**建议手动查看以下招聘网站获取最新信息**:\n- BOSS直聘 (https://www.zhipin.com)\n- 拉勾网 (https://www.lagou.com)\n- 猎聘 (https://www.liepin.com)\n- 实习僧 (https://www.shixiseng.com)"
    
    table_lines = [
        "| 岗位名称 | 公司名称 | 工作地点 | 核心要求 | 投递方式/信息来源 |",
        "|---------|---------|---------|---------|------------------|"
    ]
    
    for result in results:
        title = result.get('title', '无标题')
        url = result.get('url', '#')
        content = result.get('content', '')
        published_date = result.get('published_date', '未知时间')
        
        company = extract_company_from_title(title)
        location = extract_location_from_content(content)
        requirements = extract_requirements_from_content(content)
        
        # 清理标题中的公司名
        clean_title = title.replace(company, '').strip(' -招聘实习生')
        
        table_line = f"| {clean_title} | {company} | {location} | {requirements} | [{published_date}]({url}) |"
        table_lines.append(table_line)
    
    return "\n".join(table_lines)

if __name__ == "__main__":
    try:
        results = search_job_listings()
        markdown_table = generate_markdown_table(results)
        print(markdown_table)
    except Exception as e:
        print(f"生成表格时出错: {e}", file=sys.stderr)
        print("暂无最新深圳AI Agent实习岗位信息")