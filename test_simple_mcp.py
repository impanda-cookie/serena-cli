#!/usr/bin/env python3
"""
Simple test for MCP server functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from panda_index_helper.mcp_server import PandaIndexHelperMCPServer


async def test_simple():
    """Simple test without MCP protocol."""
    print("🧪 简单 MCP 服务器测试")
    print("=" * 40)
    
    try:
        # Create server
        server = PandaIndexHelperMCPServer()
        
        # Check MCP availability
        print(f"📊 MCP 可用性: {'✅ 可用' if server.is_mcp_available() else '❌ 不可用'}")
        
        # Show tools
        tools = server.get_tools_info()
        print(f"\n🔧 可用工具数量: {len(tools)}")
        for tool in tools:
            print(f"   - {tool['name']}: {tool['description']}")
        
        # Test tool execution
        print(f"\n🧪 测试工具执行:")
        result = await server.execute_tool("serena_status", {})
        print(f"   状态查询: {'✅ 成功' if 'error' not in result else '❌ 失败'}")
        
        print("\n✅ 测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_simple())
    sys.exit(0 if success else 1)
