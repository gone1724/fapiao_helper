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
from pathlib import Path

def check_pyinstaller():
    """检查是否安装了 PyInstaller"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller 已安装，版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("✗ PyInstaller 未安装")
        return False

def install_pyinstaller():
    """安装 PyInstaller"""
    print("正在安装 PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                      check=True, capture_output=True, text=True)
        print("✓ PyInstaller 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller 安装失败: {e}")
        return False

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
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # 打包成单个文件
        "--windowed",                   # 不显示控制台窗口
        "--name=发票助手",               # 指定输出文件名
        "--icon=icon.ico",              # 图标文件（如果存在）
        "--add-data=README.md;.",       # 添加README文件
        "--distpath=dist",              # 输出目录
        "--workpath=build",             # 工作目录
        "--clean",                      # 清理临时文件
        "fapiao_helper.py"              # 主程序文件
    ]
    
    # 如果没有图标文件，移除图标参数
    if not os.path.exists("icon.ico"):
        cmd = [arg for arg in cmd if not arg.startswith("--icon")]
        print("注意: 未找到 icon.ico 文件，将使用默认图标")
    
    try:
        print("执行命令:", " ".join(cmd))
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ 构建成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 构建失败: {e}")
        if e.stdout:
            print("标准输出:", e.stdout)
        if e.stderr:
            print("错误输出:", e.stderr)
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
    
    # 检查并安装 PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
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
            print("\n按任意键退出...")
            input()
        else:
            print("\n构建失败，按任意键退出...")
            input()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n发生错误: {e}")
        sys.exit(1)