#!/usr/bin/env python3
"""
AI Agent定时任务监控器
监控OpenClaw定时任务的执行状态
"""

import json
import time
from datetime import datetime
from typing import Dict, List

class TaskMonitor:
    def __init__(self):
        self.tasks = {}
    
    def add_task(self, task_name: str, status: str, last_run: str = None):
        """添加任务状态"""
        self.tasks[task_name] = {
            'status': status,
            'last_run': last_run or datetime.now().isoformat(),
            'timestamp': time.time()
        }
    
    def get_status_report(self) -> str:
        """生成状态报告"""
        report = "📊 AI Agent定时任务监控报告\n"
        report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for task_name, info in self.tasks.items():
            status_emoji = "✅" if info['status'] == 'success' else "❌"
            report += f"{status_emoji} {task_name}: {info['status']}\n"
            report += f"   最后执行: {info['last_run'][:19]}\n\n"
        
        return report

def main():
    # 创建监控器实例
    monitor = TaskMonitor()
    
    # 添加示例任务
    monitor.add_task("AI Agent日报", "success", "2026-03-10T09:00:00")
    monitor.add_task("深圳实习推送", "success", "2026-03-10T14:00:00")
    monitor.add_task("记忆整理", "pending", "2026-03-10T02:00:00")
    
    # 输出报告
    print(monitor.get_status_report())

if __name__ == "__main__":
    main()