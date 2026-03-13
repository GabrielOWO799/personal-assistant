import os
import json
import shutil
from datetime import datetime, timedelta

class WorkingBuffer:
    def __init__(self, buffer_name, base_path="/home/admin/.openclaw/workspace/working_buffer"):
        self.buffer_name = buffer_name
        self.base_path = base_path
        self.buffer_path = f"{base_path}/{buffer_name}"
        os.makedirs(self.buffer_path, exist_ok=True)
        
    def store_chunk(self, chunk_id, data, metadata=None):
        """存储数据块"""
        chunk_file = f"{self.buffer_path}/chunk_{chunk_id}.json"
        chunk_data = {
            "data": data,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "chunk_id": chunk_id
        }
        with open(chunk_file, 'w') as f:
            json.dump(chunk_data, f, indent=2, ensure_ascii=False)
            
    def retrieve_chunks(self, chunk_ids=None):
        """检索数据块"""
        chunks = []
        if chunk_ids is None:
            # 获取所有chunks
            for filename in os.listdir(self.buffer_path):
                if filename.startswith('chunk_') and filename.endswith('.json'):
                    with open(f"{self.buffer_path}/{filename}", 'r') as f:
                        chunks.append(json.load(f))
        else:
            for chunk_id in chunk_ids:
                chunk_file = f"{self.buffer_path}/chunk_{chunk_id}.json"
                if os.path.exists(chunk_file):
                    with open(chunk_file, 'r') as f:
                        chunks.append(json.load(f))
        return sorted(chunks, key=lambda x: x['chunk_id'])
        
    def merge_chunks(self, output_file=None):
        """合并所有chunks"""
        chunks = self.retrieve_chunks()
        merged_data = []
        metadata = {}
        
        for chunk in chunks:
            merged_data.extend(chunk['data'] if isinstance(chunk['data'], list) else [chunk['data']])
            metadata.update(chunk['metadata'])
            
        result = {
            "merged_data": merged_data,
            "metadata": metadata,
            "total_chunks": len(chunks),
            "merge_time": datetime.now().isoformat()
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
                
        return result
        
    def cleanup_old_chunks(self, hours_old=24):
        """清理旧的chunks"""
        cutoff_time = datetime.now() - timedelta(hours=hours_old)
        for filename in os.listdir(self.buffer_path):
            if filename.startswith('chunk_') and filename.endswith('.json'):
                file_path = f"{self.buffer_path}/{filename}"
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if file_time < cutoff_time:
                    os.remove(file_path)
                    
    def get_buffer_status(self):
        """获取缓冲区状态"""
        files = [f for f in os.listdir(self.buffer_path) if f.startswith('chunk_')]
        total_size = sum(os.path.getsize(f"{self.buffer_path}/{f}") for f in files)
        return {
            "buffer_name": self.buffer_name,
            "chunk_count": len(files),
            "total_size_bytes": total_size,
            "last_modified": max((os.path.getmtime(f"{self.buffer_path}/{f}") for f in files), default=0)
        }