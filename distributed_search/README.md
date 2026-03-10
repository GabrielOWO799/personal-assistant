# 分布式AI实习岗位搜索系统

## 系统架构
本系统采用分布式分时段搜索策略，将原本单次重负载的搜索任务拆分为多个轻量级子任务。

### 搜索时间表
- **09:00** - 搜索"AI Agent"相关岗位
- **10:00** - 搜索"大模型"相关岗位  
- **11:00** - 搜索"智能体"相关岗位
- **12:00** - 搜索"提示词"相关岗位
- **14:00** - 汇总所有结果，生成完整日报

### 目录结构
```
distributed_search/
├── search_buffer/          # 临时存储各时段搜索结果
├── final_report/           # 最终日报存储
├── search_manager.py       # 核心搜索管理器
├── config.py              # 系统配置
└── README.md              # 使用文档
```

## 使用方法

### 手动测试单个搜索
```python
from search_manager import DistributedSearchManager
manager = DistributedSearchManager()
manager.search_phase("AI Agent", "20260310")
```

### 手动汇总结果
```python
from search_manager import DistributedSearchManager  
manager = DistributedSearchManager()
report = manager.aggregate_results("20260310")
print(report)
```

## 定时任务集成
系统设计为与OpenClaw定时任务系统无缝集成，每个搜索阶段和汇总阶段都对应独立的cron job。

## 错误处理
- 单个搜索失败不会影响其他搜索任务
- 汇总时会检查所有搜索结果的完整性
- 支持手动重试失败的搜索任务