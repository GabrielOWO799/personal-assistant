# Active Patterns

## Pattern 1: 定时任务超时导致推送失败
category: process
frequency: 10+ occurrences
status: monitoring

**Pattern:** AI日报任务频繁超时（120秒不够用），导致内容生成后无法推送
**Root:** 超时时间配置没有根据实际执行时间调整，搜索+生成需要150-210秒
**Prevention:** 
- 所有定时任务必须评估实际执行时间
- 推送类任务超时 ≥ 300秒
- 添加 `bestEffort: true` 确保重试
**Last seen:** 2026-03-22
**Streak:** 0 days (just fixed)

---

## Pattern 2: 推送失败未及时发现

**Pattern:** 用户反馈后才发现推送失败，缺乏主动监控
**Root:** 没有建立每日检查任务执行状态的机制
**Prevention:** 
- 心跳检查时必须查看关键任务的最近执行状态
- 连续失败2次时主动提醒用户
- 在MEMORY.md记录待验证事项
**Last seen:** 2026-03-22
**Streak:** 0 days

## Pattern 3: 排查问题不系统

category: assumptions
frequency: 2 occurrences
status: emerging

**Pattern:** 用户要求"彻底检查"时，只排查单一环节，没有系统性分析全链路
**Root:** 容易陷入惯性思维，假设问题在某处，忽略了其他可能性
**Prevention:** 
- 遇到"彻底检查"必须列出全链路检查清单
- 生成→推送→送达，每个环节都要验证
- 提供完整的根因分析报告
**Last seen:** 2026-03-22
**Streak:** 0 days

---

## Pattern 4: 回答不够主动完整

category: scope
frequency: 2 occurrences
status: emerging

**Pattern:** 回答用户询问时过于简短，没有主动提供完整信息和后续价值
**Root:** 等待用户追问才提供更多信息，缺乏主动服务意识
**Prevention:** 
- 用户问"有没有"时，提供「是什么+能做什么+怎么用」
- 预判用户可能需要的下一步信息
- 主动询问"需要我帮你设置吗？"
**Last seen:** 2026-03-22
**Streak:** 0 days

---

*Patterns are detected after 3 similar reflections*
