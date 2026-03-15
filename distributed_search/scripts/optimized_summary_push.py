#!/usr/bin/env python3
"""
优化版分布式搜索汇总推送脚本
解决原脚本超时和飞书推送限制问题
兼容Python 3.6.8
"""

import os
import json
import time
import asyncio
from pathlib import Path
from typing import List, Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OptimizedSearchSummary:
    def __init__(self):
        self.search_buffer_dir = "/home/admin/.openclaw/workspace/distributed_search/search_buffer"
        self.max_files_per_batch = 10
        self.sleep_between_batches = 1  # 秒
        self.max_message_length = 4000  # 飞书消息长度限制
        
    def get_json_files(self) -> List[str]:
        """获取所有JSON文件列表"""
        json_files = []
        try:
            for file_path in Path(self.search_buffer_dir).glob("*.json"):
                if file_path.is_file():
                    json_files.append(str(file_path))
            logger.info(f"找到 {len(json_files)} 个JSON文件")
            return sorted(json_files, key=os.path.getmtime, reverse=True)
        except Exception as e:
            logger.error(f"获取JSON文件列表失败: {e}")
            return []
    
    def load_json_file(self, file_path: str) -> List[Dict]:
        """安全加载单个JSON文件并提取results"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 新的JSON格式包含results字段
                if isinstance(data, dict) and 'results' in data:
                    results = data.get('results', [])
                    logger.info(f"从文件 {file_path} 提取到 {len(results)} 个结果")
                    return results
                elif isinstance(data, list):
                    logger.info(f"从文件 {file_path} 提取到 {len(data)} 个结果（旧格式）")
                    return data
                else:
                    logger.warning(f"文件 {file_path} 格式不正确")
                    return []
        except Exception as e:
            logger.error(f"加载文件 {file_path} 失败: {e}")
            return []
    
    def filter_valid_positions(self, positions: List[Dict]) -> List[Dict]:
        """过滤有效的职位信息"""
        valid_positions = []
        exclude_keywords = ['校招', '招聘', '主页', '验证', '打卡', '白皮书', '汇总', '学员', '训练营']
        include_keywords = ['工程师', '实习生', '算法', '开发', 'Prompt Engineer', '提示词', '智能体', 'Agent']
        
        for pos in positions:
            title = str(pos.get('title', ''))
            description = str(pos.get('description', ''))
            
            # 检查是否包含排除关键词
            if any(keyword in title or keyword in description for keyword in exclude_keywords):
                continue
                
            # 检查是否包含包含关键词
            if any(keyword in title or keyword in description for keyword in include_keywords):
                # 转换为标准格式
                standardized_pos = {
                    'title': title,
                    'company': self.extract_company(title),
                    'location': pos.get('location', '深圳'),
                    'direction': self.extract_direction(title, description),
                    'salary': '面议',
                    'link': pos.get('url', '#'),
                    'source_type': pos.get('source', '招聘网站')
                }
                valid_positions.append(standardized_pos)
                
        logger.info(f"过滤后保留 {len(valid_positions)} 个有效职位")
        return valid_positions
    
    def extract_company(self, title: str) -> str:
        """从标题中提取公司名称"""
        # 常见公司关键词
        companies = ['腾讯', '字节', '华为', '阿里', '百度', '美团', '京东', '小米', '网易', '复星', '美图', '博世', '三星']
        for company in companies:
            if company in title:
                return company
        return "未知公司"
    
    def extract_direction(self, title: str, description: str) -> str:
        """从标题和描述中提取方向"""
        directions = ['AI Agent', '大模型', '算法', '开发', '提示词工程', '计算机视觉', '产品']
        for direction in directions:
            if direction in title or direction in description:
                return direction
        return "未指定方向"
    
    def process_files_in_batches(self, json_files: List[str]) -> List[Dict]:
        """分批处理JSON文件（同步版本，兼容Python 3.6）"""
        all_positions = []
        total_files = len(json_files)
        
        for i in range(0, total_files, self.max_files_per_batch):
            batch = json_files[i:i + self.max_files_per_batch]
            logger.info(f"正在处理批次 {i//self.max_files_per_batch + 1}/{(total_files-1)//self.max_files_per_batch + 1}, 文件数: {len(batch)}")
            
            # 处理当前批次
            batch_positions = []
            for file_path in batch:
                positions = self.load_json_file(file_path)
                valid_positions = self.filter_valid_positions(positions)
                batch_positions.extend(valid_positions)
            
            all_positions.extend(batch_positions)
            
            # 批次间休息，避免资源占用过高
            if i + self.max_files_per_batch < total_files:
                logger.info(f"批次处理完成，休息 {self.sleep_between_batches} 秒...")
                time.sleep(self.sleep_between_batches)
        
        # 按相关性排序（优先包含具体关键词的）
        def sort_key(pos):
            title = pos.get('title', '').lower()
            score = 0
            if '实习' in title:
                score += 10
            if '工程师' in title:
                score += 5
            if '腾讯' in title or '字节' in title or '华为' in title or '阿里' in title:
                score += 3
            return -score  # 负号表示降序
        
        all_positions.sort(key=sort_key)
        logger.info(f"总共收集到 {len(all_positions)} 个有效职位")
        return all_positions[:10]  # 只取最相关的10个
    
    def create_markdown_summary(self, positions: List[Dict], date_str: str = "2026年03月15日") -> str:
        """创建Markdown格式的日报摘要"""
        if not positions:
            return f"# 📋 深圳AI Agent实习岗位日报（{date_str}）\n\n今日暂无符合条件的岗位信息。"
        
        # 按关键词分类
        categories = {
            'AI Agent': [],
            '大模型': [],
            '算法开发': [],
            '提示词工程': []
        }
        
        for pos in positions:
            title = pos.get('title', '').lower()
            direction = pos.get('direction', '')
            
            if 'agent' in title or '智能体' in title or 'AI Agent' in direction:
                if '大模型' in title or 'llm' in title:
                    categories['大模型'].append(pos)
                elif '提示词' in title or 'prompt' in title:
                    categories['提示词工程'].append(pos)
                else:
                    categories['AI Agent'].append(pos)
            elif '大模型' in title or 'llm' in title or '大模型' in direction:
                categories['大模型'].append(pos)
            elif '提示词' in title or 'prompt' in title or '提示词工程' in direction:
                categories['提示词工程'].append(pos)
            elif '算法' in direction or '开发' in direction or '工程师' in title:
                categories['算法开发'].append(pos)
            else:
                categories['AI Agent'].append(pos)
        
        markdown = f"# 📋 深圳AI Agent实习岗位日报（{date_str}）\n\n"
        
        for category, positions_list in categories.items():
            if positions_list:
                markdown += f"## 🔍 {category} 相关岗位\n\n"
                for i, pos in enumerate(positions_list[:3], 1):  # 每类最多显示3个
                    company = pos.get('company', '未知公司')
                    location = pos.get('location', '深圳')
                    direction = pos.get('direction', '未指定方向')
                    salary = pos.get('salary', '面议')
                    link = pos.get('link', '#')
                    source_type = pos.get('source_type', '招聘网站')
                    
                    markdown += f"### {i}. {pos.get('title', '未知职位')}\n"
                    markdown += f"- **公司**: {company}\n"
                    markdown += f"- **地点**: {location}\n"
                    markdown += f"- **方向**: {direction}\n"
                    markdown += f"- **薪资**: {salary}\n"
                    markdown += f"- **链接**: [{link}]({link})\n"
                    markdown += f"- **来源**: {source_type}\n\n"
        
        # 添加建议部分
        markdown += "## 💡 建议与资源\n\n"
        markdown += "1. **投递建议**: 重点关注腾讯、字节、华为、阿里等大厂的AI岗位\n"
        markdown += "2. **技能准备**: 熟悉Python、大语言模型原理、Prompt Engineering技术\n"
        markdown += "3. **求职渠道**: 实习僧、猎聘、BOSS直聘等平台\n\n"
        markdown += "> **注**: 本日报基于分布式搜索系统整理，已严格过滤非具体岗位信息。\n"
        
        return markdown
    
    def split_message_for_feishu(self, full_message: str) -> List[str]:
        """将长消息分割为适合飞书推送的多条消息"""
        if len(full_message) <= self.max_message_length:
            return [full_message]
        
        # 分割为多个部分
        parts = []
        lines = full_message.split('\n')
        current_part = ""
        
        for line in lines:
            if len(current_part + line + '\n') <= self.max_message_length:
                current_part += line + '\n'
            else:
                if current_part:
                    parts.append(current_part)
                current_part = line + '\n'
        
        if current_part:
            parts.append(current_part)
        
        # 如果分割后的部分太多，只发送摘要
        if len(parts) > 5:
            summary = "# 📋 深圳AI Agent实习岗位日报（今日）\n\n"
            summary += "由于岗位信息较多，完整版请查看详细报告。\n\n"
            summary += "## 今日亮点\n"
            # 这里可以添加一些关键信息的摘要
            return [summary]
        
        return parts
    
    def main(self):
        """主执行函数（同步版本）"""
        logger.info("开始执行优化版分布式搜索汇总任务")
        
        # 获取JSON文件列表
        json_files = self.get_json_files()
        if not json_files:
            logger.warning("未找到任何JSON文件")
            return None
        
        # 分批处理文件
        positions = self.process_files_in_batches(json_files)
        
        # 生成日报
        from datetime import datetime
        today = datetime.now().strftime("%Y年%m月%d日")
        full_report = self.create_markdown_summary(positions, today)
        
        # 分割消息并准备推送
        message_parts = self.split_message_for_feishu(full_report)
        logger.info(f"生成日报完成，共 {len(message_parts)} 条消息")
        
        # 返回消息内容，由调用方负责实际推送
        return message_parts

if __name__ == "__main__":
    processor = OptimizedSearchSummary()
    messages = processor.main()
    if messages:
        # 在实际cron任务中，这里会返回messages供推送使用
        print("=== 生成的日报内容 ===")
        for i, msg in enumerate(messages, 1):
            print(f"\n--- 消息 {i} ---\n{msg}")
    else:
        print("=== 未生成日报内容 ===")