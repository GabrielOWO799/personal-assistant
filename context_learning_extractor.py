import os
import json
from datetime import datetime, timedelta
from working_buffer import WorkingBuffer
from wal_protocol import WALProtocol
from autonomous_executor import AutonomousExecutor

def extract_context_and_memory(buffer: WorkingBuffer, days_back: int = 7, resume: bool = False):
    """提取上下文和记忆"""
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    memory_files = []
    current_date = start_date
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        memory_file = f"/home/admin/.openclaw/workspace/memory/{date_str}.md"
        if os.path.exists(memory_file):
            memory_files.append(memory_file)
        current_date += timedelta(days=1)
    
    # 提取记忆内容
    extracted_memories = []
    for i, mem_file in enumerate(memory_files):
        with open(mem_file, 'r') as f:
            content = f.read()
        
        # 简单的上下文提取（实际可以使用更复杂的NLP方法）
        context_data = {
            "date": mem_file.split('/')[-1].replace('.md', ''),
            "content_preview": content[:500],
            "file_size": len(content),
            "has_projects": "项目进度" in content,
            "has_lessons": "经验教训" in content
        }
        
        extracted_memories.append(context_data)
        buffer.store_chunk(f"memory_{i}", context_data, {"source_file": mem_file})
    
    # 生成记忆摘要
    summary = generate_memory_summary(extracted_memories)
    
    # 保存摘要
    summary_file = f"/home/admin/.openclaw/workspace/memory/context_summary_{end_date.strftime('%Y%m%d')}.json"
    with open(summary_file, 'w') as f:
        json.dump({
            "summary": summary,
            "extracted_memories": extracted_memories,
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "extraction_time": datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)
    
    return {
        "summary_file": summary_file,
        "memory_count": len(extracted_memories),
        "period_days": days_back + 1
    }

def generate_memory_summary(memories):
    """生成记忆摘要"""
    total_files = len(memories)
    project_files = sum(1 for m in memories if m['has_projects'])
    lesson_files = sum(1 for m in memories if m['has_lessons'])
    
    summary = f"""
过去{total_files}天的记忆分析摘要：
- 总记忆文件数: {total_files}
- 包含项目进度的文件: {project_files}
- 包含经验教训的文件: {lesson_files}
- 最早记忆日期: {memories[0]['date'] if memories else 'N/A'}
- 最新记忆日期: {memories[-1]['date'] if memories else 'N/A'}
    """.strip()
    
    return summary

# 创建自主执行器实例
context_executor = AutonomousExecutor("context_learning_extraction", timeout_minutes=10)

def run_context_extraction():
    """上下文提取任务入口"""
    task_id = f"context_extract_{datetime.now().strftime('%Y%m%d')}"
    
    try:
        result = context_executor.execute_with_recovery(
            extract_context_and_memory,
            task_id,
            days_back=7
        )
        print(f"Context extraction completed: {result}")
        return result
    except Exception as e:
        print(f"Context extraction failed: {e}")
        raise