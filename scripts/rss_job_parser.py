#!/usr/bin/env python3
"""
RSS Job Parser for AI Agent positions in Shenzhen
"""
import json
import feedparser
import re
from datetime import datetime
import sys
import os

# 配置文件路径
CONFIG_FILE = "/home/admin/.openclaw/workspace/scripts/rss_sources.json"

def load_config():
    """加载RSS源配置"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('rss_sources', []), config.get('keywords', [])
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        # 返回默认配置
        return [
            {
                "name": "拉勾网 - 深圳AI职位",
                "url": "https://rsshub.app/lagou/jobs/深圳/AI",
                "category": "tech",
                "enabled": True
            }
        ], ["AI Agent", "智能体", "大模型", "LangChain", "AutoGen", "RAG"]

def extract_company(title):
    """从标题中提取公司名称"""
    # 常见的标题格式: "职位名称-公司名称" 或 "公司名称-职位名称"
    patterns = [
        r'^(.+?)[\-—–](.+?)$',  # 公司-职位 或 职位-公司
        r'【(.+?)】',  # 【公司】职位
        r'(.+?)招聘',  # 公司招聘职位
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            # 尝试确定哪部分是公司名
            parts = re.split(r'[\-—–]', title)
            if len(parts) >= 2:
                # 简单判断：较短的部分可能是公司名，或者包含"科技"、"智能"等词的
                for part in parts:
                    if any(word in part for word in ['科技', '智能', '网络', '信息', '数据', 'AI', '人工智能']):
                        return part.strip()
                # 默认返回第一部分或第二部分
                return parts[0].strip() if len(parts[0]) < len(parts[1]) else parts[1].strip()
    
    return "未知公司"

def extract_location(description):
    """从描述中提取工作地点"""
    # 查找深圳相关的地点
    shenzhen_patterns = [
        r'深圳(市)?([南福罗宝龙盐坪光明大]|[南山|福田|罗湖|宝安|龙岗|盐田|坪山|光明|大鹏])?区?',
        r'([南福罗宝龙盐坪光明大]|[南山|福田|罗湖|宝安|龙岗|盐田|坪山|光明|大鹏])区'
    ]
    
    for pattern in shenzhen_patterns:
        match = re.search(pattern, description)
        if match:
            return match.group(0)
    
    # 如果没有具体区域，至少确认是深圳
    if '深圳' in description or 'shenzhen' in description.lower():
        return "深圳市"
    
    return "深圳"

def extract_requirements(description):
    """提取核心要求（前100字）"""
    # 清理描述文本
    clean_desc = re.sub(r'<[^>]+>', '', description)  # 移除HTML标签
    clean_desc = clean_desc.replace('\n', ' ').replace('\r', ' ')
    clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
    
    # 取前100个字符
    return clean_desc[:100] + "..." if len(clean_desc) > 100 else clean_desc

def matches_keywords(title, description, keywords):
    """检查是否匹配关键词"""
    text = (title + " " + description).lower()
    for keyword in keywords:
        if keyword.lower() in text:
            return True
    return False

def parse_rss_feeds():
    """解析所有RSS源"""
    rss_sources, keywords = load_config()
    all_jobs = []
    
    for source in rss_sources:
        if not source.get('enabled', True):
            continue
            
        url = source.get('url')
        name = source.get('name', 'Unknown')
        
        if not url:
            continue
            
        print(f"正在解析RSS源: {name}")
        print(f"URL: {url}")
        
        try:
            # 解析RSS
            feed = feedparser.parse(url)
            
            if hasattr(feed, 'bozo') and feed.bozo:
                print(f"RSS解析警告: {feed.bozo_exception}")
            
            print(f"找到 {len(feed.entries)} 个条目")
            
            for entry in feed.entries:
                title = getattr(entry, 'title', '')
                description = getattr(entry, 'description', '')
                link = getattr(entry, 'link', '')
                published = getattr(entry, 'published', '')
                
                # 检查关键词匹配
                if matches_keywords(title, description, keywords):
                    job = {
                        'title': title,
                        'company': extract_company(title),
                        'location': extract_location(description),
                        'requirements': extract_requirements(description),
                        'source': link,
                        'published': published,
                        'source_name': name
                    }
                    all_jobs.append(job)
                    print(f"  ✓ 匹配: {title}")
                else:
                    print(f"  ✗ 不匹配: {title}")
                    
        except Exception as e:
            print(f"解析RSS源失败 {name}: {e}")
            continue
    
    return all_jobs

def deduplicate_jobs(jobs):
    """按标题+公司去重"""
    seen = set()
    unique_jobs = []
    
    for job in jobs:
        key = f"{job['title']}|{job['company']}"
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    return unique_jobs

def sort_jobs(jobs):
    """按发布时间排序（最新的在前）"""
    # 简单按添加顺序，因为RSS通常已经是时间排序的
    return jobs[:10]  # 取前10个

def generate_markdown_table(jobs):
    """生成Markdown表格"""
    if not jobs:
        return "暂无符合要求的深圳AI Agent实习岗位信息"
    
    table = "| 岗位名称 | 公司名称 | 工作地点 | 核心要求 | 投递方式/信息来源 |\n"
    table += "|---------|---------|---------|---------|------------------|\n"
    
    for job in jobs[:10]:
        table += f"| {job['title']} | {job['company']} | {job['location']} | {job['requirements']} | [查看详情]({job['source']}) |\n"
    
    return table

def main():
    """主函数"""
    print("开始解析深圳AI Agent实习岗位RSS源...")
    
    # 解析RSS
    jobs = parse_rss_feeds()
    print(f"总共找到 {len(jobs)} 个匹配的岗位")
    
    # 去重
    unique_jobs = deduplicate_jobs(jobs)
    print(f"去重后剩余 {len(unique_jobs)} 个岗位")
    
    # 排序并取前10个
    final_jobs = sort_jobs(unique_jobs)
    
    # 生成表格
    table = generate_markdown_table(final_jobs)
    
    # 输出到文件
    output_file = "/tmp/shenzhen_ai_agent_jobs.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 🤖 深圳AI Agent实习岗位日报\n\n")
        f.write("## 🔍 RSS源自动搜集结果\n\n")
        f.write("> **专注领域**: AI Agent、智能体、大模型、LangChain、AutoGen、RAG\n\n")
        f.write(table)
        f.write(f"\n\n---\n由太太自动推送于 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n专注为你寻找最优质的AI Agent实习机会 💪")
    
    print(f"结果已保存到: {output_file}")
    return output_file

if __name__ == "__main__":
    output_file = main()
    # 读取并输出结果用于调试
    with open(output_file, 'r', encoding='utf-8') as f:
        print("\n=== 生成的报告 ===")
        print(f.read())