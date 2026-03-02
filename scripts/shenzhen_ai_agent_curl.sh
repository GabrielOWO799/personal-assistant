#!/bin/bash
# 深圳AI Agent实习岗位链接推送脚本 - 方案A
# 使用curl直接调用SearXNG，避免Python兼容性问题

set -e

# 日志函数
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log_message "=== 深圳AI Agent实习岗位链接推送开始 ==="

# 创建临时文件
TEMP_FILE="/tmp/shenzhen_ai_agent_$(date +%Y%m%d_%H%M%S).md"
REPORT_FILE="/tmp/shenzhen_ai_agent_report_$(date +%Y%m%d_%H%M%S).md"

# 搜索关键词列表
KEYWORDS=(
    "深圳 AI Agent 实习"
    "深圳 智能体开发 实习"
    "深圳 大模型应用 实习"
    "深圳 LangChain 实习"
    "深圳 AutoGen 实习"
    "深圳 RAG 实习"
    "深圳 Prompt Engineering 实习"
    "深圳 LLM 应用 实习"
    "深圳 人工智能 实习"
    "AI Agent intern 深圳"
)

# 存储所有结果
ALL_RESULTS=""

# 搜索每个关键词
for keyword in "${KEYWORDS[@]}"; do
    log_message "搜索: $keyword"
    
    # URL编码关键词
    ENCODED_KEYWORD=$(echo "$keyword" | sed 's/ /%20/g')
    
    # 使用curl调用SearXNG
    RESPONSE=$(curl -s "http://localhost:8080/search?q=${ENCODED_KEYWORD}&format=json&language=zh&time_range=day&categories=jobs" 2>/dev/null || echo "{}")
    
    if [ -n "$RESPONSE" ] && [ "$RESPONSE" != "{}" ]; then
        # 提取标题和URL
        TITLES=$(echo "$RESPONSE" | python3 -c "
import json
import sys
try:
    data = json.load(sys.stdin)
    results = data.get('results', [])
    for result in results[:3]:  # 每个关键词取前3个结果
        title = result.get('title', '').strip()
        url = result.get('url', '').strip()
        if title and url:
            print(f'- [{title}]({url})')
except:
    pass
" 2>/dev/null || true)
        
        if [ -n "$TITLES" ]; then
            ALL_RESULTS="$ALL_RESULTS$TITLES"$'\n'
        fi
    fi
    
    # 避免请求过于频繁
    sleep 1
done

# 去重（基于URL）
if [ -n "$ALL_RESULTS" ]; then
    echo "$ALL_RESULTS" | sort -u > "$TEMP_FILE"
else
    echo "暂无符合要求的深圳AI Agent实习岗位信息" > "$TEMP_FILE"
fi

# 生成最终报告
cat > "$REPORT_FILE" << EOF
# 🤖 深圳AI Agent实习岗位日报 - $(date +%Y年%m月%d日)

## 🔍 今日精选AI Agent相关实习岗位链接

> **专注领域**: AI Agent、智能体开发、大模型应用、Agent框架(LangChain/AutoGen/CrewAI)、RAG、Prompt Engineering

EOF

# 添加搜索结果（最多10个）
head -10 "$TEMP_FILE" >> "$REPORT_FILE"

cat >> "$REPORT_FILE" << EOF

---
由太太自动推送于 $(date)
专注为你寻找最优质的AI Agent实习机会 💪
EOF

# 输出结果
cat "$REPORT_FILE"

# 清理临时文件
rm -f "$TEMP_FILE" "$REPORT_FILE"

log_message "=== 深圳AI Agent实习岗位链接推送完成 ==="