#!/usr/bin/env python3
"""
Demo script showing practical usage of Serena CLI.
This script demonstrates the core functionality in real-world scenarios.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from serena_cli.serena_manager import SerenaManager
from serena_cli.project_detector import ProjectDetector
from serena_cli.config_manager import ConfigManager
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def demo_project_detection():
    """Demonstrate project detection capabilities."""
    console.print(Panel("🔍 项目检测演示", style="blue"))
    
    detector = ProjectDetector()
    
    # Detect current project
    current_project = detector.detect_current_project()
    if current_project:
        console.print(f"✅ 自动检测到项目: {current_project}")
        
        # Get detailed project info
        project_info = detector.get_project_info(current_project)
        if project_info:
            table = Table(title="项目详细信息")
            table.add_column("属性", style="cyan")
            table.add_column("值", style="green")
            
            table.add_row("项目名称", project_info["name"])
            table.add_row("项目类型", project_info["type"])
            table.add_row("编程语言", ", ".join(project_info["languages"]))
            table.add_row("文件数量", str(project_info["size"]["total_files"]))
            table.add_row("项目大小", f"{project_info['size']['total_size_mb']:.2f} MB")
            table.add_row("Serena 配置", "✅ 已配置" if project_info["has_serena"] else "❌ 未配置")
            table.add_row("Panda 配置", "✅ 已配置" if project_info["has_panda_config"] else "❌ 未配置")
            
            console.print(table)
    else:
        console.print("❌ 无法检测到项目")
    
    console.print()


def demo_serena_manager():
    """Demonstrate Serena manager capabilities."""
    console.print(Panel("🐼 Serena 管理器演示", style="yellow"))
    
    serena_manager = SerenaManager()
    
    # Show installation guide
    guide = serena_manager.get_installation_guide()
    
    console.print(f"📊 安装指南:")
    console.print(f"   Python 版本: {guide['python_version']}")
    console.print(f"   推荐版本: {guide['recommended_version']}")
    console.print(f"   兼容性: {'✅ 兼容' if guide['compatible'] else '⚠️ 可能不兼容'}")
    console.print(f"   当前平台: {guide['current_platform']}")
    
    console.print(f"\n📦 可用安装方法:")
    for method in guide['installation_methods']:
        console.print(f"   - {method['method']}: {method['description']}")
        console.print(f"     命令: {method['command']}")
    
    if 'warnings' in guide:
        console.print(f"\n⚠️  注意事项:")
        for warning in guide['warnings']:
            console.print(f"   - {warning}")
    
    console.print()


def demo_config_management():
    """Demonstrate configuration management capabilities."""
    console.print(Panel("⚙️  配置管理演示", style="green"))
    
    config_manager = ConfigManager()
    
    # Get global config
    global_config = config_manager.get_config("global")
    if global_config:
        console.print("✅ 全局配置:")
        for key, value in global_config.items():
            if isinstance(value, dict):
                console.print(f"   {key}:")
                for sub_key, sub_value in value.items():
                    console.print(f"     {sub_key}: {sub_value}")
            else:
                console.print(f"   {key}: {value}")
    else:
        console.print("⚠️  全局配置为空（首次运行）")
    
    # Check project config
    detector = ProjectDetector()
    current_project = detector.detect_current_project()
    if current_project:
        project_config = config_manager.get_config("project", current_project)
        if project_config:
            console.print(f"\n✅ 项目配置 ({current_project}):")
            for key, value in project_config.items():
                console.print(f"   {key}: {value}")
        else:
            console.print(f"\n⚠️  项目配置为空")
    
    console.print()


async def demo_workflow():
    """Demonstrate a complete workflow."""
    console.print(Panel("🔄 完整工作流演示", style="magenta"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        # Step 1: Project detection
        task1 = progress.add_task("检测项目...", total=None)
        detector = ProjectDetector()
        current_project = detector.detect_current_project()
        progress.update(task1, description="✅ 项目检测完成")
        
        # Step 2: Environment check
        task2 = progress.add_task("检查环境...", total=None)
        serena_manager = SerenaManager()
        guide = serena_manager.get_installation_guide()
        progress.update(task2, description="✅ 环境检查完成")
        
        # Step 3: Status check
        task3 = progress.add_task("检查状态...", total=None)
        status = await serena_manager.get_status(current_project)
        progress.update(task3, description="✅ 状态检查完成")
        
        # Step 4: Configuration check
        task4 = progress.add_task("检查配置...", total=None)
        config_manager = ConfigManager()
        project_config = config_manager.get_config("project", current_project)
        progress.update(task4, description="✅ 配置检查完成")
    
    # Show workflow results
    console.print(f"\n📋 工作流结果:")
    console.print(f"   项目路径: {current_project}")
    console.print(f"   Python 兼容性: {'✅ 兼容' if guide['compatible'] else '⚠️ 可能不兼容'}")
    console.print(f"   Serena 状态: {'✅ 已启用' if status['serena_enabled'] else '❌ 未启用'}")
    console.print(f"   项目配置: {'✅ 已配置' if project_config else '❌ 未配置'}")
    
    console.print()


def demo_cli_commands():
    """Demonstrate available CLI commands."""
    console.print(Panel("💻 CLI 命令演示", style="cyan"))
    
    commands = [
        ("serena-cli --version", "显示版本信息"),
        ("serena-cli --help", "显示帮助信息"),
        ("serena-cli check-env", "检查环境兼容性"),
        ("serena-cli info", "获取项目信息"),
        ("serena-cli status", "查询 Serena 状态"),
        ("serena-cli config", "编辑项目配置"),
        ("serena-cli config --type global", "编辑全局配置"),
        ("serena-cli mcp-tools", "显示 MCP 工具信息"),
    ]
    
    table = Table(title="可用 CLI 命令")
    table.add_column("命令", style="cyan")
    table.add_column("描述", style="green")
    
    for cmd, desc in commands:
        table.add_row(cmd, desc)
    
    console.print(table)
    console.print()


def main():
    """Main demo function."""
    console.print(Panel("🐼 Serena CLI 功能演示", style="bold blue"))
    console.print("=" * 60)
    
    try:
        # Run all demos
        demo_project_detection()
        demo_serena_manager()
        demo_config_management()
        asyncio.run(demo_workflow())
        demo_cli_commands()
        
        # Summary
        console.print(Panel("🎉 演示完成！", style="bold green"))
        console.print("💡 核心功能总结:")
        console.print("   ✅ 智能项目检测")
        console.print("   ✅ Serena 管理")
        console.print("   ✅ 配置管理")
        console.print("   ✅ 完整工作流")
        console.print("   ✅ 丰富的 CLI 命令")
        
        console.print("\n🚀 现在你可以开始使用 Serena CLI 了！")
        console.print("   运行 'serena-cli --help' 查看所有可用命令")
        
    except KeyboardInterrupt:
        console.print("\n⏹️  演示被用户中断")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n💥 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
