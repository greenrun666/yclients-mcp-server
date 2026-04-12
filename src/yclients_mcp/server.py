"""YCLIENTS MCP Server - Main entry point."""

import logging
from mcp.server.fastmcp import FastMCP

from .config import settings
from .client import yclients_client
from .tools import register_all_tools


logging.basicConfig(
    level=getattr(logging, settings.mcp_log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("yclients-mcp")

mcp = FastMCP(
    "yclients-mcp-server",
    stateless_http=True,
    json_response=True,
)

mcp.settings.host = settings.mcp_host
mcp.settings.port = settings.mcp_port

register_all_tools(mcp)


def main():
    """Main entry point."""
    if not settings.yclients_partner_token:
        logger.warning("YCLIENTS_PARTNER_TOKEN not set - API calls will fail until configured")
    
    logger.info(f"Starting YCLIENTS MCP Server on {settings.mcp_host}:{settings.mcp_port}")
    
    if settings.mcp_transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
