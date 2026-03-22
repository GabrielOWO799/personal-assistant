#!/usr/bin/env python3
"""
AI潮玩周报搜索脚本 - v2.0 优化版
- 多搜索引擎备用
- 自动去重机制
- 历史对比避免重复
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
    """加载已报道过的产品历史"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'reported_products': [], 'reported_urls': []}

def save_history(history):
    """保存历史记录"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def is_duplicate(result, history):
    """检查是否已报道过"""
    url = result.get('url', '')
    title = result.get('title', '')
    
    # URL去重
    if url in history['reported_urls']:
        return True
    
    # 标题相似度检查（简单版本）
    title_keywords = set(re.findall(r'\w+', title.lower()))
    for reported_title in history['reported_products']:
        reported_keywords = set(re.findall(r'\w+', reported_title.lower()))
        # 如果关键词重叠度超过70%，认为是重复
        if len(title_keywords & reported_keywords) / max(len(title_keywords), 1) > 0.7:
            return True
    
    return False

def search_searxng(query, language="zh"):
    """使用SearXNG搜索"""
    try:
        params = {
            'q': query,
            'format': 'json',
            'language': language,
            'time_range': 'week'  # 只搜索过去一周
        }
        response = requests.get(SEARXNG_URL, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"SearXNG搜索失败: {e}")
        return None

def search_web_search(query):
    """使用web_search工具作为备用（模拟）"""
    # 这里会由cron任务中的agent调用web_search工具
    # 脚本本身不直接调用，而是在cron任务中处理
    return None

def search_ai_toy_products(history):
    """优先级1：AI潮玩新产品和创新功能"""
    queries = [
        # 中文关键词
        "AI潮玩 新品 Kickstarter",
        "AI潮玩 众筹 Indiegogo",
        "智能潮玩 发布 2026",
        "AI玩具 新功能 情感交互",
        "AI毛绒玩具 陪伴 上市",
        # 英文关键词
        "AI toy Kickstarter new",
        "smart toy Indiegogo launch",
        "robot companion 2026",
        "AI plush toy emotional",
        "interactive AI toy new"
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

def search_ai_hardware(history):
    """优先级2：AI硬件和创新功能"""
    queries = [
        "AI芯片 玩具 新品 2026",
        "边缘AI 硬件 模组 发布",
        "AI加速器 低功耗 玩具",
        "语音芯片 玩具 新品",
        "AI chip toy hardware new",
        "edge AI module 2026"
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

def search_other_info(history):
    """优先级3：其他信息"""
    queries = [
        "AI潮玩 市场趋势 2026",
        "AI玩具 投融资 新闻",
        "智能玩具 行业报告",
        "AI toy market trend",
        "AI toy investment funding"
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
        'high': ['kickstarter.com', 'indiegogo.com', 'techcrunch.com', 'theverge.com', 'toybook.com'],
        'medium': ['36kr.com', 'itjuzi.com', 'iimedia.cn', 'sina.com.cn', 'qq.com', 'sohu.com'],
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
    """去重"""
    seen = set()
    unique = []
    for result in results:
        url = result.get('url', '')
        if url not in seen:
            seen.add(url)
            unique.append(result)
    return unique

def extract_product_name(title):
    """从产品标题中提取产品名称"""
    # 简单的提取逻辑，可以根据需要优化
    return title.split('｜')[0].split('|')[0].strip()

def main():
    """主函数"""
    print("=" * 60)
    print("AI潮玩周报搜索脚本 v2.0")
    print("=" * 60)
    
    # 加载历史记录
    history = load_history()
    print(f"\n已加载历史记录: {len(history['reported_products'])} 个产品")
    
    # 按优先级搜索
    print("\n[优先级1] 搜索AI潮玩新产品...")
    toy_results = search_ai_toy_products(history)
    print(f"  找到 {len(toy_results)} 条新结果")
    
    print("\n[优先级2] 搜索AI硬件...")
    hardware_results = search_ai_hardware(history)
    print(f"  找到 {len(hardware_results)} 条新结果")
    
    print("\n[优先级3] 搜索其他信息...")
    other_results = search_other_info(history)
    print(f"  找到 {len(other_results)} 条新结果")
    
    # 合并结果
    all_results = toy_results + hardware_results + other_results
    
    # 去重
    all_results = deduplicate(all_results)
    
    # 按来源筛选
    filtered_results = filter_by_source(all_results)
    
    # 更新历史记录
    for result in filtered_results[:10]:  # 只记录前10条
        title = result.get('title', '')
        url = result.get('url', '')
        product_name = extract_product_name(title)
        if product_name and product_name not in history['reported_products']:
            history['reported_products'].append(product_name)
        if url and url not in history['reported_urls']:
            history['reported_urls'].append(url)
    
    # 保存历史记录（只保留最近100条）
    history['reported_products'] = history['reported_products'][-100:]
    history['reported_urls'] = history['reported_urls'][-100:]
    save_history(history)
    
    # 保存结果
    today = datetime.datetime.now().strftime("%Y%m%d")
    output_file = f"{SEARCH_BUFFER_DIR}/ai_toy_weekly_{today}.json"
    
    # 确保目录存在
    os.makedirs(SEARCH_BUFFER_DIR, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'date': today,
            'total_results': len(filtered_results),
            'toy_products': len(toy_results),
            'hardware': len(hardware_results),
            'other': len(other_results),
            'results': filtered_results[:20]
        }, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"搜索完成！")
    print(f"- 总结果: {len(filtered_results)} 条")
    print(f"- AI潮玩产品: {len(toy_results)} 条")
    print(f"- AI硬件: {len(hardware_results)} 条")
    print(f"- 其他: {len(other_results)} 条")
    print(f"- 新记录产品: {len([r for r in filtered_results[:10] if not is_duplicate(r, load_history())])} 个")
    print(f"结果已保存到: {output_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()