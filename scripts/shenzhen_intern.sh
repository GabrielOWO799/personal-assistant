#!/bin/bash
# 深圳AI Agent实习岗位链接推送脚本 - 14:00
# 方案A：简化版自动推送招聘链接

set -e

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "/home/admin/.openclaw/workspace/logs/shenzhen_intern_$(date +%Y%m%d).log"
}

log_message "=== 深圳AI Agent实习岗位链接推送开始 ==="

# 创建必要的目录
mkdir -p /home/admin/.openclaw/workspace/logs
mkdir -p /home/admin/.openclaw/workspace/messages/pending

# 执行curl版本的搜索脚本
/home/admin/.openclaw/workspace/scripts/shenzhen_ai_agent_curl.sh

log_message "=== 深圳AI Agent实习岗位链接推送完成 ==="