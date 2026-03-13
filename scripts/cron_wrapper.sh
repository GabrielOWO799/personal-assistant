#!/bin/bash
# 通用定时任务包装器，添加错误处理和日志记录

SCRIPT_NAME=$(basename "$1")
LOG_DIR="/home/admin/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"

# 执行脚本并记录日志
"$@" 2>&1 | tee -a "$LOG_DIR/${SCRIPT_NAME%.*}_$(date +%Y%m%d).log"

# 检查执行结果
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Task $SCRIPT_NAME failed at $(date)" >> "$LOG_DIR/task_failures.log"
    exit 1
else
    echo "✅ Task $SCRIPT_NAME completed at $(date)" >> "$LOG_DIR/task_success.log"
fi