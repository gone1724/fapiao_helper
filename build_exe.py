#!/usr/bin/env python3
"""
PyInstaller 打包脚本 - 将 fapiao_helper.py 打包为 Windows 可执行文件。

简化版本：已移除拖拽功能支持，仅保留基本的打包功能。
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
            result = subprocess.run(install_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            
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
    """使用 PyInstaller 打包 Python 脚本"""

    if not check_dependencies():
        print("\n❌ 依赖检查失败，打包中止")
        return

    # PyInstaller 基础命令
    cmd = [
        'pyinstaller',
        '--name=fapiao_helper',
        '--onefile',
        '--windowed',
        '--icon=NONE',
        '--clean',
        'fapiao_helper.py'
    ]

    print("开始打包 fapiao_helper.py 为可执行文件...")
    print('执行命令:')
    print(' '.join(cmd))

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=os.getcwd()
        )

        if result.returncode == 0:
            print("\n✅ 打包成功！")
            print("可执行文件位置: dist/fapiao_helper.exe")
            print("\n打包日志(截取):")
            print(result.stdout[-4000:])  # 避免超长
        else:
            print("\n❌ 打包失败！")
            print("错误信息:")
            print(result.stderr)
            print("\n标准输出(截取):")
            print(result.stdout[-4000:])
    except Exception as e:
        print(f"\n❌ 执行打包命令时发生错误: {e} | 建议检查: 1) pyinstaller 是否已安装 2) 路径/权限 3) 防病毒拦截")

if __name__ == "__main__":
    build_executable()