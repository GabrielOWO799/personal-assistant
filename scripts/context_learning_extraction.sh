#!/bin/bash
# 上下文学习与记忆提取任务 - 每日执行
# 使用proactive-agent的WAL协议和Working Buffer

cd /home/admin/.openclaw/workspace

# 创建日志目录
mkdir -p logs

# 设置日志文件
LOG_FILE="logs/context_learning_$(date +%Y%m%d).log"
echo "=== Context Learning Extraction Task Started ===" >> "$LOG_FILE"
echo "Execution Time: $(date)" >> "$LOG_FILE"

# 执行上下文提取
python3 -c "
from context_learning_extractor import run_context_extraction
try:
    result = run_context_extraction()
    print(f'Context extraction completed: {result}')
except Exception as e:
    print(f'Context extraction failed: {e}')
    exit(1)
" >> "$LOG_FILE" 2>&1

# 检查执行结果
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "✅ Context learning extraction completed successfully" >> "$LOG_FILE"
    echo "Context learning extraction completed at $(date)" >> memory/$(date +%Y-%m-%d).md 2>/dev/null || true
else
    echo "❌ Context learning extraction failed" >> "$LOG_FILE"
    exit 1
fi

echo "=== Context Learning Extraction Task Completed ===" >> "$LOG_FILE"