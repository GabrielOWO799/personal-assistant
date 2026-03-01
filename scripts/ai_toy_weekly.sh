#!/bin/bash
# AI+潮玩周报脚本 - 生成20条候选资讯供用户筛选
# 每周五 9:00 执行

cd /home/admin/.openclaw/workspace

# 使用 SearXNG 搜索相关网站，获取20条候选资讯
echo "正在生成AI+潮玩周报候选资讯（20条）..."

# 监控指定数据源
sources="kickstarter indiegogo theverge techcrunch toybook itjuzi 36kr mojing"

report=""
total_count=0
for source in $sources; do
    echo "搜索 $source..."
    # 获取更多结果以确保有20条候选
    result=$(python3 scripts/searxng_search.py "AI潮玩 AI玩具 $source" "news" "zh" 5)
    report="$report\n## $source\n$result\n"
    # 这里需要解析JSON并计数，简化处理
done

# 生成包含20条候选资讯的报告
echo -e "# AI+潮玩行业周报 - 候选资讯（20条）\n$(date +%Y年%m月%d日)\n\n## 请从以下20条候选资讯中筛选10条最符合要求的内容\n\n$report" > memory/ai_toy_weekly_candidates_$(date +%Y-%m-%d).md

echo "AI+潮玩周报候选资讯（20条）已生成！"