#!/bin/bash
# 消息发送监控脚本 - 检查pending消息并处理

# 加载日志工具
source /home/admin/.openclaw/workspace/scripts/log_utils.sh

log_info "=== 消息监控脚本启动 ==="
log_info "执行时间: $(date)"
log_info "当前工作目录: $(pwd)"

# 检查pending消息目录
PENDING_DIR="/home/admin/.openclaw/workspace/messages/pending"
TO_SEND_DIR="/home/admin/.openclaw/workspace/messages/to_send"

if [ ! -d "$PENDING_DIR" ]; then
    log_info "Pending目录不存在，创建目录"
    mkdir -p "$PENDING_DIR"
fi

if [ ! -d "$TO_SEND_DIR" ]; then
    log_info "To_send目录不存在，创建目录"
    mkdir -p "$TO_SEND_DIR"
fi

# 统计pending消息数量
PENDING_COUNT=$(ls -1 "$PENDING_DIR"/*.msg 2>/dev/null | wc -l)
if [ "$PENDING_COUNT" = "0" ]; then
    PENDING_COUNT=0
fi

log_info "Pending消息数量: $PENDING_COUNT"

# 如果有pending消息，记录详细信息
if [ "$PENDING_COUNT" -gt 0 ]; then
    log_info "发现pending消息，详细信息："
    for msg_file in "$PENDING_DIR"/*.msg; do
        if [ -f "$msg_file" ]; then
            log_info "文件: $(basename "$msg_file")"
            log_info "大小: $(stat -c%s "$msg_file") 字节"
            log_info "内容预览: $(head -n 3 "$msg_file" | tr '\n' ' ')"
        fi
    done
fi

# 检查Python环境
log_info "Python路径: $(which python3)"
log_info "Python版本: $(python3 --version 2>&1)"

# 检查OpenClaw环境变量
log_info "OpenClaw工作目录: $OPENCLAW_WORKSPACE"
log_info "PATH包含: $(echo $PATH | grep -o '/home/[^:]*' | head -3)"

# 记录系统信息
log_info "系统内存: $(free -h | grep 'Mem:' | awk '{print $2}')"
log_info "磁盘空间: $(df -h / | tail -1 | awk '{print $4}')"

log_info "=== 消息监控脚本结束 ==="