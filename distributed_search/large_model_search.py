#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大模型实习岗位搜索脚本
"""

import requests
import json
import time
from datetime import datetime
import os
import sys

def search_large_model_jobs():
    """执行大模型实习岗位搜索"""
    # 基础搜索查询
    query = '"深圳" "大模型" ("实习" OR "实习生") ("算法工程师" OR "微调") (site:bosszhipin.com OR site:lagou.com OR site:nowcoder.com)'
    
    print(f"执行搜索: {query}")
    
    try:
        # 使用30秒超时
        params = {
            'q': query,
            'format': 'json',
            'language': 'zh-CN',
            'safesearch': '0',
            'categories': 'general'
        }
        
        response = requests.get('http://localhost:8080/search', params=params, timeout=30)
        response.raise_for_status()
        
        results = response.json()
        print(f"搜索成功！找到 {len(results.get('results', []))} 条结果")
        
        # 过滤和处理结果
        filtered_results = []
        for result in results.get('results', []):
            title = result.get('title', '').lower()
            url = result.get('url', '')
            content = result.get('content', '').lower()
            
            # 检查是否包含必要的职位关键词
            has_position_keyword = any(keyword in title or keyword in content for keyword in ['算法工程师', '实习生', '微调', '实习'])
            is_job_page = any(domain in url for domain in ['bosszhipin.com', 'lagou.com', 'nowcoder.com'])
            
            # 排除汇总页、公司主页、验证页面等
            exclude_keywords = ['校招', '校园招聘', '公司首页', '验证', 'captcha', '汇总', '列表']
            should_exclude = any(keyword in title or keyword in content for keyword in exclude_keywords)
            
            if has_position_keyword and is_job_page and not should_exclude:
                filtered_results.append({
                    'title': result.get('title', ''),
                    'url': url,
                    'content': result.get('content', ''),
                    'engine': result.get('engine', ''),
                    'parsed_url': result.get('parsed_url', '')
                })
        
        # 限制最多15条结果
        filtered_results = filtered_results[:15]
        
        # 保存结果
        date_str = datetime.now().strftime('%Y%m%d')
        output_path = f'/home/admin/.openclaw/workspace/distributed_search/search_buffer/large_model_{date_str}.json'
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'search_query': query,
                'timestamp': datetime.now().isoformat(),
                'total_results': len(filtered_results),
                'results': filtered_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"搜索完成！结果已保存到: {output_path}")
        print(f"总共找到 {len(filtered_results)} 条相关岗位信息")
        
        return len(filtered_results)
        
    except Exception as e:
        print(f"搜索失败: {e}")
        # 创建空结果文件
        date_str = datetime.now().strftime('%Y%m%d')
        output_path = f'/home/admin/.openclaw/workspace/distributed_search/search_buffer/large_model_{date_str}.json'
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'search_query': query,
                'timestamp': datetime.now().isoformat(),
                'total_results': 0,
                'results': [],
                'error': str(e)
            }, f, ensure_ascii=False, indent=2)
        
        print(f"已创建空结果文件: {output_path}")
        return 0

if __name__ == '__main__':
    search_large_model_jobs()