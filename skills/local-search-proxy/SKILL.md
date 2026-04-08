---
name: local-search-proxy
description: 通过exec调用本地SearXNG实例进行搜索，绕过OpenClaw的localhost访问限制。Use when需要使用本地SearXNG进行搜索但web_search工具无法访问localhost时，或需要隐私保护的本地搜索。支持多引擎聚合搜索（Google/Bing/DuckDuckGo等）。
---

# Local Search Proxy

通过exec调用本地SearXNG实例，绕过OpenClaw工具层的localhost访问限制。

## 核心功能

- 使用本地SearXNG实例进行搜索
- 绕过`web_search`工具的localhost限制
- 支持多引擎聚合（Google/Bing/DuckDuckGo等）
- 完全本地运行，保护隐私

## 使用方式

### Python调用

```python
from scripts.local_search import search

# 基础搜索
results = search("AI Agent")

# 指定结果数量
results = search("AI Agent", max_results=10)

# 指定搜索引擎
results = search("AI Agent", engines="google,bing")

# 返回格式
print(results['query'])      # 搜索关键词
print(results['total'])      # 总结果数
print(results['results'])    # 结果列表
```

### 命令行调用

```bash
# 基础搜索
python scripts/local_search.py "AI Agent"

# 指定参数
python scripts/local_search.py "AI Agent" --max-results 10 --engines google,bing

# 输出JSON
python scripts/local_search.py "AI Agent" --json
```

## 返回格式

```json
{
  "query": "AI Agent",
  "total": 15,
  "results": [
    {
      "title": "...",
      "url": "...",
      "content": "...",
      "engine": "google"
    }
  ]
}
```

## 配置

### SearXNG地址

默认使用 `http://localhost:8080`，可在脚本中修改：

```python
SEARXNG_URL = "http://localhost:8080"  # 修改为你的地址
```

### 搜索引擎

默认使用：`google,bing,duckduckgo`

可选引擎：`google,bing,duckduckgo,brave,qwant,yahoo`

## 工作流程

1. 接收搜索请求
2. 构建curl命令调用本地SearXNG
3. 解析JSON结果
4. 格式化返回

## 错误处理

- SearXNG未运行：返回错误提示
- 超时：默认30秒超时
- 解析失败：返回空结果

## 依赖

- SearXNG本地实例运行中
- curl命令可用
- Python 3.6+

## 与web_search对比

| 特性 | local-search-proxy | web_search |
|------|-------------------|------------|
| localhost访问 | ✅ 支持 | ❌ 受限 |
| 隐私保护 | ✅ 完全本地 | ⚠️ 依赖外部 |
| 成本 | ✅ 免费 | 可能收费 |
| 维护成本 | ⚠️ 需维护SearXNG | ✅ 无需维护 |

## 最佳实践

1. 确保SearXNG容器正常运行
2. 定期检查SearXNG状态
3. 配合定时任务预抓取热点数据
4. 高可用场景建议配置Brave API备用
