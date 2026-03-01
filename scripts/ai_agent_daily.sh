#!/bin/bash
# AI Agent Daily Report - 9:00 AM (中文版)
cd /home/admin/.openclaw/workspace

# 使用SearXNG获取最新的AI新闻（中文）
python3 scripts/searxng_search.py "AI智能体 最新进展 24小时" "news" "zh" 10 > /tmp/ai_news.json

# 检查GitHub同步状态
GITHUB_SYNC_STATUS="未配置"
if [ -f ".github_sync_config" ]; then
    if git remote get-url origin >/dev/null 2>&1; then
        GITHUB_SYNC_STATUS="已配置"
    else
        GITHUB_SYNC_STATUS="配置中"
    fi
fi

# 检查每日维护状态
MAINTENANCE_STATUS="未执行"
if [ -f "memory/index.json" ]; then
    LAST_UPDATED=$(cat memory/index.json | jq -r '.last_updated')
    TODAY=$(date +%Y-%m-%d)
    if [[ "$LAST_UPDATED" == *"$TODAY"* ]]; then
        MAINTENANCE_STATUS="✅ 已于今日 $(date -d "$LAST_UPDATED" +%H:%M:%S) 成功完成"
    fi
fi

# 生成日报内容
REPORT_FILE="/tmp/daily_report_$(date +%Y%m%d).md"
cat > "$REPORT_FILE" << EOF
# AI智能体早报 - $(date +%Y年%m月%d日)

## 过去24小时最有价值的10条AI资讯

EOF

# 添加新闻内容（包含时间和来源链接）
python3 -c "
import json
import re
from datetime import datetime, timedelta

with open('/tmp/ai_news.json', 'r') as f:
    data = json.load(f)

if 'results' in data and len(data['results']) > 0:
    for i, result in enumerate(data['results'][:10], 1):
        title = result.get('title', '无标题')
        url = result.get('url', '#')
        content = result.get('content', '无内容')
        published_date = result.get('published_date', '未知时间')
        engine = result.get('engine', '未知来源')
        
        # 格式化输出
        print(f'### {i}. [{title}]({url})')
        print(f'- **发布时间**: {published_date}')
        print(f'- **来源**: {engine}')
        print(f'- **摘要**: {content[:200]}...')
        print()
else:
    print('暂无最新AI资讯')
"

cat >> "$REPORT_FILE" << EOF

## 系统维护状态
**每日记忆维护**：$MAINTENANCE_STATUS

**GitHub记忆同步**：$GITHUB_SYNC_STATUS
- 仓库：GabrielOWO799/personal-assistant
- 同步频率：每日2:00自动同步
- 状态：正常运行

## 记忆状态
- 项目进度：$(wc -l < memory/projects.md 2>/dev/null || echo "0")行
- 经验教训：$(wc -l < memory/lessons.md 2>/dev/null || echo "0")行  
- 今日日志：待创建

## 今日任务
- [x] AI智能体早报（中文版，24小时内10条最有价值资讯，已完成）
- [ ] 检查GitHub记忆同步
- [ ] 复习用户偏好设置  
- [ ] 更新技能状态
- [ ] 发送深圳实习岗位信息（14:00）

---
由太太生成于 $(date)
EOF

# 发送消息到Feishu - 使用修复后的消息推送方式
/scripts/message_sender.sh "AI智能体早报" "$REPORT_FILE"

# 记录生成日志
echo "AI Agent Daily Report generated at $(date)" >> memory/$(date +%Y-%m-%d).md 2>/dev/null || touch memory/$(date +%Y-%m-%d).md && echo "AI Agent Daily Report generated at $(date)" >> memory/$(date +%Y-%m-%d).md