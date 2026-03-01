#!/bin/bash
# AI Weekly Report - 每周日 10:00
cd /home/admin/.openclaw/workspace

# 获取本周日期范围（上周日到本周六）
END_DATE=$(date +%Y-%m-%d)
START_DATE=$(date -d "last sunday" +%Y-%m-%d)

# 使用SearXNG搜索本周AI新闻
python3 scripts/searxng_search.py "AI 人工智能 最新进展 2026" "news" "zh" 15 > /tmp/ai_weekly_news.json

# 生成周报内容
REPORT_FILE="/tmp/ai_weekly_report_$(date +%Y%m%d).md"
cat > "$REPORT_FILE" << EOF
# 📊 AI智能体周报精华 - $(date +%Y年%m月%d日)

## 本周最有价值的五条AI资讯（$START_DATE 至 $END_DATE）

EOF

# 处理搜索结果并提取最重要的5条
python3 -c "
import json
import re
from datetime import datetime

with open('/tmp/ai_weekly_news.json', 'r') as f:
    data = json.load(f)

if 'results' in data and len(data['results']) > 0:
    # 根据标题关键词重要性排序
    important_keywords = ['产业', '机器人', '算力', '医疗', '趋势', '应用', '规模', '市场']
    results_with_score = []
    
    for result in data['results']:
        score = 0
        title = result.get('title', '').lower()
        content = result.get('content', '').lower()
        
        for keyword in important_keywords:
            if keyword in title or keyword in content:
                score += 1
        
        results_with_score.append((score, result))
    
    # 按分数排序，取前5个
    results_with_score.sort(key=lambda x: x[0], reverse=True)
    top_results = [result for score, result in results_with_score[:5]]
    
    for i, result in enumerate(top_results, 1):
        title = result.get('title', '无标题')
        url = result.get('url', '#')
        content = result.get('content', '无内容')
        published_date = result.get('published_date', '未知时间')
        engine = result.get('engine', '未知来源')
        
        print(f'### {i}. [{title}]({url})')
        print(f'- **发布时间**: {published_date}')
        print(f'- **来源**: {engine}')
        print(f'- **摘要**: {content[:200]}...')
        print()
else:
    print('本周暂无AI相关重要资讯')
"

# 添加趋势分析部分
cat >> "$REPORT_FILE" << EOF

## 🔮 代表的核心趋势

### 🚀 趋势一：AI产业化加速
2026年是AI从实验室走向大规模商业应用的转折点，产业格局正在重塑。

### 🤖 趋势二：具身智能崛起  
AI不再局限于软件层面，而是通过人形机器人等载体进入物理世界。

### 💼 趋势三：经济影响深化
AI开始对传统行业、就业市场和资本市场产生实质性影响。

### ⚡ 趋势四：算力军备竞赛
算力基础设施成为国家战略和企业竞争的核心。

### 🏥 趋势五：垂直领域突破
AI在医疗、金融、制造等垂直领域开始产生实际业务价值。

---
由太太生成于 $(date)
EOF

# 发送消息到Feishu
/scripts/message_sender.sh "AI智能体周报精华" "$REPORT_FILE"

# 记录生成日志
echo "AI Weekly Report generated at $(date)" >> memory/$(date +%Y-%m-%d).md 2>/dev/null || touch memory/$(date +%Y-%m-%d).md && echo "AI Weekly Report generated at $(date)" >> memory/$(date +%Y-%m-%d).md