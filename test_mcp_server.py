#!/usr/bin/env python3
"""
Test script for Panda Index Helper MCP Server.
This script tests the core functionality without requiring MCP protocol.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from panda_index_helper.mcp_server import PandaIndexHelperMCPServer
from panda_index_helper.project_detector import ProjectDetector
from panda_index_helper.serena_manager import SerenaManager


async def test_mcp_server():
    """Test the MCP server functionality."""
    print("🧪 测试 Panda Index Helper MCP 服务器...")
    print("=" * 50)
    
    try:
        # Create server instance
        server = PandaIndexHelperMCPServer()
        
        # Test 1: Check available tools
        print("\n1️⃣ 测试可用工具:")
        tools = server.get_tools_info()
        for tool in tools:
            print(f"   ✅ {tool['name']}: {tool['description']}")
        
        # Test 2: Test project detection
        print("\n2️⃣ 测试项目检测:")
        detector = ProjectDetector()
        current_project = detector.detect_current_project()
        if current_project:
            print(f"   ✅ 当前项目: {current_project}")
            
            # Get project info
            project_info = detector.get_project_info(current_project)
            if project_info:
                print(f"   ✅ 项目类型: {project_info['type']}")
                print(f"   ✅ 编程语言: {', '.join(project_info['languages'])}")
                print(f"   ✅ 文件数量: {project_info['size']['total_files']}")
                print(f"   ✅ 项目大小: {project_info['size']['total_size_mb']} MB")
        else:
            print("   ❌ 无法检测到项目")
        
        # Test 3: Test Serena manager
        print("\n3️⃣ 测试 Serena 管理器:")
        serena_manager = SerenaManager()
        
        # Check Python compatibility
        print(f"   📊 Python 版本: {serena_manager.python_version}")
        print(f"   📊 兼容性: {'✅ 兼容' if serena_manager.is_python_compatible else '⚠️ 可能不兼容'}")
        print(f"   📊 推荐版本: {serena_manager._check_python_compatibility()}")
        
        # Get installation guide
        guide = serena_manager.get_installation_guide()
        print(f"   📊 当前平台: {guide['current_platform']}")
        print(f"   📊 安装方法:")
        for method in guide['installation_methods']:
            print(f"      - {method['method']}: {method['description']}")
        
        if 'warnings' in guide:
            print(f"   ⚠️  警告:")
            for warning in guide['warnings']:
                print(f"      - {warning}")
        
        # Test 4: Test tool execution (without actual installation)
        print("\n4️⃣ 测试工具执行:")
        if current_project:
            # Test status tool
            status_result = await server.execute_tool("serena_status", {"project_path": current_project})
            print(f"   📊 状态查询结果: {json.dumps(status_result, ensure_ascii=False, indent=2)}")
            
            # Test config tool
            config_result = await server.execute_tool("edit_config", {"config_type": "project"})
            print(f"   ⚙️  配置编辑结果: {json.dumps(config_result, ensure_ascii=False, indent=2)}")
        
        print("\n✅ 所有测试完成！")
        
        # Show usage instructions
        print("\n📖 使用说明:")
        print("   1. 安装: pip install panda-index-helper")
        print("   2. 配置 MCP 客户端")
        print("   3. 使用: @mcp panda-index-helper")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_serena_installation():
    """Test Serena installation (dry run)."""
    print("\n🔧 测试 Serena 安装 (模拟):")
    print("=" * 30)
    
    try:
        serena_manager = SerenaManager()
        
        # Test installation guide
        guide = serena_manager.get_installation_guide()
        print(f"📊 安装指南:")
        print(f"   Python 版本: {guide['python_version']}")
        print(f"   兼容性: {'✅ 兼容' if guide['compatible'] else '⚠️ 可能不兼容'}")
        print(f"   推荐版本: {guide['recommended_version']}")
        print(f"   当前平台: {guide['current_platform']}")
        
        print(f"\n📦 可用安装方法:")
        for method in guide['installation_methods']:
            print(f"   - {method['method']}: {method['description']}")
            print(f"     命令: {method['command']}")
        
        if 'warnings' in guide:
            print(f"\n⚠️  注意事项:")
            for warning in guide['warnings']:
                print(f"   - {warning}")
        
        return True
        
    except Exception as e:
        print(f"❌ 安装测试失败: {e}")
        return False


async def main():
    """Main test function."""
    print("🐼 Panda Index Helper MCP Server 测试套件")
    print("=" * 60)
    
    # Test 1: Basic functionality
    success1 = await test_mcp_server()
    
    # Test 2: Installation guide
    success2 = await test_serena_installation()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 测试总结:")
    print(f"   MCP 服务器测试: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"   安装指南测试: {'✅ 通过' if success2 else '❌ 失败'}")
    
    if success1 and success2:
        print("\n🎉 所有测试通过！MCP 服务器可以正常使用。")
        print("\n💡 下一步:")
        print("   1. 在 Cursor 中配置 MCP 服务器")
        print("   2. 使用 @mcp panda-index-helper 启用 Serena")
        print("   3. 享受智能编码体验！")
    else:
        print("\n⚠️  部分测试失败，请检查错误信息。")
    
    return success1 and success2


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 测试过程中发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
