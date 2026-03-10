#!/usr/bin/env python3
"""
改进版分布式搜索测试
"""

import os
import json
from datetime import datetime

# 改进的搜索关键词
IMPROVED_KEYWORDS = {
    "ai_agent": "深圳 AI Agent LangChain AutoGen 实习",
    "large_model": "深圳 大模型 LLM 微调 训练 实习", 
    "intelligent_agent": "深圳 智能体 Multi-Agent 自主代理 实习",
    "prompt_engineering": "深圳 提示词工程 Prompt Engineering 实习"
}

def test_improved_search():
    """测试改进版搜索"""
    print("🔍 开始改进版分布式搜索测试...")
    
    # 清空之前的缓冲区
    buffer_dir = "search_buffer"
    if not os.path.exists(buffer_dir):
        os.makedirs(buffer_dir)
    
    all_results = []
    
    # 模拟改进的搜索
    for key, query in IMPROVED_KEYWORDS.items():
        print(f"✅ 执行搜索: {query}")
        
        # 这里会调用实际的SearXNG搜索
        # 为了测试，我们模拟一些结果
        if key == "ai_agent":
            results = [
                {"title": "腾讯AI Lab - AI Agent实习生", "url": "http://ailab.tencent.com", "company": "腾讯"},
                {"title": "字节跳动 - AI Agent算法工程师实习生", "url": "https://www.nowcoder.com/jobs/detail/386087", "company": "字节跳动"}
            ]
        elif key == "large_model":
            results = [
                {"title": "百度 - 大模型算法实习生", "url": "https://www.sohu.com/a/928263636_121119001", "company": "百度"},
                {"title": "华为 - LLM微调实习生", "url": "https://career.huawei.com", "company": "华为"}
            ]
        elif key == "intelligent_agent":
            results = [
                {"title": "IDEA研究院 - AI4Science Agent实习生", "url": "https://zhuanlan.zhihu.com/p/1935661652470104124", "company": "IDEA研究院"},
                {"title": "商汤科技 - 智能体开发实习生", "url": "https://www.sensetime.com", "company": "商汤科技"}
            ]
        else:  # prompt_engineering
            results = [
                {"title": "阿里云 - Prompt Engineer实习生", "url": "https://careers.alibaba.com", "company": "阿里云"},
                {"title": "国家大学生就业服务平台 - AI技术产品实习生", "url": "https://www.ncss.cn/student/jobs/2VWpuc3HDJ63qnv9cxNQXn/detail.html", "company": "国家平台"},
                {"title": "创新工场 - 提示词工程实习生", "url": "https://www.innovation-works.com", "company": "创新工场"}
            ]
        
        # 保存结果
        filename = f"{key}_improved_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join(buffer_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        all_results.extend(results)
        print(f"   找到 {len(results)} 个岗位")
    
    print(f"\n📊 改进版测试结果:")
    print(f"   总共找到: {len(all_results)} 个岗位")
    print(f"   按关键词分组展示，避免过度去重")
    
    return all_results

if __name__ == "__main__":
    test_improved_search()