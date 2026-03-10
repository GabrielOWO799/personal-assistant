#!/usr/bin/env python3
"""
分布式搜索管理器
用于分时段执行关键词搜索并汇总结果
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from config import SEARCH_CONFIG

class DistributedSearchManager:
    """分布式搜索管理器主类"""
    
    def __init__(self):
        self.keywords = ["AI Agent", "大模型", "智能体", "提示词"]
        self.buffer_dir = "search_buffer"
        self.report_dir = "final_report"
        self.searxng_url = SEARCH_CONFIG['searxng_url']
        self.search_timeout = SEARCH_CONFIG['search_timeout']
        
        # 确保目录存在
        os.makedirs(self.buffer_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)
    
    def call_searxng(self, query: str, time_range: str = "") -> List[Dict]:
        """
        调用本地SearXNG实例进行搜索
        
        Args:
            query: 搜索查询字符串
            time_range: 时间范围（可选）
            
        Returns:
            搜索结果列表
        """
        try:
            # 构建搜索参数
            params = {
                'q': query,
                'format': 'json',
                'language': 'zh-CN'
            }
            
            if time_range:
                params['time_range'] = time_range
            
            # 执行HTTP请求
            response = requests.post(
                self.searxng_url,
                data=params,
                timeout=self.search_timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
            else:
                print(f"搜索请求失败: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"搜索执行异常: {str(e)}")
            return []
    
    def save_to_buffer(self, keyword: str, results: List[Dict], date_str: str):
        """
        将搜索结果保存到缓冲区
        
        Args:
            keyword: 搜索关键词
            results: 搜索结果列表
            date_str: 日期字符串 (YYYY-MM-DD)
        """
        # 清理关键词中的特殊字符
        safe_keyword = keyword.replace(" ", "_").replace("/", "_")
        filename = f"{safe_keyword}_{date_str}.json"
        filepath = os.path.join(self.buffer_dir, filename)
        
        # 保存结果
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'keyword': keyword,
                'query_time': datetime.now().isoformat(),
                'results': results,
                'result_count': len(results)
            }, f, ensure_ascii=False, indent=2)
        
        print(f"已保存 {len(results)} 条结果到 {filepath}")
    
    def load_from_buffer(self, keyword: str, date_str: str) -> Optional[List[Dict]]:
        """
        从缓冲区加载搜索结果
        
        Args:
            keyword: 搜索关键词
            date_str: 日期字符串 (YYYY-MM-DD)
            
        Returns:
            搜索结果列表，如果文件不存在则返回None
        """
        safe_keyword = keyword.replace(" ", "_").replace("/", "_")
        filename = f"{safe_keyword}_{date_str}.json"
        filepath = os.path.join(self.buffer_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('results', [])
        else:
            print(f"缓冲文件不存在: {filepath}")
            return None
    
    def remove_duplicates(self, all_results: List[Dict]) -> List[Dict]:
        """
        去除重复的搜索结果
        
        Args:
            all_results: 所有搜索结果的列表
            
        Returns:
            去重后的结果列表
        """
        seen_urls = set()
        unique_results = []
        
        for result in all_results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
    
    def sort_results_by_relevance(self, results: List[Dict]) -> List[Dict]:
        """
        根据相关性对结果进行排序
        
        Args:
            results: 搜索结果列表
            
        Returns:
            排序后的结果列表
        """
        def get_score(result: Dict) -> float:
            # 基础分数
            score = result.get('score', 0.0)
            
            # 根据发布时间调整分数（越新越高）
            published_date = result.get('publishedDate')
            if published_date:
                try:
                    pub_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                    days_old = (datetime.now() - pub_date).days
                    if days_old >= 0:
                        score += max(0, 1.0 - days_old * 0.1)  # 最多减1分
                except:
                    pass
            
            return score
        
        return sorted(results, key=get_score, reverse=True)
    
    def format_daily_report(self, all_results: List[Dict], date_str: str) -> str:
        """
        格式化每日日报
        
        Args:
            all_results: 所有搜索结果
            date_str: 日期字符串
            
        Returns:
            格式化的日报字符串
        """
        # 去重和排序
        unique_results = self.remove_duplicates(all_results)
        sorted_results = self.sort_results_by_relevance(unique_results)
        
        # 限制结果数量
        final_results = sorted_results[:10]
        
        # 生成日报内容
        report = f"# 📋 深圳AI实习岗位日报（{date_str}）\n\n"
        report += f"## 🔍 搜索关键词\n"
        for keyword in self.keywords:
            report += f"- {keyword}\n"
        
        report += f"\n## 🎯 今日精选岗位（共{len(final_results)}条）\n\n"
        
        if not final_results:
            report += "今日暂无相关实习岗位信息\n"
        else:
            for i, result in enumerate(final_results, 1):
                title = result.get('title', '无标题')
                url = result.get('url', '#')
                content = result.get('content', '无描述')
                published_date = result.get('publishedDate', '未知时间')
                
                report += f"### {i}. **{title}**\n"
                report += f"- **链接**: [{url}]({url})\n"
                if published_date != '未知时间':
                    report += f"- **发布时间**: {published_date}\n"
                report += f"- **摘要**: {content[:150]}{'...' if len(content) > 150 else ''}\n\n"
        
        report += f"---\n"
        report += f"*注：本日报基于分布式搜索系统，分时段执行关键词搜索后汇总生成。*\n"
        
        return report
    
    def search_phase(self, keyword: str, date_str: Optional[str] = None):
        """
        执行单个关键词的搜索阶段
        
        Args:
            keyword: 搜索关键词
            date_str: 日期字符串，如果为None则使用当前日期
        """
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        print(f"开始搜索关键词: {keyword}")
        
        # 构建查询
        query = f"深圳 {keyword} 实习"
        
        # 执行搜索
        results = self.call_searxng(query)
        
        # 保存结果
        self.save_to_buffer(keyword, results, date_str)
        
        print(f"关键词 '{keyword}' 搜索完成，找到 {len(results)} 条结果")
    
    def aggregate_results(self, date_str: Optional[str] = None) -> str:
        """
        汇总所有搜索结果并生成日报
        
        Args:
            date_str: 日期字符串，如果为None则使用当前日期
            
        Returns:
            格式化的日报字符串
        """
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        print(f"开始汇总 {date_str} 的搜索结果")
        
        all_results = []
        missing_keywords = []
        
        # 加载所有关键词的搜索结果
        for keyword in self.keywords:
            results = self.load_from_buffer(keyword, date_str)
            if results is not None:
                all_results.extend(results)
                print(f"加载关键词 '{keyword}' 的 {len(results)} 条结果")
            else:
                missing_keywords.append(keyword)
                print(f"警告: 关键词 '{keyword}' 的搜索结果缺失")
        
        # 生成日报
        if all_results:
            report = self.format_daily_report(all_results, date_str)
        else:
            report = f"# 📋 深圳AI实习岗位日报（{date_str}）\n\n"
            report += "今日暂无相关实习岗位信息\n\n"
            if missing_keywords:
                report += f"⚠️ 以下关键词的搜索结果缺失: {', '.join(missing_keywords)}\n"
            report += f"---\n*注：本日报基于分布式搜索系统生成。*\n"
        
        # 保存日报
        report_filename = f"daily_report_{date_str}.md"
        report_path = os.path.join(self.report_dir, report_filename)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"日报已保存到 {report_path}")
        return report

def main():
    """测试函数"""
    manager = DistributedSearchManager()
    
    # 测试单个搜索
    print("=== 测试单个搜索 ===")
    manager.search_phase("AI Agent")
    
    # 测试汇总
    print("\n=== 测试结果汇总 ===")
    report = manager.aggregate_results()
    print("生成的日报预览:")
    print(report[:500] + "..." if len(report) > 500 else report)

if __name__ == "__main__":
    main()