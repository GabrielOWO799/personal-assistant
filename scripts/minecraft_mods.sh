#!/bin/bash
# Minecraft 模组推荐 - 每周日 9:00
cd /home/admin/.openclaw/workspace

# 使用 SearXNG 搜索最新的 Minecraft 模组
python3 -m searxng search "Minecraft mods 2026" --category news --time-range week -n 5 > /tmp/mc_mods.json

# 格式化并发送消息
MESSAGE="🎮 **本周 Minecraft 模组推荐** 🎮\n\n"
while read -r line; do
    if [[ "$line" == *"title"* ]]; then
        title=$(echo "$line" | sed 's/.*"title": "\(.*\)".*/\1/')
        MESSAGE+="- $title\n"
    fi
done < /tmp/mc_mods.json

# 发送消息（需要配置实际的消息发送方式）
echo "$MESSAGE" > /tmp/mc_mods_message.md

# 清理临时文件
rm /tmp/mc_mods.json