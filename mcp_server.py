"""
MCP server for the walkthrough notebooks
This server is used to provide a MCP server for the walkthrough notebooks.

Inspired by https://github.com/daveebbelaar/ai-cookbook/tree/main/mcp/crash-course and https://www.youtube.com/watch?v=5xqFjh56AwM
"""

import os
import dotenv
from mcp.server.fastmcp import FastMCP
import tool_functions as tf

dotenv.load_dotenv()

host = os.getenv("MCP_SERVER_HOST")
port = os.getenv("MCP_SERVER_PORT")

# Create an MCP server
mcp = FastMCP(
    name="FunctionServer",
    version="1.0.0",
    description="A simple MCP server for the walkthrough notebooks",
    host=host,  # only used for SSE transport (localhost)
    port=port,  # only used for SSE transport (set this to any port)
    stateless_http=True,
)


# Add tools to the MCP server
@mcp.tool()
def calculate_btw(bedrag: float, btw_percentage: float = 21.0) -> dict:
    """
    Bereken BTW over een bedrag.

    Args:
        bedrag: Het bedrag exclusief BTW
        btw_percentage: BTW percentage (standaard 21%)

    Returns:
        Dict met BTW berekening resultaten
    """
    return tf.calculate_btw(bedrag, btw_percentage)


@mcp.tool()
def calculate_discount(bedrag: float, korting_percentage: float) -> dict:
    """
    Bereken korting over een bedrag.
    """
    return tf.calculate_discount(bedrag, korting_percentage)


@mcp.tool()
def get_inwoners_gemeente(gemeente_naam: str = None, jaar: str = "2025") -> dict:
    """
    Geef het aantal inwoners van een gemeente.
    """
    return tf.get_inwoners_gemeente(gemeente_naam, jaar)


# Run the server
if __name__ == "__main__":
    mcp.run(transport="sse")
