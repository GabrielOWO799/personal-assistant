#!/usr/bin/env python3
"""
Local Search Proxy
通过exec调用本地SearXNG实例进行搜索
"""

import subprocess
import json
import argparse
import sys
from typing import List, Dict, Optional

# 配置
SEARXNG_URL = "http://localhost:8080"
DEFAULT_ENGINES = "google,bing,duckduckgo"
DEFAULT_TIMEOUT = 30


def search(
    query: str,
    max_results: int = 10,
    engines: str = DEFAULT_ENGINES,
    timeout: int = DEFAULT_TIMEOUT
) -> Dict:
    """
    使用本地SearXNG进行搜索
    
    Args:
        query: 搜索关键词
        max_results: 最大返回结果数
        engines: 搜索引擎（逗号分隔）
        timeout: 超时时间（秒）
    
    Returns:
        搜索结果字典
    """
    if not query or not query.strip():
        return {
            "query": "",
            "total": 0,
            "results": [],
            "error": "搜索关键词不能为空"
        }
    
    # 构建curl命令
    encoded_query = query.replace("'", "'\"'\"'").replace(" ", "+")
    cmd = (
        f"curl -s --max-time {timeout} "
        f"'{SEARXNG_URL}/search?q={encoded_query}&format=json&engines={engines}'"
    )
    
    try:
        # 执行命令
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout + 5
        )
        
        stderr = result.stderr.decode('utf-8') if result.stderr else ''
        stdout = result.stdout.decode('utf-8') if result.stdout else ''
        
        if result.returncode != 0:
            return {
                "query": query,
                "total": 0,
                "results": [],
                "error": f"curl执行失败: {stderr}"
            }
        
        if not stdout.strip():
            return {
                "query": query,
                "total": 0,
                "results": [],
                "error": "SearXNG返回空结果，请检查服务是否运行"
            }
        
        # 解析JSON
        try:
            data = json.loads(stdout)
        except json.JSONDecodeError as e:
            return {
                "query": query,
                "total": 0,
                "results": [],
                "error": f"JSON解析失败: {e}"
            }
        
        # 提取结果
        raw_results = data.get("results", [])
        
        # 格式化结果
        formatted_results = []
        for item in raw_results[:max_results]:
            formatted_results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
                "engine": item.get("engine", "unknown"),
                "score": item.get("score", 0)
            })
        
        return {
            "query": query,
            "total": len(raw_results),
            "results": formatted_results,
            "error": None
        }
        
    except subprocess.TimeoutExpired:
        return {
            "query": query,
            "total": 0,
            "results": [],
            "error": f"搜索超时（>{timeout}秒）"
        }
    except Exception as e:
        return {
            "query": query,
            "total": 0,
            "results": [],
            "error": f"搜索异常: {str(e)}"
        }


def search_simple(query: str, max_results: int = 5) -> List[str]:
    """
    简化版搜索，只返回URL列表
    
    Args:
        query: 搜索关键词
        max_results: 最大返回结果数
    
    Returns:
        URL列表
    """
    result = search(query, max_results)
    if result.get("error"):
        return []
    return [item["url"] for item in result.get("results", [])]


def search_with_summary(query: str, max_results: int = 5) -> str:
    """
    搜索并返回格式化的摘要文本
    
    Args:
        query: 搜索关键词
        max_results: 最大返回结果数
    
    Returns:
        格式化的搜索结果文本
    """
    result = search(query, max_results)
    
    if result.get("error"):
        return f"搜索失败: {result['error']}"
    
    if not result.get("results"):
        return f"未找到关于'{query}'的结果"
    
    lines = [f"🔍 搜索结果: {query}", f"共找到 {result['total']} 条结果\n"]
    
    for i, item in enumerate(result["results"], 1):
        lines.append(f"{i}. {item['title']}")
        lines.append(f"   {item['url']}")
        if item.get('content'):
            content = item['content'][:150] + '...' if len(item['content']) > 150 else item['content']
            lines.append(f"   {content}")
        lines.append("")
    
    return '\n'.join(lines)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='Local Search Proxy')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--max-results', '-n', type=int, default=10, help='最大结果数')
    parser.add_argument('--engines', '-e', default=DEFAULT_ENGINES, help='搜索引擎')
    parser.add_argument('--json', '-j', action='store_true', help='输出JSON格式')
    parser.add_argument('--simple', '-s', action='store_true', help='仅输出URL')
    
    args = parser.parse_args()
    
    if args.simple:
        urls = search_simple(args.query, args.max_results)
        for url in urls:
            print(url)
    elif args.json:
        result = search(args.query, args.max_results, args.engines)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        summary = search_with_summary(args.query, args.max_results)
        print(summary)


if __name__ == "__main__":
    main()
