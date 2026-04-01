#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深圳AI实习岗位日报汇总脚本
用于汇总分布式搜索的结果并生成Markdown格式日报
"""

import json
import os
from datetime import datetime, timedelta

# 配置
SEARCH_BUFFER_DIR = "/home/admin/.openclaw/workspace/distributed_search/search_buffer"
CATEGORIES = {
    "ai_agent": "AI Agent",
    "large_model": "大模型",
    "intelligent_agent": "智能体",
    "prompt": "提示词工程",
    "ai_product_manager": "AI产品经理"
}

def get_date_str(days_offset=0):
    """获取日期字符串"""
    date = datetime.now() + timedelta(days=days_offset)
    return date.strftime("%Y%m%d")

def read_json_file(filepath):
    """安全读取JSON文件"""
    try:
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"读取文件失败 {filepath}: {e}")
        return None

def filter_internship_jobs(jobs):
    """筛选实习和春招岗位"""
    filtered = []
    keywords = ["实习", "实习生", "春招", "校招", "2026届"]
    exclude_keywords = ["社招", "全职", "3年以上", "5年以上"]
    
    for job in jobs:
        title = job.get("title", "")
        # 必须包含实习/春招关键词
        if not any(kw in title for kw in keywords):
            continue
        # 排除社招
        if any(kw in title for kw in exclude_keywords):
            continue
        filtered.append(job)
    
    return filtered

def deduplicate_jobs(jobs_list):
    """根据URL去重"""
    seen_urls = set()
    unique_jobs = []
    
    for job in jobs_list:
        url = job.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_jobs.append(job)
    
    return unique_jobs

def get_company_type(company):
    """判断公司类型"""
    big_tech = ["字节", "腾讯", "阿里", "百度", "华为", "美团", "京东", "小米", 
                "OPPO", "vivo", "快手", "滴滴", "网易", "拼多多", "深信服"]
    unicorn = ["智谱", "月之暗面", "MiniMax", "零一万物", "百川", "面壁", "阶跃"]
    
    for name in big_tech:
        if name in company:
            return "[大厂]"
    for name in unicorn:
        if name in company:
            return "[独角兽]"
    return "[创业公司]"

def get_job_type(title):
    """判断岗位类型"""
    if "实习" in title or "实习生" in title:
        return "[实习]"
    elif "春招" in title or "校招" in title or "2026届" in title:
        return "[春招]"
    return "[校招]"

def generate_report():
    """生成日报"""
    today = get_date_str()
    yesterday = get_date_str(-1)
    
    all_jobs = []
    category_stats = {}
    
    # 读取各分类数据
    for key, name in CATEGORIES.items():
        # 尝试今天的文件
        filepath = os.path.join(SEARCH_BUFFER_DIR, f"{key}_{today}.json")
        data = read_json_file(filepath)
        
        # 如果今天没有，尝试昨天的文件
        if not data:
            filepath = os.path.join(SEARCH_BUFFER_DIR, f"{key}_{yesterday}.json")
            data = read_json_file(filepath)
        
        if data and "jobs" in data:
            jobs = filter_internship_jobs(data["jobs"])
            category_stats[name] = len(jobs)
            for job in jobs:
                job["category"] = name
            all_jobs.extend(jobs)
        else:
            category_stats[name] = 0
    
    # 去重
    all_jobs = deduplicate_jobs(all_jobs)
    
    # 按公司类型排序（大厂优先）
    all_jobs.sort(key=lambda x: (
        0 if get_company_type(x.get("company", "")) == "[大厂]" else
        1 if get_company_type(x.get("company", "")) == "[独角兽]" else 2
    ))
    
    # 生成Markdown报告
    report_date = datetime.now().strftime("%Y年%m月%d日")
    report = f"""# 🎯 深圳AI实习岗位日报 | {report_date}

> 📊 数据来源：分布式搜索（AI Agent / 大模型 / 智能体 / 提示词工程 / AI产品经理）
> ⏰ 更新时间：{datetime.now().strftime("%H:%M")}

---

## 📈 今日概览

| 分类 | 岗位数量 |
|------|----------|
"""
    
    for name, count in category_stats.items():
        report += f"| {name} | {count}个 |\n"
    
    report += f"| **总计** | **{len(all_jobs)}个** |\n\n"
    
    if not all_jobs:
        report += """---

⚠️ **今日暂无新岗位**

可能原因：
- 分布式搜索任务尚未完成
- 搜索缓冲区文件缺失
- 当日确实无新增岗位

建议稍后再次查看或检查搜索任务状态。
"""
        return report
    
    report += """---

## 💼 精选岗位

"""
    
    # 显示前20个岗位
    for i, job in enumerate(all_jobs[:20], 1):
        company = job.get("company", "未知公司")
        title = job.get("title", "未知岗位")
        job_type = get_job_type(title)
        company_type = get_company_type(company)
        url = job.get("url", "")
        description = job.get("description", "暂无描述")
        category = job.get("category", "")
        
        report += f"""### {i}. {company_type} {job_type} {title}

**公司**：{company}  
**分类**：{category}  
**链接**：{url}  
**简介**：{description[:150]}{'...' if len(description) > 150 else ''}

---

"""
    
    # 添加投递建议
    report += """## 📝 投递建议

### 简历优化
- 突出AI相关项目经验，特别是Agent开发、大模型应用等
- 量化成果（如"提升效率30%"、"服务1000+用户"）
- 技术栈明确（Python、LangChain、RAG等）

### 面试准备
- 熟悉常见AI Agent架构（ReAct、Plan-and-Solve等）
- 了解Prompt Engineering最佳实践
- 准备1-2个完整的项目案例（背景-方案-结果）

### 时间规划
- 大厂实习通常提前3-6个月开放申请
- 春招高峰期：3-5月
- 建议每周至少投递5-10个岗位

---

## 📚 学习资源

- [LangChain官方文档](https://python.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook)
- [吴恩达AI Agent课程](https://www.deeplearning.ai/short-courses/)

---

💡 **温馨提示**：岗位信息可能存在时效性问题，建议点击链接查看详情并尽快投递。

🎉 祝你求职顺利！有问题随时找我哦~
"""
    
    return report

if __name__ == "__main__":
    report = generate_report()
    print(report)
