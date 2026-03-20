#!/usr/bin/env python3
"""
AI潮玩周报搜索脚本 - 优化版
按优先级搜索AI潮玩新产品、AI硬件、其他信息
"""

import requests
import json
import datetime
import time

SEARXNG_URL = "http://localhost:8080/search"

def search_searxng(query, language="zh"):
    """使用SearXNG搜索"""
    try:
        params = {
            'q': query,
            'format': 'json',
            'language': language
        }
        response = requests.get(SEARXNG_URL, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"搜索失败: {e}")
        return None

def search_ai_toy_products():
    """优先级1：AI潮玩新产品和创新功能"""
    queries = [
        # 中文关键词
        "AI潮玩 新品 发布",
        "AI潮玩 创新功能",
        "智能潮玩 新上市",
        "AI玩具 新功能 情感交互",
        "AI毛绒玩具 陪伴",
        # 英文关键词
        "AI toy new product launch",
        "smart toy innovation",
        "robot companion new",
        "AI plush toy emotional",
        "interactive AI toy"
    ]
    
    results = []
    for query in queries:
        data = search_searxng(query)
        if data and 'results' in data:
            results.extend(data['results'])
        time.sleep(1)  # 避免请求过快
    
    return results

def search_ai_hardware():
    """优先级2：AI硬件和创新功能"""
    queries = [
        "AI芯片 玩具 新品",
        "边缘AI 硬件 模组",
        "AI加速器 低功耗",
        "语音芯片 玩具",
        "AI chip toy hardware",
        "edge AI module",
        "AI accelerator edge computing"
    ]
    
    results = []
    for query in queries:
        data = search_searxng(query)
        if data and 'results' in data:
            results.extend(data['results'])
        time.sleep(1)
    
    return results

def search_other_info():
    """优先级3：其他信息"""
    queries = [
        "AI潮玩 市场趋势",
        "AI玩具 投融资",
        "智能玩具 行业报告",
        "AI toy market trend",
        "AI toy investment"
    ]
    
    results = []
    for query in queries:
        data = search_searxng(query)
        if data and 'results' in data:
            results.extend(data['results'])
        time.sleep(1)
    
    return results

def filter_by_source(results):
    """按来源优先级筛选"""
    priority_sources = {
        'high': ['kickstarter.com', 'indiegogo.com', 'techcrunch.com', 'theverge.com', 'toybook.com'],
        'medium': ['36kr.com', 'itjuzi.com', 'iimedia.cn', 'sina.com.cn', 'qq.com'],
        'low': ['zhihu.com', 'csdn.net', 'github.com']
    }
    
    filtered = {'high': [], 'medium': [], 'low': []}
    
    for result in results:
        url = result.get('url', '')
        for level, domains in priority_sources.items():
            if any(domain in url for domain in domains):
                filtered[level].append(result)
                break
        else:
            filtered['low'].append(result)
    
    # 按优先级合并
    return filtered['high'] + filtered['medium'] + filtered['low']

def deduplicate(results):
    """去重"""
    seen = set()
    unique = []
    for result in results:
        url = result.get('url', '')
        if url not in seen:
            seen.add(url)
            unique.append(result)
    return unique

def main():
    """主函数"""
    print("开始搜索AI潮玩资讯...")
    
    # 按优先级搜索
    print("\n[优先级1] 搜索AI潮玩新产品...")
    toy_results = search_ai_toy_products()
    
    print("\n[优先级2] 搜索AI硬件...")
    hardware_results = search_ai_hardware()
    
    print("\n[优先级3] 搜索其他信息...")
    other_results = search_other_info()
    
    # 合并结果
    all_results = toy_results + hardware_results + other_results
    
    # 去重
    all_results = deduplicate(all_results)
    
    # 按来源筛选
    filtered_results = filter_by_source(all_results)
    
    # 保存结果
    today = datetime.datetime.now().strftime("%Y%m%d")
    output_file = f"/home/admin/.openclaw/workspace/distributed_search/search_buffer/ai_toy_weekly_{today}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'date': today,
            'total_results': len(filtered_results),
            'toy_products': len(toy_results),
            'hardware': len(hardware_results),
            'other': len(other_results),
            'results': filtered_results[:20]  # 只保留前20条
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n搜索完成！共找到 {len(filtered_results)} 条结果")
    print(f"- AI潮玩产品: {len(toy_results)} 条")
    print(f"- AI硬件: {len(hardware_results)} 条")
    print(f"- 其他: {len(other_results)} 条")
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main()