import os
import json
from datetime import datetime, timedelta
from working_buffer import WorkingBuffer
from wal_protocol import WALProtocol
from autonomous_executor import AutonomousExecutor

def analyze_chat_records(buffer: WorkingBuffer, days_back: int = 3, resume: bool = False):
    """分析聊天记录"""
    # 查找聊天记录文件
    chat_dir = "/home/admin/.openclaw/workspace/messages"
    if not os.path.exists(chat_dir):
        os.makedirs(chat_dir)
    
    # 获取最近的聊天记录文件
    chat_files = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        # 假设聊天记录按日期存储
        chat_file = f"{chat_dir}/chat_{date_str}.json"
        if os.path.exists(chat_file):
            chat_files.append(chat_file)
        current_date += timedelta(days=1)
    
    # 分析聊天记录
    analysis_results = []
    for i, chat_file in enumerate(chat_files):
        with open(chat_file, 'r') as f:
            try:
                chat_data = json.load(f)
                if isinstance(chat_data, list):
                    message_count = len(chat_data)
                    # 简单分析：统计消息数量、关键词等
                    analysis = {
                        "date": chat_file.split('_')[-1].replace('.json', ''),
                        "message_count": message_count,
                        "has_questions": any("?" in str(msg.get('content', '')) for msg in chat_data),
                        "has_commands": any("/" in str(msg.get('content', '')) for msg in chat_data),
                        "avg_message_length": sum(len(str(msg.get('content', ''))) for msg in chat_data) / message_count if message_count > 0 else 0
                    }
                else:
                    analysis = {
                        "date": chat_file.split('_')[-1].replace('.json', ''),
                        "message_count": 1,
                        "has_questions": "?" in str(chat_data.get('content', '')),
                        "has_commands": "/" in str(chat_data.get('content', '')),
                        "avg_message_length": len(str(chat_data.get('content', '')))
                    }
                
                analysis_results.append(analysis)
                buffer.store_chunk(f"chat_analysis_{i}", analysis, {"source_file": chat_file})
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON file: {chat_file}")
                continue
    
    # 生成分析报告
    report = generate_chat_analysis_report(analysis_results)
    
    # 保存分析结果
    report_file = f"{chat_dir}/analysis_report_{end_date.strftime('%Y%m%d')}.json"
    with open(report_file, 'w') as f:
        json.dump({
            "report": report,
            "analysis_results": analysis_results,
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "analysis_time": datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)
    
    return {
        "report_file": report_file,
        "analyzed_days": len(analysis_results),
        "total_messages": sum(r['message_count'] for r in analysis_results)
    }

def generate_chat_analysis_report(analysis_results):
    """生成聊天分析报告"""
    if not analysis_results:
        return "暂无聊天记录可分析"
    
    total_messages = sum(r['message_count'] for r in analysis_results)
    avg_messages_per_day = total_messages / len(analysis_results)
    question_days = sum(1 for r in analysis_results if r['has_questions'])
    command_days = sum(1 for r in analysis_results if r['has_commands'])
    
    report = f"""
聊天记录分析报告（ {len(analysis_results)}天）：
- 总消息数: {total_messages}
- 日均消息数: {avg_messages_per_day:.1f}
- 包含问题的天数: {question_days}
- 包含命令的天数: {command_days}
- 最活跃日期: {max(analysis_results, key=lambda x: x['message_count'])['date'] if analysis_results else 'N/A'}
    """.strip()
    
    return report

# 创建自主执行器实例
chat_executor = AutonomousExecutor("chat_analysis_processing", timeout_minutes=8)

def run_chat_analysis():
    """聊天分析任务入口"""
    task_id = f"chat_analysis_{datetime.now().strftime('%Y%m%d')}"
    
    try:
        result = chat_executor.execute_with_recovery(
            analyze_chat_records,
            task_id,
            days_back=3
        )
        print(f"Chat analysis completed: {result}")
        return result
    except Exception as e:
        print(f"Chat analysis failed: {e}")
        raise