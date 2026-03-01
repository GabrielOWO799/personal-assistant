#!/bin/bash
# 通用消息推送脚本
# 用法: ./message_sender.sh "标题" < content_file

TITLE="$1"
CONTENT_FILE="$2"

# 使用OpenClaw的message工具发送到Feishu
# 由于我们是在Feishu环境中，可以直接使用message工具

# 读取内容文件
if [ -f "$CONTENT_FILE" ]; then
    CONTENT=$(cat "$CONTENT_FILE")
else
    echo "Error: Content file not found"
    exit 1
fi

# 创建临时消息文件
echo "$CONTENT" > /tmp/message_content.txt

# 这里需要调用OpenClaw的message工具
# 但在shell脚本中无法直接调用，需要通过其他方式
# 临时解决方案：将内容保存到特定位置，由主程序读取并发送

mkdir -p /home/admin/.openclaw/workspace/messages/pending
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo "Title: $TITLE" > "/home/admin/.openclaw/workspace/messages/pending/${TIMESTAMP}.msg"
echo "Content:" >> "/home/admin/.openclaw/workspace/messages/pending/${TIMESTAMP}.msg"
echo "$CONTENT" >> "/home/admin/.openclaw/workspace/messages/pending/${TIMESTAMP}.msg"
echo "" >> "/home/admin/.openclaw/workspace/messages/pending/${TIMESTAMP}.msg"
echo "Channel: feishu" >> "/home/admin/.openclaw/workspace/messages/pending/${TIMESTAMP}.msg"

echo "Message queued for delivery: $TITLE"