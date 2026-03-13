import json
import os
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"

class WALProtocol:
    def __init__(self, task_name, log_dir="/home/admin/.openclaw/workspace/wal_logs"):
        self.task_name = task_name
        self.log_dir = log_dir
        self.log_file = f"{log_dir}/{task_name}_wal.json"
        os.makedirs(log_dir, exist_ok=True)
        
    def log_start(self, task_id, metadata=None):
        """记录任务开始"""
        entry = {
            "task_id": task_id,
            "status": TaskStatus.RUNNING.value,
            "start_time": datetime.now().isoformat(),
            "metadata": metadata or {},
            "checkpoint": None
        }
        self._write_log(entry)
        return entry
        
    def log_checkpoint(self, task_id, checkpoint_data):
        """记录检查点"""
        current_log = self._read_log()
        if current_log and current_log.get("task_id") == task_id:
            current_log["checkpoint"] = checkpoint_data
            current_log["last_checkpoint"] = datetime.now().isoformat()
            self._write_log(current_log)
            
    def log_complete(self, task_id, result_data):
        """记录任务完成"""
        current_log = self._read_log()
        if current_log and current_log.get("task_id") == task_id:
            current_log["status"] = TaskStatus.COMPLETED.value
            current_log["end_time"] = datetime.now().isoformat()
            current_log["result"] = result_data
            self._write_log(current_log)
            
    def log_failure(self, task_id, error_message):
        """记录任务失败"""
        current_log = self._read_log()
        if current_log and current_log.get("task_id") == task_id:
            current_log["status"] = TaskStatus.FAILED.value
            current_log["end_time"] = datetime.now().isoformat()
            current_log["error"] = error_message
            self._write_log(current_log)
            
    def _read_log(self):
        """读取当前日志"""
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return None
        
    def _write_log(self, entry):
        """写入日志"""
        with open(self.log_file, 'w') as f:
            json.dump(entry, f, indent=2, ensure_ascii=False)
            
    def get_last_status(self):
        """获取最后状态"""
        return self._read_log()