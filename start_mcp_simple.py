#!/usr/bin/env python3
"""
Simplified MCP server startup script to avoid TaskGroup issues.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from panda_index_helper.mcp_server import PandaIndexHelperMCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def start_simple_mcp():
    """Start MCP server with simplified error handling."""
    try:
        logger.info("Initializing Panda Index Helper MCP Server...")
        
        # Create server instance
        server = PandaIndexHelperMCPServer()
        
        if server.is_mcp_available():
            logger.info("MCP server available, starting...")
            try:
                await server.run()
            except Exception as e:
                logger.error(f"MCP server failed to start: {e}")
                if "TaskGroup" in str(e):
                    logger.error("TaskGroup error detected - this is a known MCP library issue")
                    logger.info("Falling back to CLI mode")
                raise
        else:
            logger.warning("MCP server not available, running in CLI mode")
            print("MCP server not available, but CLI functionality is working")
            print("Available CLI commands:")
            print("  panda-index-helper enable")
            print("  panda-index-helper status")
            print("  panda-index-helper config")
            print("  panda-index-helper info")
            
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        print(f"\n❌ MCP 服务器启动失败: {e}")
        print("\n💡 解决方案:")
        print("1. 使用 CLI 命令直接操作:")
        print("   panda-index-helper enable")
        print("   panda-index-helper status")
        print("   panda-index-helper config")
        print("\n2. 检查 MCP 库版本:")
        print("   pip show mcp")
        print("\n3. 尝试重新安装 MCP 库:")
        print("   pip install --upgrade mcp")
        print("\n4. 运行兼容性检查:")
        print("   python check_compatibility.py")
        return False
    
    return True


async def main():
    """Main entry point."""
    print("🐼 Panda Index Helper MCP Server - 简化启动")
    print("=" * 50)
    
    try:
        success = await start_simple_mcp()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  服务器被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 启动过程中发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
