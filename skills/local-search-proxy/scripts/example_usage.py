#!/usr/bin/env python3
"""
Local Search Proxy 使用示例
"""

from local_search import search, search_simple, search_with_summary

# 示例1: 基础搜索
print("=" * 50)
print("示例1: 基础搜索")
print("=" * 50)
result = search("AI Agent", max_results=3)
print(f"搜索关键词: {result['query']}")
print(f"总结果数: {result['total']}")
for item in result['results']:
    print(f"- {item['title']}: {item['url']}")

# 示例2: 简化搜索（仅URL）
print("\n" + "=" * 50)
print("示例2: 简化搜索（仅URL）")
print("=" * 50)
urls = search_simple("Python教程", max_results=3)
for url in urls:
    print(url)

# 示例3: 格式化摘要
print("\n" + "=" * 50)
print("示例3: 格式化摘要")
print("=" * 50)
summary = search_with_summary("大模型", max_results=2)
print(summary)
