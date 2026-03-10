#!/usr/bin/env python3
"""
简化版销售数据分析器 - 生成小尺寸图片便于分享
"""

import os
import csv
import sys
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import random


def check_and_install_matplotlib() -> bool:
    """检查matplotlib是否已安装，如果没有则自动安装"""
    try:
        import matplotlib.pyplot as plt
        return True
    except ImportError:
        print("检测到matplotlib未安装，正在自动安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
            print("matplotlib安装成功！")
            return True
        except subprocess.CalledProcessError:
            print("❌ matplotlib安装失败，请手动安装：pip install matplotlib")
            return False


def create_sample_csv(filename: str = "data.csv", rows: int = 10) -> None:
    """创建示例CSV文件"""
    print(f"正在创建示例CSV文件: {filename}")
    
    end_date = datetime.now()
    dates = [(end_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(rows)]
    dates.reverse()
    sales = [random.randint(1000, 10000) for _ in range(rows)]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['日期', '销售额'])
        for date, sale in zip(dates, sales):
            writer.writerow([date, sale])
    
    print(f"✅ 示例CSV文件已创建，包含{rows}行数据")


def load_csv_data(filename: str = "data.csv") -> Optional[List[Dict[str, str]]]:
    """读取CSV文件数据"""
    if not os.path.exists(filename):
        print(f"❌ 文件 {filename} 不存在")
        return None
    
    try:
        data = []
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        print(f"❌ 读取CSV文件时出错: {e}")
        return None


def calculate_statistics(data: List[Dict[str, str]]) -> Dict[str, float]:
    """计算销售额的统计信息"""
    try:
        sales = [float(row['销售额']) for row in data]
        total = sum(sales)
        average = total / len(sales) if sales else 0
        maximum = max(sales) if sales else 0
        minimum = min(sales) if sales else 0
        
        return {'total': total, 'average': average, 'max': maximum, 'min': minimum}
    except (ValueError, KeyError) as e:
        print(f"❌ 计算统计信息时出错: {e}")
        return {'total': 0, 'average': 0, 'max': 0, 'min': 0}


def plot_sales_data_small(data: List[Dict[str, str]], output_prefix: str = "sales_small") -> Tuple[str, str]:
    """绘制小尺寸销售数据图表"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from datetime import datetime
        
        dates = [datetime.strptime(row['日期'], '%Y-%m-%d') for row in data]
        sales = [float(row['销售额']) for row in data]
        
        # 设置小尺寸图表 (800x600 像素)
        plt.rcParams['figure.figsize'] = [8, 6]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 折线图 - 小尺寸
        plt.figure(figsize=(8, 4))
        plt.plot(dates, sales, marker='o', linewidth=1.5, markersize=4)
        plt.title('Sales Trend', fontsize=12)
        plt.xlabel('Date', fontsize=10)
        plt.ylabel('Sales', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()
        line_chart_file = f"{output_prefix}_line.png"
        plt.savefig(line_chart_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        # 柱状图 - 小尺寸
        plt.figure(figsize=(8, 4))
        bars = plt.bar(range(len(dates)), sales, alpha=0.7, color='skyblue')
        plt.title('Daily Sales', fontsize=12)
        plt.xlabel('Date', fontsize=10)
        plt.ylabel('Sales', fontsize=10)
        plt.grid(True, alpha=0.3, axis='y')
        plt.xticks(range(len(dates)), [d.strftime('%m-%d') for d in dates], rotation=45, fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()
        bar_chart_file = f"{output_prefix}_bar.png"
        plt.savefig(bar_chart_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        return line_chart_file, bar_chart_file
        
    except Exception as e:
        print(f"❌ 绘制图表时出错: {e}")
        return "error_line.png", "error_bar.png"


def main():
    """主函数"""
    print("📊 简化版销售数据分析器启动中...")
    
    if not check_and_install_matplotlib():
        print("无法继续执行，请先安装matplotlib")
        return
    
    csv_filename = "data.csv"
    if not os.path.exists(csv_filename):
        create_sample_csv(csv_filename, 10)
    else:
        print(f"✅ 找到现有CSV文件: {csv_filename}")
    
    data = load_csv_data(csv_filename)
    if data is None:
        print("无法读取数据，程序退出")
        return
    
    print(f"✅ 成功读取 {len(data)} 行数据")
    
    stats = calculate_statistics(data)
    
    print("\n📈 销售数据统计结果:")
    print(f"   总销售额: ¥{stats['total']:,.2f}")
    print(f"   平均销售额: ¥{stats['average']:,.2f}")
    print(f"   最高销售额: ¥{stats['max']:,.2f}")
    print(f"   最低销售额: ¥{stats['min']:,.2f}")
    
    print("\n🎨 正在生成小尺寸图表...")
    line_file, bar_file = plot_sales_data_small(data)
    
    print(f"\n✅ 小尺寸图表已生成:")
    print(f"   折线图: {line_file}")
    print(f"   柱状图: {bar_file}")
    print(f"\n📁 文件大小更小，便于分享！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")