#!/usr/bin/env python3
"""
PyInstaller 打包脚本 - 将 fapiao_helper.py 打包为 Windows 可执行文件。

新增支持 (方法B):
1. 若存在目录 tk_extra/tkdnd2.9 则自动随包加入 (供 tkinterdnd2 使用)。
2. 自动生成运行时 hook (_tkdnd_runtime_hook.py) 在 PyInstaller 解包目录中设置环境变量 TCLLIBPATH 以便 Tcl 找到 tkdnd。 
     Windows 下不需要修改代码主体即可启用拖拽。

使用步骤:
    在项目根目录创建 tk_extra/tkdnd2.9 并放入官方 tkdnd2.9 发行包里的所有文件 (pkgIndex.tcl、tkdnd.tcl、*.dll 等)。
    然后运行本脚本。若目录不存在会继续打包但仅提示不启用拖拽资源打包。
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


def ensure_tkdnd_hook(tkdnd_folder: str) -> str | None:
    """若需要支持 tkdnd，生成运行时 hook 文件并返回其路径；否则返回 None。"""
    if not os.path.isdir(tkdnd_folder):
        return None
    hook_path = '_tkdnd_runtime_hook.py'
    code = (
        "import os, sys\n"
        "base = getattr(sys, '_MEIPASS', None)\n"
        "if base:\n"
        "    cand = os.path.join(base, 'tkdnd2.9')\n"
        "    if os.path.isdir(cand):\n"
        "        prev = os.environ.get('TCLLIBPATH', '')\n"
        "        os.environ['TCLLIBPATH'] = (cand + (' ' + prev if prev else ''))\n"
    )
    with open(hook_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return hook_path


def build_executable():
    """使用 PyInstaller 打包 Python 脚本，并可选包含 tkdnd2.9 目录。"""

    if not check_dependencies():
        print("\n❌ 依赖检查失败，打包中止")
        return

    # 可选 tkdnd 目录
    tkdnd_dir = os.path.join('tk_extra', 'tkdnd2.9')
    has_tkdnd = os.path.isdir(tkdnd_dir)
    if has_tkdnd:
        print(f"✔ 发现 tkdnd 目录: {tkdnd_dir}，将随包加入并启用拖拽功能。")
    else:
        print("ℹ 未发现 tk_extra/tkdnd2.9，打包后若缺少系统 tkdnd 将仅禁用拖拽。")

    # 生成 hook (仅在有 tkdnd 时)
    hook_file = ensure_tkdnd_hook(tkdnd_dir) if has_tkdnd else None

    # PyInstaller 基础命令
    cmd = [
        'pyinstaller',
        '--name=fapiao_helper',
        '--onefile',
        '--windowed',
        '--icon=NONE',
        '--clean',
    ]

    if has_tkdnd:
        # Windows 下 --add-data 使用 分号 ; 作为分隔符
        add_data_arg = f"{tkdnd_dir}{os.pathsep}tkdnd2.9"
        cmd += ['--add-data', add_data_arg]
    if hook_file:
        cmd += ['--runtime-hook', hook_file]

    cmd.append('fapiao_helper.py')

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
            if has_tkdnd:
                print("拖拽支持: 已尝试随包注入 tkdnd2.9 (运行时自动设置 TCLLIBPATH)")
            else:
                print("拖拽支持: 未包含 tkdnd2.9，需系统已有 tkdnd 或改用普通点击选择。")
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