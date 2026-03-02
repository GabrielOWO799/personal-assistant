#!/usr/bin/env python3
"""
AI Agent实习岗位关键词搜索脚本
专注于深圳地区的AI Agent相关实习岗位
"""

import json
import sys
import subprocess
import time

# AI Agent相关关键词列表
AI_AGENT_KEYWORDS = [
    "AI Agent",
    "智能体开发", 
    "大模型应用",
    "LangChain",
    "AutoGen",
    "CrewAI",
    "RAG",
    "检索增强生成",
    "Prompt Engineering",
    "提示工程",
    "Agent框架",
    "多智能体",
    "LLM应用",
    "大语言模型"
]

def search_ai_agent_internships():
    """搜索AI Agent相关的深圳实习岗位"""
    all_results = []
    
    # 逐个搜索关键词
    for keyword in AI_AGENT_KEYWORDS:
        search_query = f"深圳 {keyword} 实习"
        print(f"搜索关键词: {search_query}")
        
        try:
            # 调用searxng_search.py
            result = subprocess.run([
                "python3", "scripts/searxng_search.py", 
                search_query, "jobs", "zh", "5"
            ], capture_output=True, text=True, cwd="/home/admin/.openclaw/workspace")
            
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    if 'results' in data:
                        all_results.extend(data['results'])
                        print(f"找到 {len(data['results'])} 个结果")
                except json.JSONDecodeError:
                    print("JSON解析失败")
            else:
                print(f"搜索失败: {result.stderr}")
                
        except Exception as e:
            print(f"搜索异常: {e}")
        
        # 避免请求过于频繁
        time.sleep(1)
    
    # 去重并返回前10个结果
    unique_results = []
    seen_titles = set()
    
    for result in all_results:
        title = result.get('title', '')
        if title not in seen_titles:
            seen_titles.add(title)
            unique_results.append(result)
            if len(unique_results) >= 10:
                break
    
    return unique_results[:10]

if __name__ == "__main__":
    results = search_ai_agent_internships()
    
    # 输出为JSON格式
    output = {"results": results}
    print(json.dumps(output, ensure_ascii=False, indent=2))