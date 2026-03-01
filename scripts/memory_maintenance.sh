#!/bin/bash
# Memory Maintenance Script - 每天2:00执行
# 清理临时文件、更新记忆索引、同步GitHub

set -e

WORKSPACE="/home/admin/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)

echo "[$(date)] Starting memory maintenance..."

# 1. 清理临时文件
find "$WORKSPACE" -name "*.tmp" -delete
find "$WORKSPACE" -name "*.temp" -delete
find "$WORKSPACE/memory" -name "*.log" -mtime +7 -delete

# 2. 更新记忆索引
python3 << EOF
import os
import json
from datetime import datetime, timedelta

workspace = "$WORKSPACE"
memory_dir = os.path.join(workspace, "memory")

# 读取所有记忆文件
memory_files = []
for root, dirs, files in os.walk(memory_dir):
    for file in files:
        if file.endswith('.md') and file != 'lessons.md' and file != 'projects.md':
            memory_files.append(os.path.join(root, file))

# 创建索引
index = {
    'last_updated': datetime.now().isoformat(),
    'memory_files': memory_files,
    'total_files': len(memory_files)
}

with open(os.path.join(memory_dir, 'index.json'), 'w') as f:
    json.dump(index, f, indent=2)

print(f"Updated memory index with {len(memory_files)} files")
EOF

# 3. 同步GitHub
cd "$WORKSPACE"
if [ -d ".git" ]; then
    git add .
    git commit -m "Memory maintenance - $DATE" || true
    git push origin main || true
fi

echo "[$(date)] Memory maintenance completed!"