#!/usr/bin/env python3
"""
深圳AI Agent实习岗位链接推送（方案A）
- 使用SearXNG搜索相关关键词
- 返回最相关的招聘链接
- 不尝试解析详细字段，直接提供链接
"""

import json
import subprocess
import sys
import time
import re
from datetime import datetime

def execute_searxng_search(query, max_results=5):
    """执行SearXNG搜索（Python 3.8兼容版本）"""
    try:
        # 使用stdout/stderr分离的方式（兼容Python 3.8）
        process = subprocess.Popen([
            sys.executable, "scripts/searxng_search.py", 
            query, "jobs", "zh", str(max_results)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
        cwd="/home/admin/.openclaw/workspace", text=True)
        
        stdout, stderr = process.communicate(timeout=30)
        
        if process.returncode == 0:
            try:
                data = json.loads(stdout)
                return data.get('results', [])
            except json.JSONDecodeError as e:
                print(f"JSON解析失败: {e}")
                return []
        else:
            print(f"搜索失败 ({query}): {stderr}")
            return []
    except subprocess.TimeoutExpired:
        print(f"搜索超时 ({query})")
        return []
    except Exception as e:
        print(f"搜索异常 ({query}): {e}")
        return []

def is_relevant_job(result):
    """判断是否为相关的工作岗位"""
    title = result.get('title', '').lower()
    content = result.get('content', '').lower()
    url = result.get('url', '')
    
    # 相关关键词
    relevant_keywords = [
        'ai agent', '智能体', '大模型', 'langchain', 'autogen',
        'crewai', 'rag', '检索增强', 'prompt', '提示工程',
        'llm', '大语言模型', '实习', '实习生', 'intern'
    ]
    
    # 招聘网站域名
    job_sites = [
        'zhipin.com', 'lagou.com', 'liepin.com', 'shixiseng.com',
        '51job.com', 'yingjiesheng.com', 'nowcoder.com', 'indeed.com'
    ]
    
    # 检查关键词匹配
    has_keyword = any(keyword in title or keyword in content for keyword in relevant_keywords)
    
    # 检查是否为招聘网站
    is_job_site = any(site in url for site in job_sites)
    
    # 检查是否包含深圳
    has_shenzhen = '深圳' in title or '深圳' in content or 'shenzhen' in url.lower()
    
    return (has_keyword or is_job_site) and has_shenzhen

def search_ai_agent_jobs():
    """搜索AI Agent相关实习岗位"""
    # 搜索关键词
    queries = [
        '深圳 AI Agent 实习',
        '深圳 智能体开发 实习', 
        '深圳 大模型应用 实习',
        '深圳 LangChain 实习',
        '深圳 AutoGen 实习',
        '深圳 RAG 实习',
        '深圳 Prompt Engineering 实习',
        '深圳 LLM 应用 实习',
        '深圳 人工智能 实习',
        'AI Agent intern 深圳'
    ]
    
    all_results = []
    
    print("开始搜索深圳AI Agent实习岗位...")
    
    for query in queries:
        print(f"搜索: {query}")
        results = execute_searxng_search(query, 3)
        
        # 过滤相关结果
        relevant_results = [r for r in results if is_relevant_job(r)]
        all_results.extend(relevant_results)
        
        time.sleep(1)  # 避免请求过于频繁
    
    # 去重（基于URL）
    seen_urls = set()
    unique_results = []
    for result in all_results:
        url = result.get('url', '')
        clean_url = re.sub(r'\?.*$', '', url)  # 移除URL参数
        if clean_url not in seen_urls:
            seen_urls.add(clean_url)
            unique_results.append(result)
    
    return unique_results[:10]  # 返回前10个结果

def generate_markdown_report(results):
    """生成Markdown格式的报告"""
    current_date = datetime.now().strftime('%Y年%m月%d日')
    
    report = f"""# 🤖 深圳AI Agent实习岗位日报 - {current_date}

## 🔍 今日精选AI Agent相关实习岗位

> **专注领域**: AI Agent、智能体开发、大模型应用、Agent框架(LangChain/AutoGen/CrewAI)、RAG、Prompt Engineering

"""
    
    if results:
        for i, result in enumerate(results, 1):
            title = result.get('title', '无标题')
            url = result.get('url', '#')
            engine = result.get('engine', '未知来源')
            
            report += f"{i}. [{title}]({url})\n"
            report += f"   - **来源**: {engine}\n\n"
    else:
        report += "暂无符合要求的深圳AI Agent实习岗位信息\n\n"
        report += "**建议手动查看以下招聘网站**:\n"
        report += "- BOSS直聘 (https://www.zhipin.com)\n"
        report += "- 拉勾网 (https://www.lagou.com)\n"
        report += "- 猎聘 (https://www.liepin.com)\n"
        report += "- 实习僧 (https://www.shixiseng.com)\n\n"
    
    report += "---\n"
    report += f"由太太自动推送于 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    report += "专注为你寻找最优质的AI Agent实习机会 💪"
    
    return report

if __name__ == "__main__":
    results = search_ai_agent_jobs()
    report = generate_markdown_report(results)
    print(report)