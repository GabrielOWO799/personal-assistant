#!/bin/bash
# 错误处理和重试机制

# 日志函数
log_error() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] $1" >> /home/admin/.openclaw/workspace/logs/error.log
}

log_info() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1" >> /home/admin/.openclaw/workspace/logs/error.log
}

# 重试函数
retry_command() {
    local cmd="$1"
    local max_retries=${2:-3}
    local delay=${3:-5}
    
    for i in $(seq 1 $max_retries); do
        log_info "Attempt $i: $cmd"
        if eval "$cmd"; then
            log_info "Command succeeded on attempt $i"
            return 0
        else
            log_error "Command failed on attempt $i"
            if [ $i -lt $max_retries ]; then
                sleep $delay
            fi
        fi
    done
    
    log_error "Command failed after $max_retries attempts: $cmd"
    return 1
}

# 环境检查
check_environment() {
    log_info "Checking environment..."
    
    # 检查Python路径
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 not found"
        return 1
    fi
    
    # 检查工作目录
    if [ ! -d "/home/admin/.openclaw/workspace" ]; then
        log_error "Workspace directory not found"
        return 1
    fi
    
    # 检查日志目录
    mkdir -p /home/admin/.openclaw/workspace/logs
    
    log_info "Environment check passed"
    return 0
}

# 发送错误通知
send_error_notification() {
    local error_msg="$1"
    local task_name="$2"
    
    log_error "Sending error notification for $task_name: $error_msg"
    
    # 创建错误通知文件
    mkdir -p /home/admin/.openclaw/workspace/messages/errors
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    cat > "/home/admin/.openclaw/workspace/messages/errors/${TIMESTAMP}_error.json" << EOF
{
  "task": "$task_name",
  "error": "$error_msg",
  "timestamp": "$(date -Iseconds)",
  "status": "requires_attention"
}
EOF
}