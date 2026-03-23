#!/usr/bin/env python3
"""
AI硬件搜集脚本 - 周五21:00执行
搜索关键词：AI芯片、端侧AI模组、语音芯片、AI硬件供应链
"""

import requests
import json
import datetime
import time
import os
import re
from urllib.parse import urlparse

SEARXNG_URL = "http://localhost:8080/search"
SEARCH_BUFFER_DIR = "/home/admin/.openclaw/workspace/distributed_search/search_buffer"
HISTORY_FILE = "/home/admin/.openclaw/workspace/distributed_search/ai_toy_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'reported_products': [], 'reported_urls': []}

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def is_duplicate(result, history):
    url = result.get('url', '')
    title = result.get('title', '')
    
    if url in history['reported_urls']:
        return True
    
    title_keywords = set(re.findall(r'\w+', title.lower()))
    for reported_title in history['reported_products']:
        reported_keywords = set(re.findall(r'\w+', reported_title.lower()))
        if len(title_keywords & reported_keywords) / max(len(title_keywords), 1) > 0.7:
            return True
    
    return False

def search_searxng(query, time_range="month"):
    """搜索，优先一周，扩大到半年"""
    try:
        params = {
            'q': query,
            'format': 'json',
            'language': 'zh-CN',
            'time_range': time_range
        }
        response = requests.get(SEARXNG_URL, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                return data
            if time_range == "week":
                return search_searxng(query, "month")
            if time_range == "month":
                return search_searxng(query, "year")
        return None
    except Exception as e:
        print(f"搜索失败: {e}")
        return None

def search_ai_hardware(history):
    """AI硬件搜索"""
    queries = [
        "AI芯片 玩具 新品 2026",
        "端侧AI 模组 发布",
        "语音芯片 玩具 低功耗",
        "边缘AI 硬件 玩具",
        "AI加速器 玩具应用",
        "AI眼镜 芯片 新品",
        "神经网络处理器 玩具",
        "AIoT芯片 智能玩具",
        "RISC-V AI芯片 发布",
        "AI硬件 供应链 2026"
    ]
    
    results = []
    for query in queries:
        data = search_searxng(query)
        if data and 'results' in data:
            for result in data['results']:
                if not is_duplicate(result, history):
                    results.append(result)
        time.sleep(1)
    
    return results

def filter_by_source(results):
    """按来源优先级筛选"""
    priority_sources = {
        'high': ['36kr.com', 'itjuzi.com', 'iimedia.cn', 'techcrunch.com'],
        'medium': ['sina.com.cn', 'qq.com', 'sohu.com', '163.com', 'ifeng.com'],
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
    
    return filtered['high'] + filtered['medium'] + filtered['low']

def deduplicate(results):
    seen = set()
    unique = []
    for result in results:
        url = result.get('url', '')
        if url not in seen:
            seen.add(url)
            unique.append(result)
    return unique

def extract_product_name(title):
    return title.split('｜')[0].split('|')[0].strip()

def main():
    print("=" * 60)
    print("AI硬件搜集脚本 - 周五21:00执行")
    print("=" * 60)
    
    history = load_history()
    print(f"\n已加载历史记录: {len(history['reported_products'])} 个产品")
    
    print("\n[AI硬件] 搜索AI硬件新品...")
    results = search_ai_hardware(history)
    print(f"  找到 {len(results)} 条结果")
    
    # 去重
    results = deduplicate(results)
    
    # 按来源筛选
    filtered_results = filter_by_source(results)
    
    # 更新历史记录
    for result in filtered_results[:10]:
        title = result.get('title', '')
        url = result.get('url', '')
        product_name = extract_product_name(title)
        if product_name and product_name not in history['reported_products']:
            history['reported_products'].append(product_name)
        if url and url not in history['reported_urls']:
            history['reported_urls'].append(url)
    
    # 保存历史记录
    history['reported_products'] = history['reported_products'][-100:]
    history['reported_urls'] = history['reported_urls'][-100:]
    save_history(history)
    
    # 保存结果
    today = datetime.datetime.now().strftime("%Y%m%d")
    output_file = f"{SEARCH_BUFFER_DIR}/ai_hardware_{today}.json"
    
    os.makedirs(SEARCH_BUFFER_DIR, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'date': today,
            'category': 'AI硬件',
            'total_results': len(filtered_results),
            'results': filtered_results[:10]
        }, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"AI硬件搜集完成！")
    print(f"- 总结果: {len(filtered_results)} 条")
    print(f"- 保存前10条到: {output_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
