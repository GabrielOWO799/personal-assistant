#!/usr/bin/env python3
"""
销售数据分析器
功能：
1. 检查并创建示例CSV文件（如果不存在）
2. 读取CSV文件并计算统计信息
3. 使用matplotlib绘制折线图和柱状图
4. 自动安装依赖包（如果需要）
"""

import os
import csv
import sys
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import random


def check_and_install_matplotlib() -> bool:
    """
    检查matplotlib是否已安装，如果没有则自动安装
    Returns:
        bool: 安装成功返回True，否则返回False
    """
    try:
        import matplotlib.pyplot as plt
        return True
    except ImportError:
        print("检测到matplotlib未安装，正在自动安装...")
        try:
            # 尝试使用pip安装
            subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
            print("matplotlib安装成功！")
            return True
        except subprocess.CalledProcessError:
            print("❌ matplotlib安装失败，请手动安装：pip install matplotlib")
            return False


def create_sample_csv(filename: str = "data.csv", rows: int = 10) -> None:
    """
    创建示例CSV文件
    
    Args:
        filename: CSV文件名
        rows: 要生成的行数
    """
    print(f"正在创建示例CSV文件: {filename}")
    
    # 生成最近10天的日期
    end_date = datetime.now()
    dates = [(end_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(rows)]
    dates.reverse()  # 从最早到最晚
    
    # 生成随机销售额（1000-10000之间）
    sales = [random.randint(1000, 10000) for _ in range(rows)]
    
    # 写入CSV文件
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['日期', '销售额'])  # 表头
        for date, sale in zip(dates, sales):
            writer.writerow([date, sale])
    
    print(f"✅ 示例CSV文件已创建，包含{rows}行数据")


def load_csv_data(filename: str = "data.csv") -> Optional[List[Dict[str, str]]]:
    """
    读取CSV文件数据
    
    Args:
        filename: CSV文件名
        
    Returns:
        List[Dict]: 包含数据的字典列表，如果文件不存在返回None
    """
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
    """
    计算销售额的统计信息
    
    Args:
        data: CSV数据列表
        
    Returns:
        Dict: 包含总和、平均值、最大值、最小值的字典
    """
    try:
        sales = [float(row['销售额']) for row in data]
        
        total = sum(sales)
        average = total / len(sales) if sales else 0
        maximum = max(sales) if sales else 0
        minimum = min(sales) if sales else 0
        
        return {
            'total': total,
            'average': average,
            'max': maximum,
            'min': minimum
        }
    except (ValueError, KeyError) as e:
        print(f"❌ 计算统计信息时出错: {e}")
        return {'total': 0, 'average': 0, 'max': 0, 'min': 0}


def plot_sales_data(data: List[Dict[str, str]], output_prefix: str = "sales") -> Tuple[str, str]:
    """
    绘制销售数据图表
    
    Args:
        data: CSV数据列表
        output_prefix: 输出文件名前缀
        
    Returns:
        Tuple[str, str]: 折线图和柱状图的文件名
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from datetime import datetime
        
        # 准备数据
        dates = [datetime.strptime(row['日期'], '%Y-%m-%d') for row in data]
        sales = [float(row['销售额']) for row in data]
        
        # 创建图表
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文显示
        plt.rcParams['axes.unicode_minus'] = False   # 支持负号显示
        
        # 折线图
        plt.figure(figsize=(12, 6))
        plt.plot(dates, sales, marker='o', linewidth=2, markersize=6)
        plt.title('销售额趋势图', fontsize=16, fontweight='bold')
        plt.xlabel('日期', fontsize=12)
        plt.ylabel('销售额', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # 设置日期格式
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
        
        plt.tight_layout()
        line_chart_file = f"{output_prefix}_line_chart.png"
        plt.savefig(line_chart_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 柱状图
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(dates)), sales, alpha=0.7, color='skyblue')
        plt.title('每日销售额柱状图', fontsize=16, fontweight='bold')
        plt.xlabel('日期', fontsize=12)
        plt.ylabel('销售额', fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        
        # 设置x轴标签
        plt.xticks(range(len(dates)), [d.strftime('%m-%d') for d in dates], rotation=45)
        
        # 在柱子上显示数值
        for bar, sale in zip(bars, sales):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(sales)*0.01, 
                    f'{int(sale)}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        bar_chart_file = f"{output_prefix}_bar_chart.png"
        plt.savefig(bar_chart_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        return line_chart_file, bar_chart_file
        
    except Exception as e:
        print(f"❌ 绘制图表时出错: {e}")
        return "error_line.png", "error_bar.png"


def import_local_csv(filename: str) -> Optional[List[Dict[str, str]]]:
    """
    导入本地CSV文件的接口函数
    
    Args:
        filename: 要导入的CSV文件路径
        
    Returns:
        List[Dict]: CSV数据，如果失败返回None
    """
    return load_csv_data(filename)


def main():
    """主函数"""
    print("📊 销售数据分析器启动中...")
    
    # 检查并安装matplotlib
    if not check_and_install_matplotlib():
        print("无法继续执行，请先安装matplotlib")
        return
    
    csv_filename = "data.csv"
    
    # 检查CSV文件是否存在，如果不存在则创建示例数据
    if not os.path.exists(csv_filename):
        create_sample_csv(csv_filename, 10)
    else:
        print(f"✅ 找到现有CSV文件: {csv_filename}")
    
    # 读取CSV数据
    data = load_csv_data(csv_filename)
    if data is None:
        print("无法读取数据，程序退出")
        return
    
    print(f"✅ 成功读取 {len(data)} 行数据")
    
    # 计算统计信息
    stats = calculate_statistics(data)
    
    # 打印统计结果
    print("\n📈 销售数据统计结果:")
    print(f"   总销售额: ¥{stats['total']:,.2f}")
    print(f"   平均销售额: ¥{stats['average']:,.2f}")
    print(f"   最高销售额: ¥{stats['max']:,.2f}")
    print(f"   最低销售额: ¥{stats['min']:,.2f}")
    
    # 绘制图表
    print("\n🎨 正在生成图表...")
    line_file, bar_file = plot_sales_data(data)
    
    # 打印生成的文件信息
    print(f"\n✅ 图表已生成:")
    print(f"   折线图: {line_file}")
    print(f"   柱状图: {bar_file}")
    print(f"\n📁 所有文件保存在当前目录: {os.getcwd()}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")