#!/usr/bin/env python3
"""
PyInstaller打包脚本 - 将fapiao.py打包为Windows可执行文件
"""

import subprocess
import sys
import os
import importlib.util

def check_dependencies():
    """检查requirements.txt中的依赖库是否已安装"""
    requirements_file = 'requirements.txt'
    
    if not os.path.exists(requirements_file):
        print(f"❌ 未找到依赖文件: {requirements_file}")
        return False
    
    missing_deps = []
    
    with open(requirements_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # 解析包名（去除版本号）
                package_name = line.split('==')[0].split('>')[0].split('<')[0].split('~')[0]
                
                if importlib.util.find_spec(package_name) is None:
                    missing_deps.append(package_name)
    
    if missing_deps:
        print("⚠️  检测到缺少以下依赖库:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\n🔄 正在自动安装缺失的依赖库...")
        
        try:
            install_cmd = [sys.executable, '-m', 'pip', 'install', '-r', requirements_file]
            result = subprocess.run(install_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 依赖库安装成功！")
                return True
            else:
                print("❌ 依赖库安装失败！")
                print("错误信息:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ 安装依赖库时发生错误: {e}")
            return False
    
    print("✅ 所有依赖库已安装")
    return True


def build_executable():
    """使用PyInstaller打包Python脚本"""
    
    # 首先检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，打包中止")
        return
    
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