#!/usr/bin/env python3
"""
分布式搜索系统测试脚本
"""

import os
import sys
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from search_manager import DistributedSearchManager

def test_framework():
    """测试基础框架功能"""
    print("🚀 开始测试分布式搜索系统基础框架...")
    
    # 创建管理器实例
    manager = DistributedSearchManager()
    
    # 测试1: 检查目录结构
    print("✅ 测试1: 目录结构检查")
    assert os.path.exists(manager.config["BUFFER_DIR"]), "缓冲目录不存在"
    assert os.path.exists(manager.config["REPORT_DIR"]), "报告目录不存在"
    print("   目录结构正常")
    
    # 测试2: 检查配置
    print("✅ 测试2: 配置检查")
    assert len(manager.keywords) == 4, f"关键词数量错误: {len(manager.keywords)}"
    print(f"   关键词: {manager.keywords}")
    
    # 测试3: 缓冲文件操作
    print("✅ 测试3: 缓冲文件操作")
    test_data = {"test": "data", "timestamp": datetime.now().isoformat()}
    keyword = "AI Agent"
    date_str = datetime.now().strftime("%Y%m%d")
    
    manager.save_to_buffer(keyword, test_data, date_str)
    loaded_data = manager.load_from_buffer(keyword, date_str)
    
    assert loaded_data == test_data, "缓冲文件读写不一致"
    print("   缓冲文件操作正常")
    
    # 测试4: 报告生成
    print("✅ 测试4: 报告生成")
    all_results = [
        {
            "title": "测试岗位1",
            "company": "测试公司",
            "location": "深圳",
            "url": "https://example.com",
            "published_date": "2026-03-10"
        }
    ]
    
    report = manager.format_daily_report(all_results, date_str)
    assert "深圳AI实习岗位日报" in report, "报告格式错误"
    print("   报告生成正常")
    
    print("\n🎉 基础框架测试完成！所有功能正常运行。")
    print(f"📁 项目路径: {os.path.dirname(os.path.abspath(__file__))}")
    
    return True

if __name__ == "__main__":
    try:
        test_framework()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        sys.exit(1)