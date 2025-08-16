#!/usr/bin/env python3
"""
PyPI publishing script for Serena CLI.
This script handles building, testing, and publishing to PyPI.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a command and handle errors."""
    print(f"🔧 {description}")
    print(f"命令: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} 成功")
            return result.stdout
        else:
            print(f"❌ {description} 失败")
            print(f"错误: {result.stderr}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 异常: {e}")
        return None

def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 检查发布前置条件...")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ 请在项目根目录运行此脚本")
        return False
    
    # Check if build tools are installed
    try:
        import build
        import twine
        print("✅ 构建工具已安装")
    except ImportError:
        print("❌ 请安装构建工具: pip install build twine")
        return False
    
    # Check if we have a clean git state
    if run_command("git status --porcelain", "检查 Git 状态", check=False):
        print("⚠️  Git 工作目录不干净，建议先提交所有更改")
        response = input("是否继续? (y/N): ")
        if response.lower() != 'y':
            return False
    
    return True

def run_tests():
    """Run the test suite."""
    print("\n🧪 运行测试套件...")
    
    # Run pytest
    if not run_command("python -m pytest", "运行 pytest"):
        print("❌ 测试失败，无法发布")
        return False
    
    # Run type checking
    if not run_command("python -m mypy src/", "运行类型检查"):
        print("⚠️  类型检查失败，但继续发布")
    
    return True

def build_package():
    """Build the package."""
    print("\n🔨 构建包...")
    
    # Clean previous builds
    run_command("rm -rf dist/ build/ *.egg-info/", "清理之前的构建", check=False)
    
    # Build the package
    if not run_command("python -m build", "构建包"):
        return False
    
    # Check the built package
    if not run_command("python -m twine check dist/*", "检查构建的包"):
        return False
    
    return True

def publish_to_pypi(test=False):
    """Publish to PyPI."""
    print(f"\n🚀 发布到 {'Test PyPI' if test else 'PyPI'}...")
    
    if test:
        cmd = "python -m twine upload --repository testpypi dist/*"
        description = "发布到 Test PyPI"
    else:
        cmd = "python -m twine upload dist/*"
        description = "发布到 PyPI"
    
    if not run_command(cmd, description):
        return False
    
    return True

def show_instructions(test=False):
    """Show post-publish instructions."""
    print("\n" + "=" * 60)
    if test:
        print("🎉 成功发布到 Test PyPI!")
        print("=" * 60)
        print("\n📦 安装测试版本:")
        print("   pip install --index-url https://test.pypi.org/simple/ serena-cli")
        print("\n🔗 查看包:")
        print("   https://test.pypi.org/project/serena-cli/")
    else:
        print("🎉 成功发布到 PyPI!")
        print("=" * 60)
        print("\n📦 安装最新版本:")
        print("   pip install serena-cli")
        print("\n🔗 查看包:")
        print("   https://pypi.org/project/serena-cli/")
    
    print("\n💡 提示:")
    print("   - 等待几分钟让包在 PyPI 上可用")
    print("   - 检查包是否正确安装")
    print("   - 验证所有功能正常工作")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Serena CLI PyPI 发布脚本")
    parser.add_argument("--test", action="store_true", help="发布到 Test PyPI")
    parser.add_argument("--skip-tests", action="store_true", help="跳过测试")
    parser.add_argument("--skip-build", action="store_true", help="跳过构建")
    args = parser.parse_args()
    
    print("🚀 Serena CLI PyPI 发布脚本")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Run tests (unless skipped)
    if not args.skip_tests:
        if not run_tests():
            sys.exit(1)
    
    # Build package (unless skipped)
    if not args.skip_build:
        if not build_package():
            sys.exit(1)
    
    # Publish to PyPI
    if not publish_to_pypi(args.test):
        sys.exit(1)
    
    # Show instructions
    show_instructions(args.test)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  发布被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 发布过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
