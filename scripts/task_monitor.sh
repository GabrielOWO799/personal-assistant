#!/bin/bash
# 任务监控脚本 - 每12小时检查关键定时任务状态

cd /home/admin/.openclaw/workspace

# 检查今日AI日报是否已生成
TODAY=$(date +%Y-%m-%d)
AI_REPORT_LOG="/tmp/daily_report_${TODAY//\-/}.md"

if [ ! -f "$AI_REPORT_LOG" ]; then
    # 检查日志中是否有今日的AI日报记录
    if ! grep -q "AI Agent Daily Report generated at.*$TODAY" memory/$TODAY.md 2>/dev/null; then
        echo "⚠️ AI日报任务可能未执行！"
        # 尝试手动执行
        echo "正在尝试手动执行AI日报任务..."
        /home/admin/.openclaw/workspace/scripts/ai_agent_daily.sh
    fi
fi

# 检查GitHub同步状态
if [ -f ".github_sync_config" ]; then
    if ! git remote get-url origin >/dev/null 2>&1; then
        echo "⚠️ GitHub同步配置有问题！"
    fi
fi

# 检查内存维护状态
if [ ! -f "memory/index.json" ]; then
    echo "⚠️ 内存维护未执行！"
fi

# 记录监控结果
echo "✅ 任务监控完成于 $(date)" >> memory/heartbeat-state.json