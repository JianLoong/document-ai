from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

import os

confluence_tool = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="fastmcp",
            args=["run", "./mcp/server.py", "--no-banner"],
            env={
                "CONFLUENCE_API_KEY": os.getenv("CONFLUENCE_API_KEY"),
                "CONFLUENCE_BASE_URL": os.getenv("CONFLUENCE_BASE_URL"),
            },
        ),
    )
)
