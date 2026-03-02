#!/usr/bin/env python3
"""
深圳AI Agent实习岗位推荐Skill
- 优化搜索策略
- 改进数据提取  
- 实现去重和过滤
- 生成表格格式报告
"""

import json
import subprocess
import time
import re
from datetime import datetime

class ShenzhenAIAgentInternSkill:
    def __init__(self):
        self.search_queries = [
            # 精确的招聘网站定向搜索
            '"深圳 AI Agent 实习" site:zhipin.com',
            '"深圳 智能体开发 实习" site:zhipin.com',
            '"深圳 大模型应用 实习" site:lagou.com', 
            '"深圳 LangChain 实习" site:liepin.com',
            '"深圳 AutoGen 实习" site:shixiseng.com',
            '"深圳 RAG 实习" site:zhipin.com',
            '"深圳 Prompt Engineering 实习" site:lagou.com',
            # 通用搜索作为备用
            '深圳 "AI Agent" 实习',
            '深圳 "大模型" 实习',
            '深圳 "智能体" 实习'
        ]
        
        self.relevant_keywords = [
            'AI Agent', '智能体', '大模型', 'LangChain', 'AutoGen',
            'CrewAI', 'RAG', '检索增强', 'Prompt', '提示工程',
            'LLM', '大语言模型', '实习', '实习生'
        ]
        
        self.job_sites = [
            'zhipin.com', 'lagou.com', 'liepin.com', 'shixiseng.com',
            '51job.com', 'yingjiesheng.com', 'nowcoder.com'
        ]

    def execute_search(self, query):
        """执行SearXNG搜索"""
        try:
            result = subprocess.run([
                "python3", "/home/admin/.openclaw/workspace/scripts/searxng_search.py",
                query, "jobs", "zh", "8"
            ], capture_output=True, text=True, cwd="/home/admin/.openclaw/workspace")
            
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    return data.get('results', [])
                except json.JSONDecodeError:
                    print(f"JSON解析失败: {query}")
                    return []
            else:
                print(f"搜索失败 ({query})")
                return []
        except Exception as e:
            print(f"搜索异常 ({query}): {e}")
            return []

    def filter_relevant(self, results):
        """过滤相关结果"""
        filtered = []
        for result in results:
            title = result.get('title', '').lower()
            content = result.get('content', '').lower()
            url = result.get('url', '')
            
            # 检查关键词匹配
            keyword_match = any(kw.lower() in title or kw.lower() in content 
                              for kw in self.relevant_keywords)
            
            # 检查是否为招聘网站
            site_match = any(site in url for site in self.job_sites)
            
            if keyword_match or site_match:
                filtered.append(result)
        
        return filtered

    def extract_fields(self, result):
        """提取表格所需字段"""
        title = result.get('title', '未知职位')
        url = result.get('url', '#')
        content = result.get('content', '')
        
        # 提取公司名称（从标题或URL中推测）
        company = self.extract_company(title, url)
        
        # 提取工作地点
        location = self.extract_location(title, content)
        
        # 提取核心要求（内容前100字）
        requirements = content[:100] + "..." if len(content) > 100 else content
        
        return {
            'position': title,
            'company': company,
            'location': location,
            'requirements': requirements,
            'source': url
        }

    def extract_company(self, title, url):
        """从标题或URL提取公司名"""
        # 从BOSS直聘URL提取
        if 'zhipin.com' in url:
            match = re.search(r'www\.zhipin\.com/gongsi/([^/]+)', url)
            if match:
                return "BOSS直聘上的公司"
        
        # 从标题中提取（假设格式为"职位 - 公司"）
        if ' - ' in title:
            parts = title.split(' - ')
            if len(parts) >= 2:
                return parts[-1]
        
        # 从猎聘URL提取
        if 'liepin.com' in url:
            return "猎聘网上的公司"
            
        return "未知公司"

    def extract_location(self, title, content):
        """提取工作地点"""
        # 搜索深圳的具体区域
        shenzhen_areas = ['南山区', '福田区', '罗湖区', '宝安区', '龙岗区', '盐田区', '龙华区', '坪山区', '光明区']
        
        text = title + ' ' + content
        for area in shenzhen_areas:
            if area in text:
                return area
        
        # 如果没有具体区域，返回深圳
        if '深圳' in text:
            return '深圳'
        
        return '未知地点'

    def remove_duplicates(self, jobs):
        """基于职位+公司去重"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            key = f"{job['position']}|{job['company']}"
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs

    def generate_table(self, jobs):
        """生成Markdown表格"""
        if not jobs:
            return "暂无符合要求的深圳AI Agent实习岗位信息"
        
        table = "| 岗位名称 | 公司名称 | 工作地点 | 核心要求 | 投递方式/信息来源 |\n"
        table += "|---------|---------|---------|---------|------------------|\n"
        
        for job in jobs[:10]:  # 取前10个
            position = job['position'].replace('|', '\\|')
            company = job['company'].replace('|', '\\|')
            location = job['location'].replace('|', '\\|')
            requirements = job['requirements'].replace('|', '\\|').replace('\n', ' ')
            source = f"[链接]({job['source']})"
            
            table += f"| {position} | {company} | {location} | {requirements} | {source} |\n"
        
        return table

    def run(self):
        """执行完整的实习岗位推荐流程"""
        print("开始执行深圳AI Agent实习岗位推荐...")
        
        # 1. 优化搜索策略
        all_results = []
        for query in self.search_queries:
            print(f"搜索: {query}")
            results = self.execute_search(query)
            filtered = self.filter_relevant(results)
            all_results.extend(filtered)
            time.sleep(1)  # 避免请求过快
        
        # 2. 改进数据提取
        extracted_jobs = []
        for result in all_results:
            job = self.extract_fields(result)
            extracted_jobs.append(job)
        
        # 3. 去重和过滤
        unique_jobs = self.remove_duplicates(extracted_jobs)
        
        # 4. 生成表格报告
        table = self.generate_table(unique_jobs)
        
        # 5. 生成完整报告
        report = f"""# 🤖 深圳AI Agent实习岗位日报 - {datetime.now().strftime('%Y年%m月%d日')}

## 🔍 今日精选AI Agent相关实习岗位

> **专注领域**: AI Agent、智能体、大模型、LangChain、AutoGen、RAG、Prompt Engineering

{table}

---
由太太自动推送于 {datetime.now().strftime('%Y-%m-%d %H:%M')}
专注为你寻找最优质的AI Agent实习机会 💪
"""
        
        return report

if __name__ == "__main__":
    skill = ShenzhenAIAgentInternSkill()
    report = skill.run()
    print(report)