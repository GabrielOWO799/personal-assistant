#!/usr/bin/env python3
"""
AI潮玩搜索脚本V2 - 优化版
时间范围：优先一周 → 一个月 → 半年
专注：具体产品 + 具体新技术
"""

import subprocess
import json
import os
import urllib.parse
from datetime import datetime

# 搜索配置
CATEGORY = "AI潮玩"
TIME_RANGES = ["week", "month", "year"]  # searxng的time_range参数
OUTPUT_DIR = "/home/admin/.openclaw/workspace/distributed_search/search_buffer"

# 关键词列表 - 聚焦具体产品和技术
KEYWORDS = [
    "AI潮玩新产品 2026",
    "AI陪伴机器人 发布",
    "智能玩具 新品",
    "AI玩具 技术突破",
    "情感陪伴 AI硬件",
    "多模态 AI玩具",
    "AI眼镜 新品发布",
    "具身智能 机器人",
    "AI硬件 CES 2026",
    "儿童AI玩具 上市"
]

def search_searxng(keyword, time_range):
    """使用SearXNG搜索"""
    try:
        encoded_keyword = urllib.parse.quote(keyword)
        cmd = [
            "curl", "-s", "-m", "30",
            f"http://localhost:8080/search?q={encoded_keyword}&format=json&time_range={time_range}"
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=35)
        stdout = result.stdout.decode('utf-8') if result.stdout else ""
        if result.returncode == 0 and stdout:
            data = json.loads(stdout)
            return data.get("results", [])
    except Exception as e:
        print(f"搜索失败 {keyword} {time_range}: {e}")
    return []

def filter_product_tech(results):
    """过滤出包含具体产品和技术的内容"""
    filtered = []
    for r in results:
        title = r.get("title", "").lower()
        content = r.get("content", "").lower()
        
        # 产品关键词
        product_keywords = ["新品", "发布", "上市", "推出", "众筹", "预售", "开售"]
        # 技术关键词
        tech_keywords = ["技术", "芯片", "模型", "算法", "交互", "多模态", "端侧", "大模型"]
        
        has_product = any(k in title or k in content for k in product_keywords)
        has_tech = any(k in title or k in content for k in tech_keywords)
        
        # 优先选择同时包含产品和技术信息的内容
        if has_product or has_tech:
            r["priority"] = "high" if (has_product and has_tech) else "medium"
            filtered.append(r)
    
    return filtered

def main():
    today = datetime.now().strftime("%Y%m%d")
    all_results = []
    
    print(f"=== {CATEGORY}搜索开始 ===")
    print(f"时间范围策略: 优先一周 → 一个月 → 半年")
    print(f"搜索关键词数: {len(KEYWORDS)}")
    
    for keyword in KEYWORDS:
        print(f"\n搜索关键词: {keyword}")
        keyword_results = []
        
        # 按时间范围优先级搜索
        for time_range in TIME_RANGES:
            print(f"  尝试 {time_range}...", end=" ")
            results = search_searxng(keyword, time_range)
            
            if results:
                print(f"找到 {len(results)} 条")
                # 标记时间范围
                for r in results:
                    r["time_range"] = time_range
                keyword_results.extend(results)
                break  # 找到结果就停止
            else:
                print("无结果")
        
        all_results.extend(keyword_results)
    
    print(f"\n原始结果总数: {len(all_results)}")
    
    # 过滤产品和技术内容
    filtered = filter_product_tech(all_results)
    print(f"过滤后结果数: {len(filtered)}")
    
    # 去重（按URL）
    seen_urls = set()
    unique_results = []
    for r in filtered:
        url = r.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(r)
    
    print(f"去重后结果数: {len(unique_results)}")
    
    # 按优先级排序
    unique_results.sort(key=lambda x: x.get("priority", "low"), reverse=True)
    
    # 取前10条
    final_results = unique_results[:10]
    print(f"最终选取: {len(final_results)} 条")
    
    # 保存结果
    output_file = os.path.join(OUTPUT_DIR, f"ai_chaowan_{today}_v2.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "date": today,
            "category": CATEGORY,
            "version": "v2",
            "strategy": "week_month_year",
            "focus": "product_tech",
            "total_results": len(all_results),
            "filtered_results": len(filtered),
            "unique_results": len(unique_results),
            "final_results": len(final_results),
            "results": final_results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存: {output_file}")
    print(f"=== {CATEGORY}搜索完成 ===")

if __name__ == "__main__":
    main()
