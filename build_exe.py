#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发票助手一键打包脚本
使用 PyInstaller 将 Python 程序打包成独立的 exe 文件
"""

import os
import sys
import subprocess
import shutil
import PyInstaller
from pathlib import Path

def clean_build_dirs():
    """清理之前的构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 清理 .spec 文件
    for spec_file in Path('.').glob('*.spec'):
        print(f"删除文件: {spec_file}")
        spec_file.unlink()

def build_exe():
    """构建 exe 文件"""
    print("开始构建 exe 文件...")
    
    # PyInstaller 命令参数
    icon_path = (Path(__file__).resolve().parent / "icon.ico")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # 打包成单个文件
        "--windowed",                   # 不显示控制台窗口
        "--name=发票助手",               # 指定输出文件名
        "--distpath=dist",              # 输出目录
        "--workpath=build",             # 工作目录
        "--clean",                      # 清理临时文件
        "--disable-windowed-traceback", # 禁用窗口化错误追踪
        "fapiao_helper.py"              # 主程序文件
    ]

    # 处理图标（使用绝对路径，避免因CWD不同找不到图标）
    if icon_path.exists():
        # 在主程序文件之前插入 --icon <path>
        cmd[-1:-1] = ["--icon", str(icon_path)]
        print(f"使用图标: {icon_path}")
    else:
        print("注意: 未找到 icon.ico 文件，将使用默认图标")
    
    try:
        print("执行命令:", " ".join(cmd))
        # 不捕获输出，避免Windows控制台编码导致的UnicodeDecodeError
        subprocess.run(cmd, check=True)
        print("✓ 构建成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 构建失败: {e}")
        return False

def show_result():
    """显示构建结果"""
    dist_dir = Path("dist")
    if dist_dir.exists():
        exe_files = list(dist_dir.glob("*.exe"))
        if exe_files:
            exe_file = exe_files[0]
            file_size = exe_file.stat().st_size / (1024 * 1024)  # MB
            print(f"\n🎉 打包完成!")
            print(f"📁 输出目录: {dist_dir.absolute()}")
            print(f"📄 exe 文件: {exe_file.name}")
            print(f"📊 文件大小: {file_size:.1f} MB")
            print(f"\n可执行文件路径: {exe_file.absolute()}")
        else:
            print("✗ 在 dist 目录中未找到 exe 文件")
    else:
        print("✗ dist 目录不存在")

def main():
    """主函数"""
    print("=" * 50)
    print("      发票助手 - 一键打包工具")
    print("=" * 50)
    
    # 检查主程序文件是否存在
    if not os.path.exists("fapiao_helper.py"):
        print("✗ 错误: 未找到主程序文件 fapiao_helper.py")
        return False
    
    # 清理之前的构建
    clean_build_dirs()
    
    # 构建 exe
    if build_exe():
        show_result()
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n构建成功")
        else:
            print("\n构建失败")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n发生错误: {e}")
        sys.exit(1)