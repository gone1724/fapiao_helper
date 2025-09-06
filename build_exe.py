#!/usr/bin/env python3
"""
PyInstaller打包脚本 - 将fapiao.py打包为Windows可执行文件
"""

import subprocess
import sys
import os

def build_executable():
    """使用PyInstaller打包Python脚本"""
    
    # PyInstaller命令参数
    cmd = [
        'pyinstaller',
        '--name=fapiao_tool',      # 可执行文件名称
        '--onefile',               # 打包成单个可执行文件
        '--windowed',              # 不显示控制台窗口（GUI应用）
        '--icon=NONE',             # 不使用图标
        '--clean',                 # 清理临时文件
        'fapiao.py'                # 主脚本文件
    ]
    
    print("开始打包fapiao.py为可执行文件...")
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("\n✅ 打包成功！")
            print("可执行文件位置: dist/fapiao_tool.exe")
            print("\n打包日志:")
            print(result.stdout)
        else:
            print("\n❌ 打包失败！")
            print("错误信息:")
            print(result.stderr)
            print("\n标准输出:")
            print(result.stdout)
            
    except Exception as e:
        print(f"\n❌ 执行打包命令时发生错误: {e}")

if __name__ == "__main__":
    build_executable()