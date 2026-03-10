#!/usr/bin/env python3
"""
分布式搜索系统 - 简化版本
用于测试基础框架功能
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

# 配置常量
SEARCH_KEYWORDS = ["AI Agent", "大模型", "智能体", "提示词"]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUFFER_DIR = os.path.join(BASE_DIR, "search_buffer")
REPORT_DIR = os.path.join(BASE_DIR, "final_report")

class DistributedSearchManager:
    def __init__(self):
        """初始化搜索管理器"""
        self.keywords = SEARCH_KEYWORDS
        self.buffer_dir = BUFFER_DIR
        self.report_dir = REPORT_DIR
        # 确保目录存在
        os.makedirs(self.buffer_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)
    
    def get_today_date_str(self) -> str:
        """获取今天的日期字符串"""
        return datetime.now().strftime("%Y%m%d")
    
    def get_buffer_filename(self, keyword: str, date_str: str = None) -> str:
        """获取缓冲文件名"""
        if date_str is None:
            date_str = self.get_today_date_str()
        safe_keyword = keyword.replace(" ", "_").replace("/", "_")
        return f"{safe_keyword}_{date_str}.json"
    
    def save_search_results(self, keyword: str, results: List[Dict], date_str: str = None):
        """保存搜索结果到缓冲区"""
        if date_str is None:
            date_str = self.get_today_date_str()
        
        filename = self.get_buffer_filename(keyword, date_str)
        filepath = os.path.join(self.buffer_dir, filename)
        
        data = {
            'keyword': keyword,
            'search_time': datetime.now().isoformat(),
            'results': results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 保存搜索结果: {filepath}")
    
    def load_search_results(self, keyword: str, date_str: str = None) -> Optional[Dict]:
        """从缓冲区加载搜索结果"""
        if date_str is None:
            date_str = self.get_today_date_str()
        
        filename = self.get_buffer_filename(keyword, date_str)
        filepath = os.path.join(self.buffer_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠️  缓冲文件不存在: {filepath}")
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def simulate_search_phase(self, keyword: str):
        """模拟搜索阶段（实际使用时会调用SearXNG）"""
        print(f"🔍 模拟搜索关键词: {keyword}")
        
        # 模拟搜索结果
        mock_results = [
            {
                'title': f'模拟岗位 - {keyword}工程师',
                'company': '模拟公司',
                'location': '深圳',
                'publish_time': datetime.now().isoformat(),
                'url': 'https://example.com'
            }
        ]
        
        self.save_search_results(keyword, mock_results)
        print(f"✅ 模拟搜索完成: {keyword}")
    
    def aggregate_results(self, date_str: str = None):
        """汇总所有搜索结果"""
        if date_str is None:
            date_str = self.get_today_date_str()
        
        print(f"📊 开始汇总搜索结果 (日期: {date_str})")
        
        all_results = []
        successful_keywords = []
        
        for keyword in self.keywords:
            results_data = self.load_search_results(keyword, date_str)
            if results_data and 'results' in results_data:
                all_results.extend(results_data['results'])
                successful_keywords.append(keyword)
            else:
                print(f"⚠️  跳过关键词: {keyword} (无数据)")
        
        # 生成报告
        report = self.generate_report(all_results, successful_keywords, date_str)
        report_filename = f"shenzhen_ai_intern_report_{date_str}.md"
        report_path = os.path.join(self.report_dir, report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 汇总完成! 报告已保存: {report_path}")
        return report
    
    def generate_report(self, all_results: List[Dict], keywords: List[str], date_str: str) -> str:
        """生成最终报告"""
        report = f"# 📋 深圳AI实习岗位日报 ({date_str})\n\n"
        report += f"## 🔍 搜索关键词\n"
        for keyword in keywords:
            report += f"- {keyword}\n"
        
        report += f"\n## 🎯 发现岗位 ({len(all_results)}个)\n\n"
        
        for i, result in enumerate(all_results, 1):
            report += f"### {i}. **{result.get('title', '未知岗位')}**\n"
            report += f"- **公司**: {result.get('company', '未知')}\n"
            report += f"- **地点**: {result.get('location', '未知')}\n"
            report += f"- **链接**: {result.get('url', '无')}\n\n"
        
        report += f"---\n*注：本报告由分布式搜索系统自动生成*"
        return report

def main():
    """主函数 - 测试基础框架"""
    print("🚀 开始测试分布式搜索系统基础框架...")
    
    try:
        # 创建搜索管理器
        manager = DistributedSearchManager()
        print("✅ 搜索管理器初始化成功")
        
        # 模拟搜索阶段
        for keyword in SEARCH_KEYWORDS:
            manager.simulate_search_phase(keyword)
            time.sleep(0.1)  # 小延迟避免冲突
        
        # 模拟汇总阶段
        report = manager.aggregate_results()
        print("✅ 基础框架测试完成!")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)