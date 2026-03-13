#!/bin/bash
# 分布式搜索汇总推送任务 - 使用proactive-agent模式

cd /home/admin/.openclaw/workspace

# 创建必要的目录
mkdir -p logs working_buffer wal_logs

# 设置Python路径
PYTHON_PATH="/usr/bin/python3.8"

# 执行聚合任务
$PYTHON_PATH -c "
import sys
sys.path.append('/home/admin/.openclaw/workspace')
from distributed_search_aggregator import run_daily_aggregation
result = run_daily_aggregation()
print('Aggregation result:', result)
"

# 记录执行日志
echo \"Distributed search aggregation completed at \$(date)\" >> memory/\$(date +%Y-%m-%d).md