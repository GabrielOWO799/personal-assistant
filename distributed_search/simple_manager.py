#!/usr/bin/env python3
"""
简化版分布式搜索管理器
用于测试基础框架
"""

import os
import json
from datetime import datetime

class SimpleSearchManager:
    def __init__(self):
        self.keywords = ["AI Agent", "大模型", "智能体", "提示词"]
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.buffer_dir = os.path.join(self.base_dir, "search_buffer")
        self.report_dir = os.path.join(self.base_dir, "final_report")
        
        # 确保目录存在
        os.makedirs(self.buffer_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)
    
    def save_search_result(self, keyword, results):
        """保存搜索结果到缓冲区"""
        date_str = datetime.now().strftime("%Y%m%d")
        safe_keyword = keyword.replace(" ", "_").replace("/", "_")
        filename = f"{safe_keyword}_{date_str}.json"
        filepath = os.path.join(self.buffer_dir, filename)
        
        data = {
            "keyword": keyword,
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def load_all_results(self):
        """加载所有搜索结果"""
        all_results = []
        date_str = datetime.now().strftime("%Y%m%d")
        
        for keyword in self.keywords:
            safe_keyword = keyword.replace(" ", "_").replace("/", "_")
            filename = f"{safe_keyword}_{date_str}.json"
            filepath = os.path.join(self.buffer_dir, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_results.append(data)
        
        return all_results
    
    def generate_report(self, all_results):
        """生成汇总报告"""
        report = "# 📋 深圳AI实习岗位日报\n\n"
        report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for result_data in all_results:
            keyword = result_data["keyword"]
            results = result_data["results"]
            report += f"## 🔍 {keyword} 相关岗位\n\n"
            if results:
                for i, result in enumerate(results[:5], 1):  # 只显示前5个
                    title = result.get('title', '无标题')
                    url = result.get('url', '#')
                    report += f"{i}. [{title}]({url})\n"
            else:
                report += "暂无相关岗位信息\n"
            report += "\n"
        
        return report

def test_framework():
    """测试基础框架"""
    print("🚀 开始测试分布式搜索系统基础框架...")
    
    try:
        # 初始化管理器
        manager = SimpleSearchManager()
        print("✅ 搜索管理器初始化成功")
        
        # 测试保存结果
        test_results = [
            {"title": "测试岗位1", "url": "https://example.com/1"},
            {"title": "测试岗位2", "url": "https://example.com/2"}
        ]
        
        filepath = manager.save_search_result("AI Agent", test_results)
        print(f"✅ 测试结果保存成功: {filepath}")
        
        # 测试加载结果
        loaded_results = manager.load_all_results()
        print(f"✅ 结果加载成功: 找到 {len(loaded_results)} 个关键词的结果")
        
        # 测试生成报告
        report = manager.generate_report(loaded_results)
        print("✅ 报告生成成功")
        print("\n📋 生成的报告预览:")
        print(report[:200] + "...")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_framework()