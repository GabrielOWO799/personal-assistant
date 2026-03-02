#!/bin/bash
# 日志工具函数

LOG_DIR="/home/admin/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"

log_info() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1" >> "$LOG_DIR/task_debug.log"
}

log_error() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] $1" >> "$LOG_DIR/task_debug.log"
}

log_debug() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [DEBUG] $1" >> "$LOG_DIR/task_debug.log"
}

# 记录环境信息
log_environment() {
    log_info "=== 环境信息 ==="
    log_info "执行时间: $(date)"
    log_info "当前用户: $(whoami)"
    log_info "工作目录: $(pwd)"
    log_info "Python路径: $(which python3 2>/dev/null || echo 'not found')"
    log_info "Python版本: $(python3 --version 2>/dev/null || echo 'not found')"
    log_info "PATH: $PATH"
    
    # 检查pending消息数量
    PENDING_COUNT=$(ls /home/admin/.openclaw/workspace/messages/pending/ 2>/dev/null | wc -l)
    log_info "Pending消息数量: $PENDING_COUNT"
    
    # 检查to_send消息数量  
    TO_SEND_COUNT=$(ls /home/admin/.openclaw/workspace/messages/to_send/ 2>/dev/null | wc -l)
    log_info "To_send消息数量: $TO_SEND_COUNT"
    log_info "================"
}