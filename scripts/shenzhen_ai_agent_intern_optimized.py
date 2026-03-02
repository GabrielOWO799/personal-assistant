#!/usr/bin/env python3
"""
深圳AI Agent实习岗位优化版搜集脚本
整合了优化搜索策略、改进数据提取、去重过滤功能
"""

import json
import sys
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 添加项目路径
sys.path.append('/home/admin/.openclaw/workspace/scripts')

try:
    from optimized_search_strategy import search_with_optimized_strategy
    from improved_data_extraction import extract_job_fields
    from deduplication_filter import deduplicate_and_filter_jobs
except ImportError as e:
    print(f"导入模块失败: {e}")
    sys.exit(1)

def main():
    """主函数：执行完整的深圳AI Agent实习岗位搜集流程"""
    print("=== 深圳AI Agent实习岗位优化版搜集开始 ===")
    
    # 1. 优化搜索策略
    print("步骤1: 执行优化搜索策略...")
    search_results = search_with_optimized_strategy()
    print(f"找到 {len(search_results)} 个原始搜索结果")
    
    # 2. 改进数据提取
    print("步骤2: 执行改进的数据提取...")
    extracted_jobs = []
    for result in search_results:
        try:
            job_info = extract_job_fields(result)
            if job_info and is_valid_job(job_info):
                extracted_jobs.append(job_info)
                print(f"成功提取岗位: {job_info.get('position', '未知')}")
        except Exception as e:
            print(f"提取岗位失败: {e}")
            continue
    
    print(f"成功提取 {len(extracted_jobs)} 个有效岗位")
    
    # 3. 去重和过滤
    print("步骤3: 执行去重和过滤...")
    filtered_jobs = deduplicate_and_filter_jobs(extracted_jobs)
    print(f"去重过滤后剩余 {len(filtered_jobs)} 个岗位")
    
    # 4. 生成报告
    print("步骤4: 生成最终报告...")
    report = generate_report(filtered_jobs)
    
    # 5. 保存报告
    output_file = f"/tmp/shenzhen_ai_agent_intern_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"报告已保存到: {output_file}")
    print("=== 深圳AI Agent实习岗位优化版搜集完成 ===")
    
    # 输出报告内容
    print("\n=== 生成的报告 ===")
    print(report)

def is_valid_job(job_info: Dict) -> bool:
    """验证岗位信息是否有效"""
    required_fields = ['position', 'company', 'location', 'requirements', 'source']
    return all(job_info.get(field) for field in required_fields)

def generate_report(jobs: List[Dict]) -> str:
    """生成Markdown格式的报告"""
    if not jobs:
        return """# 🤖 深圳AI Agent实习岗位日报

## 🔍 RSS源自动搜集结果

> **专注领域**: AI Agent、智能体、大模型、LangChain、AutoGen、RAG

暂无符合要求的深圳AI Agent实习岗位信息

---
由太太自动推送于 {}
专注为你寻找最优质的AI Agent实习机会 💪""".format(datetime.now().strftime('%Y-%m-%d %H:%M'))
    
    # 限制最多10个岗位
    jobs = jobs[:10]
    
    report = """# 🤖 深圳AI Agent实习岗位日报

## 🔍 RSS源自动搜集结果

> **专注领域**: AI Agent、智能体、大模型、LangChain、AutoGen、RAG

| 岗位名称 | 公司名称 | 工作地点 | 核心要求 | 投递方式/信息来源 |
|---------|---------|---------|---------|------------------|
"""
    
    for job in jobs:
        position = job.get('position', '未知岗位')
        company = job.get('company', '未知公司')
        location = job.get('location', '深圳')
        requirements = job.get('requirements', '未提供具体要求')
        source = job.get('source', '#')
        
        # 确保核心要求不超过100字
        if len(requirements) > 100:
            requirements = requirements[:100] + "..."
        
        report += f"| {position} | {company} | {location} | {requirements} | [{source}]({source}) |\n"
    
    report += f"\n---\n由太太自动推送于 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n专注为你寻找最优质的AI Agent实习机会 💪"
    
    return report

if __name__ == "__main__":
    main()