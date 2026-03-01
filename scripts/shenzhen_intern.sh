#!/bin/bash
# 深圳实习岗位推送脚本 - 14:00
cd /home/admin/.openclaw/workspace

# 使用 SearXNG 搜索深圳实习岗位
echo "正在搜索深圳实习岗位信息..."

# 执行搜索并保存结果
python3 scripts/searxng_search.py "深圳 实习岗位" "jobs" "zh" 15 > /tmp/shenzhen_intern_today.json

# 检查搜索结果
if [ ! -f "/tmp/shenzhen_intern_today.json" ]; then
    echo "搜索失败，使用备用数据"
    echo '{"results": [{"title": "暂无最新深圳实习岗位", "url": "#", "content": "请稍后再试", "engine": "备用数据", "published_date": "未知"}]}' > /tmp/shenzhen_intern_today.json
fi

# 生成消息内容
REPORT_FILE="/tmp/shenzhen_intern_report_$(date +%Y%m%d).md"
cat > "$REPORT_FILE" << EOF
# 📋 深圳实习岗位日报 - $(date +%Y年%m月%d日)

## 🔍 今日精选实习岗位

EOF

# 添加岗位信息
python3 -c "
import json
with open('/tmp/shenzhen_intern_today.json', 'r') as f:
    data = json.load(f)

if 'results' in data and len(data['results']) > 0:
    for i, result in enumerate(data['results'][:10], 1):
        title = result.get('title', '无标题')
        url = result.get('url', '#')
        content = result.get('content', '无内容')
        published_date = result.get('published_date', '未知时间')
        engine = result.get('engine', '未知来源')
        
        print(f'### {i}. [{title}]({url})')
        print(f'- **发布时间**: {published_date}')
        print(f'- **来源**: {engine}')
        print(f'- **详情**: {content[:150]}...')
        print()
else:
    print('暂无最新深圳实习岗位信息')
"

cat >> "$REPORT_FILE" << EOF

---
由太太自动推送于 $(date)
EOF

# 发送消息到Feishu
./scripts/message_sender.sh "深圳实习岗位日报" "$REPORT_FILE"

echo "深圳实习岗位信息已成功推送！"

# 记录执行日志
echo "深圳实习岗位推送执行于 $(date)" >> memory/$(date +%Y-%m-%d).md 2>/dev/null || touch memory/$(date +%Y-%m-%d).md && echo "深圳实习岗位推送执行于 $(date)" >> memory/$(date +%Y-%m-%d).md