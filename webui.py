# -*- coding: utf-8 -*-
"""
如意基金分析 - Web UI 快捷启动
双击此文件或运行: python webui.py
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """启动 WebUI"""
    project_dir = Path(__file__).parent

    # 检查 .env
    if not (project_dir / ".env").exists():
        print("⚠ 未找到 .env 文件，从 .env.example 复制...")
        import shutil
        shutil.copy(project_dir / ".env.example", project_dir / ".env")
        print("✓ 已创建 .env，请编辑填入 API Key 后重新启动")

    # 检查前端构建
    static_dir = project_dir / "static"
    if not (static_dir / "index.html").exists():
        print("📦 前端未构建，正在构建...")
        frontend_dir = project_dir / "apps" / "dsa-web"
        if (frontend_dir / "package.json").exists():
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=False)
            subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=False)
            print("✓ 前端构建完成")

    # 启动服务
    print("🚀 启动如意基金分析 Web 服务...")
    print("  访问: http://127.0.0.1:8000")
    print("  按 Ctrl+C 停止\n")

    os.chdir(project_dir)
    os.system(f"{sys.executable} main.py --serve-only")


if __name__ == "__main__":
    main()
