"""
File Reader Assistant Agent
Demonstrates MCP tools integration with ADK using the filesystem MCP server.

Reference: https://adk.dev/tools-custom/mcp-tools/
"""

import os # Required for path operations
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Define the folder to allow file access (must be absolute path)
ALLOWED_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "./mcp_test_files"))

# Create the folder if it doesn't exist
os.makedirs(ALLOWED_PATH, exist_ok=True)

# Create the agent with MCP filesystem tools
root_agent = LlmAgent(
    model = 'gemini-2.5-flash',
    name = 'file_reader_assistant',
    description = 'Helps users read and explore files using MCP tools.',
    instruction = """
    You are a file reader assistant that helps users explore files.

    Your capabilities:
    - Discover the folder you have access to using list_allowed_directories
    - List files in directories using list_directory
    - Read file contents using read_file

    When helping users:
    1. If you don't already know the allowed folder path, call list_allowed_directories first.
    2. Use list_directory (with that path) to show available files
    3. Use read_file to display file contents when asked
    4. Describe what you find in a helpful way

    Always be clear about which folder you're working with.
    """,
    tools = [
        McpToolset(
            connection_params = StdioConnectionParams(
                server_params = StdioServerParameters(
                    command = 'npx',
                    args = [
                        '-y',
                        '@modelcontextprotocol/server-filesystem',
                        ALLOWED_PATH,
                    ],
                ),
            ),
            # Filter to only expose safe, read-only tools
            tool_filter = ['list_directory', 'read_file', 'list_allowed_directories'],
        )
    ],
)
