# 销售数据分析器

## 功能特性
- ✅ 自动检测并创建示例CSV文件
- ✅ 读取CSV数据并计算统计信息
- ✅ 自动生成折线图和柱状图
- ✅ 自动安装matplotlib依赖
- ✅ 完整的异常处理
- ✅ 提供CSV导入接口

## 使用方法

### 基本使用
```bash
python sales_analyzer.py
```

### 导入自定义CSV文件
```python
from sales_analyzer import import_local_csv

# 导入本地CSV文件
data = import_local_csv("your_file.csv")
if data:
    # 处理数据
    print(f"成功导入 {len(data)} 行数据")
```

## 输出文件
- `data.csv` - 示例数据文件（如果不存在）
- `sales_line_chart.png` - 销售额趋势折线图
- `sales_bar_chart.png` - 每日销售额柱状图

## 依赖
- Python 3.6+
- matplotlib (自动安装)
- csv (Python内置)