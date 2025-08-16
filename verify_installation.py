#!/usr/bin/env python3
"""
Final verification script for Panda Index Helper installation.
This script verifies that everything is working correctly.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from panda_index_helper.mcp_server import PandaIndexHelperMCPServer
from panda_index_helper.serena_manager import SerenaManager
from panda_index_helper.project_detector import ProjectDetector
from panda_index_helper.config_manager import ConfigManager


async def verify_installation():
    """Verify the complete installation."""
    print("🔍 Panda Index Helper 安装验证")
    print("=" * 50)
    
    results = {}
    
    try:
        # Test 1: Import all modules
        print("\n1️⃣ 模块导入测试:")
        try:
            from panda_index_helper import (
                PandaIndexHelperMCPServer,
                SerenaManager,
                ProjectDetector,
                ConfigManager
            )
            print("   ✅ 所有模块导入成功")
            results["imports"] = True
        except Exception as e:
            print(f"   ❌ 模块导入失败: {e}")
            results["imports"] = False
        
        # Test 2: Create instances
        print("\n2️⃣ 实例创建测试:")
        try:
            server = PandaIndexHelperMCPServer()
            serena_manager = SerenaManager()
            detector = ProjectDetector()
            config_manager = ConfigManager()
            print("   ✅ 所有实例创建成功")
            results["instances"] = True
        except Exception as e:
            print(f"   ❌ 实例创建失败: {e}")
            results["instances"] = False
        
        # Test 3: MCP server functionality
        print("\n3️⃣ MCP 服务器功能测试:")
        try:
            tools = server.get_tools_info()
            print(f"   ✅ 可用工具数量: {len(tools)}")
            for tool in tools:
                print(f"      - {tool['name']}: {tool['description']}")
            results["mcp_tools"] = True
        except Exception as e:
            print(f"   ❌ MCP 工具获取失败: {e}")
            results["mcp_tools"] = False
        
        # Test 4: Project detection
        print("\n4️⃣ 项目检测测试:")
        try:
            current_project = detector.detect_current_project()
            if current_project:
                print(f"   ✅ 当前项目: {current_project}")
                project_info = detector.get_project_info(current_project)
                if project_info:
                    print(f"      - 类型: {project_info['type']}")
                    print(f"      - 语言: {', '.join(project_info['languages'])}")
                results["project_detection"] = True
            else:
                print("   ⚠️  无法检测到项目")
                results["project_detection"] = False
        except Exception as e:
            print(f"   ❌ 项目检测失败: {e}")
            results["project_detection"] = False
        
        # Test 5: Serena manager
        print("\n5️⃣ Serena 管理器测试:")
        try:
            guide = serena_manager.get_installation_guide()
            print(f"   ✅ 安装指南生成成功")
            print(f"      - Python 版本: {guide['python_version']}")
            print(f"      - 兼容性: {'✅ 兼容' if guide['compatible'] else '⚠️ 可能不兼容'}")
            results["serena_manager"] = True
        except Exception as e:
            print(f"   ❌ Serena 管理器测试失败: {e}")
            results["serena_manager"] = False
        
        # Test 6: Tool execution
        print("\n6️⃣ 工具执行测试:")
        try:
            if current_project:
                result = await server.execute_tool("serena_status", {"project_path": current_project})
                if "error" not in result:
                    print("   ✅ 工具执行成功")
                    results["tool_execution"] = True
                else:
                    print(f"   ⚠️  工具执行返回错误: {result['error']}")
                    results["tool_execution"] = False
            else:
                print("   ⚠️  跳过工具执行测试（无项目）")
                results["tool_execution"] = False
        except Exception as e:
            print(f"   ❌ 工具执行失败: {e}")
            results["tool_execution"] = False
        
        # Test 7: Configuration management
        print("\n7️⃣ 配置管理测试:")
        try:
            config = config_manager.get_config("global")
            if config:
                print("   ✅ 全局配置读取成功")
            else:
                print("   ⚠️  全局配置为空（可能是首次运行）")
            results["config_management"] = True
        except Exception as e:
            print(f"   ❌ 配置管理测试失败: {e}")
            results["config_management"] = False
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 验证总结:")
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        for test_name, result in results.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"   {test_name}: {status}")
        
        print(f"\n总体结果: {passed_tests}/{total_tests} 测试通过")
        
        if passed_tests == total_tests:
            print("\n🎉 恭喜！Panda Index Helper 安装验证完全通过！")
            print("\n💡 下一步:")
            print("   1. 在 Cursor 中配置 MCP 服务器")
            print("   2. 使用 @mcp panda-index-helper 启用 Serena")
            print("   3. 享受智能编码体验！")
        elif passed_tests >= total_tests * 0.8:
            print("\n⚠️  大部分测试通过，但有一些小问题。")
            print("   建议检查错误信息并解决相关问题。")
        else:
            print("\n❌ 多个测试失败，安装可能有问题。")
            print("   请检查错误信息并重新安装。")
        
        return passed_tests == total_tests
        
    except Exception as e:
        print(f"\n💥 验证过程中发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main verification function."""
    try:
        success = await verify_installation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  验证被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 验证过程中发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
