#!/usr/bin/env python3
"""
简单图片压缩脚本
"""

from PIL import Image
import os

def compress_image(input_path, output_path, quality=85):
    """压缩图片"""
    try:
        with Image.open(input_path) as img:
            # 转换为RGB模式（如果需要）
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 保存压缩后的图片
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            print(f"✅ 压缩完成: {input_path} -> {output_path}")
            return True
    except Exception as e:
        print(f"❌ 压缩失败: {e}")
        return False

if __name__ == "__main__":
    # 压缩折线图
    compress_image("sales_line_chart.png", "sales_line_chart_small.jpg", quality=70)
    # 压缩柱状图  
    compress_image("sales_bar_chart.png", "sales_bar_chart_small.jpg", quality=70)
    
    # 显示文件大小
    files = ["sales_line_chart.png", "sales_line_chart_small.jpg", 
             "sales_bar_chart.png", "sales_bar_chart_small.jpg"]
    for f in files:
        if os.path.exists(f):
            size = os.path.getsize(f)
            print(f"{f}: {size} bytes ({size/1024:.1f} KB)")