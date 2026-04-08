# AI竞品分析器 - 完整代码文档

> 项目路径：`/home/admin/projects/ai-product-analyzer/`
> 生成时间：2026-04-08

---

## 项目结构

```
ai-product-analyzer/
├── src/
│   ├── main.py              # 主入口
│   ├── api_scraper.py       # API抓取器
│   ├── selenium_scraper.py  # Selenium浏览器抓取器
│   ├── database.py          # SQLite数据持久化
│   ├── comparator.py        # 竞品对比分析
│   ├── user_profiler.py     # 用户画像生成
│   └── priority_sorter.py   # 需求优先级排序
├── data/                    # 数据存储目录
└── README.md                # 项目说明
```

---

## 依赖安装

```bash
pip3 install selenium requests openpyxl
```

---

## 1. 主入口模块 (main.py)

**功能**：整合所有功能模块，提供统一命令行接口

**使用方式**：
```bash
python3 src/main.py                    # 完整流程
python3 src/main.py --api-only         # 仅运行API抓取
python3 src/main.py --test             # 运行测试
python3 src/main.py --db-stats         # 查看数据库统计
python3 src/main.py --search "关键词"   # 搜索产品
python3 src/main.py --compare "A, B"   # 对比产品
python3 src/main.py --list-products    # 列出所有产品
```

---

## 2. API抓取器 (api_scraper.py)

**功能**：使用Product Hunt和GitHub API获取AI产品信息

**主要方法**：
- `scrape_product_hunt()` - 抓取Product Hunt上的AI产品
- `scrape_github_trending()` - 抓取GitHub热门AI项目
- `scrape_all()` - 抓取所有API数据源

**数据字段**：platform, name, description, url, stars, forks, topics, category, scraped_at

---

## 3. Selenium抓取器 (selenium_scraper.py)

**功能**：使用浏览器自动化绕过反爬机制

**主要方法**：
- `scrape_product_hunt()` - 抓取Product Hunt首页产品
- `scrape_github_trending()` - 抓取GitHub Trending页面
- `close()` - 关闭浏览器

**环境要求**：Chrome/Chromium浏览器 + ChromeDriver驱动

---

## 4. 数据库模块 (database.py)

**功能**：SQLite数据持久化、去重和全量覆盖更新

**主要方法**：
- `insert_products()` - 批量插入产品数据（全量覆盖模式）
- `get_all_products()` - 获取所有产品数据
- `search_products()` - 搜索产品
- `get_statistics()` - 获取数据库统计信息
- `export_to_json()` - 导出所有数据到JSON

**表结构**：
- `products` - 产品信息主表
- `scrape_logs` - 抓取日志表

---

## 5. 竞品对比分析模块 (comparator.py)

**功能**：支持多产品横向对比、优劣势分析和可视化报告生成

**主要方法**：
- `list_available_products()` - 列出可用于对比的产品
- `compare_products()` - 对比多个产品
- `generate_comparison_table()` - 生成对比表格（Markdown格式）
- `save_comparison_report()` - 保存对比报告

**对比维度**：
- 基础信息（平台、语言、Stars、Forks）
- 技术栈对比（共同技术、独有技术）
- SWOT分析（优势、劣势、机会、威胁）

---

## 6. 用户画像模块 (user_profiler.py)

**功能**：基于竞品数据生成目标用户画像

**用户画像类型**：
1. **技术开发者** - 关注技术实现、开源项目
2. **商业用户** - 关注商业价值、ROI
3. **普通用户** - 非技术背景，希望快速使用
4. **企业级用户** - 需要大规模部署、高可用性

---

## 7. 需求优先级模块 (priority_sorter.py)

**功能**：基于竞品分析和用户画像，生成需求优先级建议

**需求类型**：
- `core_function` - 核心功能（权重1.5）
- `user_experience` - 用户体验（权重1.3）
- `technical` - 技术优化（权重1.0）
- `business` - 商业化（权重1.2）
- `security` - 安全合规（权重1.4）

