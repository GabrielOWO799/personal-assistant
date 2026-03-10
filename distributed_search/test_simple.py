#!/usr/bin/env python3
"""
简化版测试脚本
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from search_manager_simple import DistributedSearchManager

def test_framework():
    """测试基础框架"""
    print("🚀 开始测试分布式搜索系统基础框架...")
    
    try:
        # 创建管理器实例
        manager = DistributedSearchManager()
        print("✅ 搜索管理器初始化成功")
        
        # 测试目录创建
        manager.ensure_directories()
        print("✅ 目录结构创建成功")
        
        # 测试配置
        print(f"✅ 配置加载成功，关键词数量: {len(manager.search_keywords)}")
        
        # 测试缓冲文件路径
        test_keyword = "AI Agent"
        buffer_path = manager.get_buffer_path(test_keyword)
        print(f"✅ 缓冲文件路径生成成功: {buffer_path}")
        
        # 测试报告路径
        report_path = manager.get_report_path()
        print(f"✅ 报告文件路径生成成功: {report_path}")
        
        print("🎉 基础框架测试完成！所有组件正常工作。")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_framework()