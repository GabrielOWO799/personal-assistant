#!/bin/bash
# 聊天记录学习分析任务 - 每日执行
# 使用proactive-agent的WAL协议和Working Buffer

cd /home/admin/.openclaw/workspace

# 创建日志目录
mkdir -p logs

# 设置日志文件
LOG_FILE="logs/chat_analysis_$(date +%Y%m%d).log"
echo "=== Chat Analysis Processing Task Started ===" >> "$LOG_FILE"
echo "Execution Time: $(date)" >> "$LOG_FILE"

# 执行聊天分析
python3 -c "
from chat_analysis_processor import run_chat_analysis
try:
    result = run_chat_analysis()
    print(f'Chat analysis completed: {result}')
except Exception as e:
    print(f'Chat analysis failed: {e}')
    exit(1)
" >> "$LOG_FILE" 2>&1

# 检查执行结果
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "✅ Chat analysis processing completed successfully" >> "$LOG_FILE"
    echo "Chat analysis processing completed at $(date)" >> memory/$(date +%Y-%m-%d).md 2>/dev/null || true
else
    echo "❌ Chat analysis processing failed" >> "$LOG_FILE"
    exit 1
fi

echo "=== Chat Analysis Processing Task Completed ===" >> "$LOG_FILE"