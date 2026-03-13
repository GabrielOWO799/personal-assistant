import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from wal_protocol import WALProtocol
from working_buffer import WorkingBuffer

class AutonomousExecutor:
    def __init__(self, task_name, timeout_minutes=30, max_retries=2, retry_interval_minutes=5):
        self.task_name = task_name
        self.timeout_minutes = timeout_minutes
        self.max_retries = max_retries
        self.retry_interval_minutes = retry_interval_minutes
        self.wal = WALProtocol(task_name)
        self.buffer = WorkingBuffer(task_name)
        
    def execute_with_recovery(self, task_function, task_id, **kwargs):
        """带恢复能力的任务执行"""
        # 检查是否有未完成的任务
        last_status = self.wal.get_last_status()
        if last_status and last_status['status'] == 'running':
            # 检查是否超时
            start_time = datetime.fromisoformat(last_status['start_time'])
            if datetime.now() - start_time > timedelta(minutes=self.timeout_minutes):
                # 超时，标记为失败并重新开始
                self.wal.log_failure(task_id, f"Task timeout after {self.timeout_minutes} minutes")
                return self._execute_with_retries(task_function, task_id, **kwargs)
            else:
                # 尝试恢复执行
                return self._resume_execution(task_function, task_id, last_status, **kwargs)
        else:
            # 正常开始新任务
            return self._execute_with_retries(task_function, task_id, **kwargs)
            
    def _execute_with_retries(self, task_function, task_id, **kwargs):
        """带重试机制的执行"""
        for attempt in range(self.max_retries + 1):
            try:
                if attempt == 0:
                    self.wal.log_start(task_id, kwargs)
                else:
                    print(f"Retry attempt {attempt}/{self.max_retries} for task {task_id}")
                    self.wal.log_start(task_id, {**kwargs, "retry_attempt": attempt})
                
                result = task_function(self.buffer, **kwargs)
                self.wal.log_complete(task_id, result)
                return result
                
            except Exception as e:
                error_msg = str(e)
                if attempt < self.max_retries:
                    print(f"Task {task_id} failed on attempt {attempt + 1}, retrying in {self.retry_interval_minutes} minutes...")
                    self.wal.log_failure(task_id, f"Attempt {attempt + 1} failed: {error_msg}")
                    # 等待重试间隔
                    time.sleep(self.retry_interval_minutes * 60)
                else:
                    # 最后一次重试也失败了
                    final_error = f"All {self.max_retries + 1} attempts failed. Last error: {error_msg}"
                    self.wal.log_failure(task_id, final_error)
                    raise Exception(final_error)
                    
    def _resume_execution(self, task_function, task_id, last_status, **kwargs):
        """恢复执行"""
        print(f"Resuming task {task_id} from checkpoint...")
        # 这里可以根据checkpoint数据恢复状态
        # 简化实现：重新开始但使用已有的buffer数据
        try:
            result = task_function(self.buffer, resume=True, **kwargs)
            self.wal.log_complete(task_id, result)
            return result
        except Exception as e:
            self.wal.log_failure(task_id, f"Resume failed: {str(e)}")
            raise
            
    def monitor_and_heal(self):
        """监控并自动修复"""
        status = self.wal.get_last_status()
        if not status:
            return "No previous task found"
            
        if status['status'] == 'running':
            start_time = datetime.fromisoformat(status['start_time'])
            if datetime.now() - start_time > timedelta(minutes=self.timeout_minutes):
                # 自动修复超时任务
                self.wal.log_failure(status['task_id'], "Auto-healed timeout")
                return "Timeout task auto-healed"
                
        elif status['status'] == 'failed':
            # 检查是否需要重试
            failure_time = datetime.fromisoformat(status.get('end_time', datetime.now().isoformat()))
            if datetime.now() - failure_time < timedelta(minutes=self.retry_interval_minutes * (self.max_retries + 1)):
                return "Task failed but within retry window"
            else:
                return "Task failed and retry window expired"
            
        return f"Task status: {status['status']}"