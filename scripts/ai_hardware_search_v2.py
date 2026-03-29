#!/usr/bin/env python3
"""
AI硬件搜索脚本V2 - 优化版
时间范围：优先一周 → 一个月 → 半年
专注：具体产品 + 具体新技术
"""

import subprocess
import json
import os
from datetime import datetime

# 搜索配置
CATEGORY = "AI硬件"
TIME_RANGES = ["week", "month", "year"]
OUTPUT_DIR = "/home/admin/.openclaw/workspace/distributed_search/search_buffer"

# 关键词列表 - 聚焦具体产品和技术
KEYWORDS = [
    "AI硬件 新品发布 2026",
    "AI芯片 上市",
    "AI眼镜 发布",
    "AI机器人 开售",
    "端侧AI芯片 推出",
    "AI硬件 技术突破",
    "AI模组 发布",
    "AI算力芯片 新品",
    "AI硬件 CES 2026",
    "AI推理芯片 上市"
]

def search_searxng(keyword, time_range):
    """使用SearXNG搜索"""
    try:
        cmd = [
            "curl", "-s", "-m", "30",
            f"http://localhost:8080/search?q={keyword}&format=json&time_range={time_range}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
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
        product_keywords = ["新品", "发布", "上市", "推出", "众筹", "预售", "开售", "量产"]
        # 技术关键词
        tech_keywords = ["芯片", "算力", "模型", "推理", "训练", "端侧", "云端", "架构", "工艺"]
        
        has_product = any(k in title or k in content for k in product_keywords)
        has_tech = any(k in title or k in content for k in tech_keywords)
        
        if has_product or has_tech:
            r["priority"] = "high" if (has_product and has_tech) else "medium"
            filtered.append(r)
    
    return filtered

def main():
    today = datetime.now().strftime("%Y%m%d")
    all_results = []
    
    print(f"=== {CATEGORY}搜索开始 ===")
    
    for keyword in KEYWORDS:
        print(f"\n搜索关键词: {keyword}")
        keyword_results = []
        
        for time_range in TIME_RANGES:
            print(f"  尝试 {time_range}...", end=" ")
            results = search_searxng(keyword, time_range)
            
            if results:
                print(f"找到 {len(results)} 条")
                for r in results:
                    r["time_range"] = time_range
                keyword_results.extend(results)
                break
            else:
                print("无结果")
        
        all_results.extend(keyword_results)
    
    print(f"\n原始结果总数: {len(all_results)}")
    
    filtered = filter_product_tech(all_results)
    print(f"过滤后结果数: {len(filtered)}")
    
    # 去重
    seen_urls = set()
    unique_results = []
    for r in filtered:
        url = r.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(r)
    
    print(f"去重后结果数: {len(unique_results)}")
    
    # 排序并取前10
    unique_results.sort(key=lambda x: x.get("priority", "low"), reverse=True)
    final_results = unique_results[:10]
    print(f"最终选取: {len(final_results)} 条")
    
    # 保存
    output_file = os.path.join(OUTPUT_DIR, f"ai_hardware_{today}_v2.json")
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
