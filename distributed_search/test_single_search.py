#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simple_manager import DistributedSearchManager

if __name__ == "__main__":
    keyword = "深圳 大模型 LLM 微调 训练 实习"
    output_file = "large_model_test"
    print(f"🔍 执行搜索: {keyword}")
    
    manager = DistributedSearchManager()
    results = manager.call_searxng(keyword)
    
    if results:
        # 保存结果
        test_buffer_dir = os.path.join(manager.buffer_dir, output_file)
        with open(test_buffer_dir, 'w', encoding='utf-8') as f:
            f.write(str(results))
        print(f"✅ 搜索结果已保存到: {test_buffer_dir}")
        print(f"📊 找到 {len(results)} 个岗位")
    else:
        print("❌ 未找到相关岗位")