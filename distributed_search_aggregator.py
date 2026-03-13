import os
import json
from datetime import datetime
from working_buffer import WorkingBuffer
from wal_protocol import WALProtocol
from autonomous_executor import AutonomousExecutor

def aggregate_search_results(buffer: WorkingBuffer, date_str: str = None, resume: bool = False):
    """聚合分布式搜索结果"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y%m%d')
    
    # 定义需要聚合的搜索类型
    search_types = ['ai_agent', 'large_model', 'intelligent_agent', 'prompt']
    
    all_results = []
    missing_types = []
    
    for search_type in search_types:
        result_file = f"/home/admin/.openclaw/workspace/distributed_search/search_buffer/{search_type}_{date_str}.json"
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_results.extend(data)
                else:
                    all_results.append(data)
            # 存储到working buffer作为检查点
            buffer.store_chunk(f"{search_type}_{date_str}", data, {"source": result_file})
        else:
            missing_types.append(search_type)
    
    if missing_types:
        raise Exception(f"Missing search results for: {missing_types}")
    
    # 生成最终报告
    report_content = generate_final_report(all_results, date_str)
    
    # 保存最终报告
    final_report_path = f"/home/admin/.openclaw/workspace/distributed_search/final_report/daily_report_{date_str}.md"
    with open(final_report_path, 'w') as f:
        f.write(report_content)
    
    return {
        "report_path": final_report_path,
        "total_results": len(all_results),
        "aggregated_types": search_types,
        "date": date_str
    }

def generate_final_report(results, date_str):
    """生成最终报告内容"""
    date_formatted = f"{date_str[:4]}年{date_str[4:6]}月{date_str[6:]}日"
    content = f"# AI实习岗位日报 - {date_formatted}\n\n"
    
    for i, result in enumerate(results[:20], 1):  # 只显示前20个结果
        title = result.get('title', '无标题')
        url = result.get('url', '#')
        company = result.get('company', '未知公司')
        location = result.get('location', '未知地点')
        salary = result.get('salary', '薪资面议')
        
        content += f"### {i}. [{title}]({url})\n"
        content += f"- **公司**: {company}\n"
        content += f"- **地点**: {location}\n"
        content += f"- **薪资**: {salary}\n\n"
    
    content += f"\n---\n由太太生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    return content

# 创建自主执行器实例
aggregator_executor = AutonomousExecutor("distributed_search_aggregation", timeout_minutes=15)

def run_daily_aggregation():
    """每日聚合任务入口"""
    today = datetime.now().strftime('%Y%m%d')
    task_id = f"agg_{today}"
    
    try:
        result = aggregator_executor.execute_with_recovery(
            aggregate_search_results, 
            task_id, 
            date_str=today
        )
        print(f"Aggregation completed: {result}")
        return result
    except Exception as e:
        print(f"Aggregation failed: {e}")
        raise