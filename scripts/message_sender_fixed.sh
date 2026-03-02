#!/bin/bash
# 修复版通用消息推送脚本
# 用法: ./message_sender_fixed.sh "标题" < content_file

TITLE="$1"
CONTENT_FILE="$2"

# 读取内容文件
if [ -f "$CONTENT_FILE" ]; then
    CONTENT=$(cat "$CONTENT_FILE")
else
    echo "Error: Content file not found"
    exit 1
fi

# 直接使用OpenClaw的message工具发送到当前飞书对话
# 注意：这需要在OpenClaw环境中执行，不能在独立shell中运行

echo "准备发送消息到飞书..."
echo "标题: $TITLE"
echo "内容长度: $(echo "$CONTENT" | wc -c) 字符"

# 由于在shell脚本中无法直接调用OpenClaw工具，
# 我们需要通过主程序来处理
# 创建标记文件通知主程序发送消息

mkdir -p /home/admin/.openclaw/workspace/messages/to_send
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cat > "/home/admin/.openclaw/workspace/messages/to_send/${TIMESTAMP}.json" << EOF
{
  "title": "$TITLE",
  "content": "$CONTENT",
  "channel": "feishu",
  "timestamp": "$(date -Iseconds)"
}
EOF

echo "消息已准备就绪，等待主程序发送"