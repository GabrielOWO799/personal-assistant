# 深圳AI Agent实习岗位推荐技能

## 描述
专门用于每天自动搜集和推送深圳地区AI Agent相关实习岗位的技能。使用优化的搜索策略、改进的数据提取和智能去重过滤。

## 触发条件
当用户提到以下关键词时激活：
- 深圳实习
- AI Agent实习  
- 智能体开发实习
- 大模型实习
- LangChain/AutoGen/CrewAI/RAG实习

## 功能特性
- ✅ 优化搜索策略：使用site限定符定向搜索主要招聘网站
- ✅ 改进数据提取：从招聘网站提取结构化岗位信息
- ✅ 智能去重过滤：基于标题+公司去重，确保内容新鲜
- ✅ 表格格式输出：包含岗位名称、公司、地点、要求、链接
- ✅ 定时自动推送：每天14:00通过飞书发送

## 依赖
- SearXNG本地实例（端口8080）
- Python 3.8+
- feedparser库（用于RSS解析）
- requests库（用于HTTP请求）

## 配置
定时任务已配置在crontab中：
`0 14 * * * /home/admin/.openclaw/workspace/scripts/cron_wrapper.sh /home/admin/.openclaw/workspace/scripts/shenzhen_ai_agent_intern_optimized.py`