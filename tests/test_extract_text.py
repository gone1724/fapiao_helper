#!/usr/bin/env python3
"""
测试 extract_text 功能的脚本
选择PDF文件并提取文本内容，保存为同名txt文件
"""

import os
import sys
from pathlib import Path

# 添加父目录到路径，以便导入fapiao.py中的extract_text
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pdfminer.high_level import extract_text
import tkinter as tk
from tkinter import filedialog

def test_extract_text():
    """测试extract_text功能的主函数"""
    
    # 创建隐藏的tkinter窗口用于文件选择
    root = tk.Tk()
    root.withdraw()
    
    # 选择PDF文件
    file_path = filedialog.askopenfilename(
        title="选择要测试的PDF文件",
        filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
    )
    
    if not file_path:
        print("未选择文件，测试取消")
        return
    
    print(f"正在处理文件: {file_path}")
    
    try:
        # 提取文本
        text = extract_text(file_path) or ""
        
        if not text.strip():
            print("警告：未能从PDF中提取到任何文本内容")
            text = "[未能提取到文本内容]"
        
        # 生成输出文件名
        input_path = Path(file_path)
        output_path = input_path.with_suffix('.txt')
        
        # 保存文本到文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✅ 文本提取完成！")
        print(f"输入文件: {file_path}")
        print(f"输出文件: {output_path}")
        print(f"文本长度: {len(text)} 字符")
        
        # 显示前500字符的预览
        preview = text[:500]
        if len(text) > 500:
            preview += "..."
        print(f"\n文本预览:")
        print("-" * 50)
        print(preview)
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ 处理文件时发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_extract_text()
    input("\n按回车键退出...")