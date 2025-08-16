#!/usr/bin/env python3
"""
Compatibility check script for Panda Index Helper.
This script checks the user's environment and provides recommendations.
"""

import asyncio
import platform
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from panda_index_helper.serena_manager import SerenaManager
from panda_index_helper.project_detector import ProjectDetector


def check_python_compatibility():
    """Check Python version compatibility."""
    print("🐍 Python 兼容性检查")
    print("=" * 30)
    
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"当前版本: {version}")
    
    # Check compatibility
    major, minor = sys.version_info.major, sys.version_info.minor
    compatible = major == 3 and minor in [11, 12]
    
    if compatible:
        print("✅ 兼容性: 完全兼容 Serena")
    else:
        print("⚠️  兼容性: 可能不兼容 Serena")
        print("   推荐版本: Python 3.11 或 3.12")
    
    return compatible


def check_system_info():
    """Check system information."""
    print("\n💻 系统信息")
    print("=" * 20)
    
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"架构: {platform.machine()}")
    print(f"Python 路径: {sys.executable}")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"虚拟环境: {'✅ 是' if in_venv else '❌ 否'}")


def check_dependencies():
    """Check required dependencies."""
    print("\n📦 依赖检查")
    print("=" * 20)
    
    # Check MCP
    try:
        import mcp
        print("✅ MCP 库: 已安装")
    except ImportError:
        print("❌ MCP 库: 未安装")
        print("   安装命令: pip install mcp")
    
    # Check PyYAML
    try:
        import yaml
        print("✅ PyYAML: 已安装")
    except ImportError:
        print("❌ PyYAML: 未安装")
        print("   安装命令: pip install pyyaml")
    
    # Check Click
    try:
        import click
        print("✅ Click: 已安装")
    except ImportError:
        print("❌ Click: 未安装")
        print("   安装命令: pip install click")
    
    # Check Rich
    try:
        import rich
        print("✅ Rich: 已安装")
    except ImportError:
        print("❌ Rich: 未安装")
        print("   安装命令: pip install rich")


def check_installation_tools():
    """Check available installation tools."""
    print("\n🔧 安装工具检查")
    print("=" * 25)
    
    serena_manager = SerenaManager()
    guide = serena_manager.get_installation_guide()
    
    print(f"推荐 Python 版本: {guide['recommended_version']}")
    print(f"当前 Python 版本: {guide['python_version']}")
    print(f"兼容性: {'✅ 兼容' if guide['compatible'] else '⚠️ 可能不兼容'}")
    
    print(f"\n可用安装方法:")
    for method in guide['installation_methods']:
        print(f"  - {method['method']}: {method['description']}")
        print(f"    命令: {method['command']}")
    
    if 'warnings' in guide:
        print(f"\n⚠️  注意事项:")
        for warning in guide['warnings']:
            print(f"  - {warning}")


def check_project_environment():
    """Check current project environment."""
    print("\n📁 项目环境检查")
    print("=" * 25)
    
    detector = ProjectDetector()
    current_project = detector.detect_current_project()
    
    if current_project:
        print(f"✅ 当前项目: {current_project}")
        
        project_info = detector.get_project_info(current_project)
        if project_info:
            print(f"   项目类型: {project_info['type']}")
            print(f"   编程语言: {', '.join(project_info['languages'])}")
            print(f"   文件数量: {project_info['size']['total_files']}")
            print(f"   项目大小: {project_info['size']['total_size_mb']} MB")
            print(f"   Serena 配置: {'✅ 已配置' if project_info['has_serena'] else '❌ 未配置'}")
            print(f"   Panda 配置: {'✅ 已配置' if project_info['has_panda_config'] else '❌ 未配置'}")
    else:
        print("❌ 无法检测到项目")
        print("   请确保在项目目录中运行此脚本")


def provide_recommendations():
    """Provide recommendations based on the environment."""
    print("\n💡 使用建议")
    print("=" * 20)
    
    # Check Python version
    major, minor = sys.version_info.major, sys.version_info.minor
    compatible = major == 3 and minor in [11, 12]
    
    if not compatible:
        print("⚠️  Python 版本建议:")
        print("   当前版本可能不兼容 Serena，建议:")
        print("   1. 使用 Python 3.11 或 3.12")
        print("   2. 创建新的虚拟环境")
        print("   3. 或者等待 Serena 更新支持 Python 3.13")
        print()
    
    print("🚀 安装建议:")
    print("   1. 确保在项目目录中")
    print("   2. 安装 Panda Index Helper: pip install panda-index-helper")
    print("   3. 配置 MCP 客户端")
    print("   4. 使用: @mcp panda-index-helper")
    
    print("\n🔧 故障排除:")
    print("   如果遇到问题:")
    print("   1. 检查 Python 版本兼容性")
    print("   2. 确保网络连接正常")
    print("   3. 尝试使用 --force 参数")
    print("   4. 查看日志文件获取详细错误信息")


async def main():
    """Main compatibility check function."""
    print("🐼 Panda Index Helper 兼容性检查")
    print("=" * 50)
    
    # Run all checks
    python_compatible = check_python_compatibility()
    check_system_info()
    check_dependencies()
    check_installation_tools()
    check_project_environment()
    provide_recommendations()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 检查总结:")
    print(f"   Python 兼容性: {'✅ 通过' if python_compatible else '⚠️ 需要注意'}")
    print("   系统环境: ✅ 已检查")
    print("   依赖库: ✅ 已检查")
    print("   安装工具: ✅ 已检查")
    print("   项目环境: ✅ 已检查")
    
    if python_compatible:
        print("\n🎉 环境检查通过！可以正常使用 Panda Index Helper。")
    else:
        print("\n⚠️  环境检查发现兼容性问题，请参考上述建议。")
    
    return python_compatible


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  检查被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
