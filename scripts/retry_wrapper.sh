#!/bin/bash
# 重试包装器 - 为任务提供两次重试，每次间隔5分钟

SCRIPT_NAME=$(basename "$1")
LOG_DIR="/home/admin/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"

MAX_RETRIES=2
RETRY_INTERVAL=300  # 5分钟 = 300秒

for ((attempt=0; attempt<=MAX_RETRIES; attempt++)); do
    if [ $attempt -gt 0 ]; then
        echo "[$(date)] Attempt $((attempt + 1))/$((MAX_RETRIES + 1)) for $SCRIPT_NAME" >> "$LOG_DIR/${SCRIPT_NAME%.*}_$(date +%Y%m%d).log"
        sleep $RETRY_INTERVAL
    fi
    
    # 执行脚本
    "$@" 2>&1 | tee -a "$LOG_DIR/${SCRIPT_NAME%.*}_$(date +%Y%m%d).log"
    
    # 检查执行结果
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo "✅ Task $SCRIPT_NAME completed successfully on attempt $((attempt + 1)) at $(date)" >> "$LOG_DIR/task_success.log"
        exit 0
    else
        echo "❌ Task $SCRIPT_NAME failed on attempt $((attempt + 1)) at $(date)" >> "$LOG_DIR/task_failures.log"
        if [ $attempt -eq $MAX_RETRIES ]; then
            echo "💥 Task $SCRIPT_NAME failed after $((MAX_RETRIES + 1)) attempts at $(date)" >> "$LOG_DIR/task_failures.log"
            exit 1
        fi
    fi
done