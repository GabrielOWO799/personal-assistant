#!/usr/bin/env python3
"""
分布式搜索系统配置文件
"""

import os
from datetime import datetime

# 搜索关键词配置
SEARCH_KEYWORDS = [
    "AI Agent",
    "大模型", 
    "智能体",
    "提示词"
]

# 时间配置
SEARCH_SCHEDULE = {
    "AI Agent": "09:00",
    "大模型": "10:00", 
    "智能体": "11:00",
    "提示词": "12:00"
}

AGGREGATION_TIME = "14:00"

# 路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUFFER_DIR = os.path.join(BASE_DIR, "search_buffer")
REPORT_DIR = os.path.join(BASE_DIR, "final_report")

# SearXNG配置
SEARXNG_URL = "http://localhost:8080"
SEARCH_TIMEOUT = 30

# 搜索参数
SEARCH_QUERY_TEMPLATE = "深圳 {keyword} 实习"
MAX_RESULTS_PER_SEARCH = 20

def get_today_date_str():
    """获取今天的日期字符串"""
    return datetime.now().strftime("%Y%m%d")

def get_buffer_filename(keyword, date_str=None):
    """获取缓冲文件名"""
    if date_str is None:
        date_str = get_today_date_str()
    safe_keyword = keyword.replace(" ", "_").replace("/", "_")
    return f"{safe_keyword}_{date_str}.json"

def get_report_filename(date_str=None):
    """获取报告文件名"""
    if date_str is None:
        date_str = get_today_date_str()
    return f"shenzhen_ai_intern_report_{date_str}.md"