"""
Simple tools service with a single MCP client.
"""

import logging
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from fastmcp import Client

load_dotenv()

logger = logging.getLogger(__name__)

# Global MCP client instance
mcp_client = None


def initialize_client():
    """
    Initialize the global MCP client using environment configuration.
    """
    global mcp_client

    # Environment variables for MCP server configuration
    mcp_url = os.environ.get("MCP_URL", "http://localhost:9000/mcp")

    logger.info(f"Initializing MCP client for: {mcp_url}")
    mcp_client = Client(mcp_url)


async def get_tools_list() -> List[Dict[str, Any]]:
    """
    Get list of all available tools from the MCP client.

    Returns:
        List of tool dictionaries
    """
    if mcp_client is None:
        logger.error("MCP client not initialized")
        return []

    try:
        async with mcp_client:
            tools = await mcp_client.list_tools()

            tools_list = []
            for tool in tools:
                tool_dict = {
                    "name": tool.name if hasattr(tool, "name") else str(tool),
                    "description": getattr(tool, "description", ""),
                    "schema": getattr(tool, "inputSchema", None),
                }
                tools_list.append(tool_dict)

            logger.info(f"Retrieved {len(tools_list)} tools")
            return tools_list

    except Exception as e:
        logger.error(f"Failed to get tools: {str(e)}")
        return []


async def call_tool(tool_name: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Call a specific tool with parameters.

    Args:
        tool_name: Name of the tool to call
        params: Parameters to pass to the tool

    Returns:
        Tool execution result
    """
    if mcp_client is None:
        logger.error("MCP client not initialized")
        return {"error": "MCP client not initialized"}

    if params is None:
        params = {}

    try:
        async with mcp_client:
            result = await mcp_client.call_tool(tool_name, params)
            logger.info(f"Called tool '{tool_name}' successfully")
            return result.structured_content

    except Exception as e:
        logger.error(f"Failed to call tool '{tool_name}': {str(e)}")
        return {"error": str(e)}