**优先级分级**：
- **P0** - 必须做（最高优先级）
- **P1** - 应该做（高优先级）
- **P2** - 可以做（中优先级）
- **P3** - 暂缓（低优先级）

---

## 功能状态

| 模块 | 状态 | 说明 |
|------|------|------|
| API抓取器 | ✅ 正常 | 已测试通过 |
| Selenium抓取器 | ⚠️ 需环境 | 需要Chrome和ChromeDriver |
| 数据持久化 | ✅ 正常 | SQLite数据库 |
| 竞品对比分析 | ✅ 正常 | 支持SWOT分析 |
| 用户画像生成 | ✅ 正常 | 4类用户画像 |
| 需求优先级排序 | ✅ 正常 | P0-P3分级 |

---

## 完整代码

由于代码较长，以下是各模块的核心代码片段。如需完整代码文件，请告知具体需要哪个模块。

### main.py 核心类

```python
class AIProductAnalyzer:
    def __init__(self, product_hunt_token=None, github_token=None, use_db=True):
        self.product_hunt_token = product_hunt_token
        self.github_token = github_token
        self.use_db = use_db
        self.all_data = []
        self.db = ProductDatabase() if use_db else None
    
    def run_full_pipeline(self):
        # 阶段1: API抓取
        api_results = self.run_api_scraper()
        self.all_data.extend(api_results)
        
        # 阶段2: Selenium抓取
        selenium_results = self.run_selenium_scraper()
        self.all_data.extend(selenium_results)
        
        # 阶段3: 竞品分析
        report = self.run_competitor_analysis()
        
        # 阶段4: 数据分析
        analysis = self.run_analytics()
        
        # 阶段5: 数据导出
        self.run_export(analysis)
        
        return report
```

### api_scraper.py 核心方法

```python
class APIScraper:
    def scrape_github_trending(self, language="python", max_items=10):
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "AI OR artificial-intelligence OR machine-learning",
            "sort": "stars",
            "order": "desc",
            "per_page": max_items
        }
        response = requests.get(url, params=params, timeout=10)
        # 解析数据...
```

### database.py 核心方法

```python
class ProductDatabase:
    def insert_products(self, products):
        # 使用 INSERT OR REPLACE 实现全量覆盖
        cursor.execute('''
            INSERT OR REPLACE INTO products 
            (name, platform, tagline, description, url, ...)
            VALUES (...)
        ''', data)
```

### comparator.py 核心方法

```python
class ProductComparator:
    def compare_products(self, product_names):
        # 获取产品详情
        products = [self.get_product_details(name) for name in product_names]
        
        # 执行各项对比分析
        comparison = {
            'products': products,
            'basic_comparison': self._compare_basic_info(products),
            'metrics_comparison': self._compare_metrics(products),
            'tech_stack_comparison': self._compare_tech_stack(products),
            'swot_analysis': self._generate_swot_analysis(products)
        }
        return comparison
```

### user_profiler.py 核心方法

```python
class UserProfiler:
    def generate_personas(self):
        products = self.db.get_all_products(limit=200)
        
        personas = {
            'technical_users': self._analyze_technical_users(products),
            'business_users': self._analyze_business_users(products),
            'casual_users': self._analyze_casual_users(products),
            'enterprise_users': self._analyze_enterprise_users(products)
        }
        return personas
```

### priority_sorter.py 核心方法

```python
class PrioritySorter:
    def calculate_priority_score(self, requirement):
        impact_scores = {'低': 1, '中': 3, '高': 5}
        cost_scores = {'低': 5, '中': 3, '高': 1}
        
        user_impact = impact_scores.get(requirement['user_impact'], 3)
        competitive = impact_scores.get(requirement['competitive_pressure'], 3)
        cost = cost_scores.get(requirement['implementation_cost'], 3)
        
        type_weight = self.REQUIREMENT_TYPES.get(requirement['type'], {}).get('weight', 1.0)
        
        score = (user_impact * 0.4 + competitive * 0.3 + cost * 0.3) * type_weight * 10
        return round(score, 1)
```

---

*文档由AI助手自动生成*
