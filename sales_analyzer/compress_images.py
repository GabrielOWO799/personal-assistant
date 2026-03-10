#!/usr/bin/env python3
"""
压缩图片以适应飞书发送
"""

from PIL import Image
import os

def compress_image(input_path, output_path, quality=85, max_size=(800, 600)):
    """
    压缩图片
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        quality: JPEG质量 (1-100)
        max_size: 最大尺寸 (width, height)
    """
    try:
        with Image.open(input_path) as img:
            # 转换为RGB模式（如果是RGBA）
            if img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # 调整大小
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存压缩后的图片
            img.save(output_path, 'PNG', optimize=True, quality=quality)
            print(f"✅ 压缩完成: {input_path} -> {output_path}")
            print(f"   原始大小: {os.path.getsize(input_path)} bytes")
            print(f"   压缩后: {os.path.getsize(output_path)} bytes")
            
    except Exception as e:
        print(f"❌ 压缩失败: {e}")

if __name__ == "__main__":
    # 压缩折线图
    compress_image(
        "sales_line_chart.png", 
        "sales_line_chart_compressed.png",
        quality=80,
        max_size=(800, 600)
    )
    
    # 压缩柱状图
    compress_image(
        "sales_bar_chart.png", 
        "sales_bar_chart_compressed.png",
        quality=80,
        max_size=(800, 600)
    )