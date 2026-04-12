"""YCLIENTS MCP Server - Main entry point."""

import asyncio
import logging
import sys
from contextlib import asynccontextmanager

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
import uvicorn

from .config import settings
from .client import yclients_client
from .tools import register_all_tools


logging.basicConfig(
    level=getattr(logging, settings.mcp_log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("yclients-mcp")


def create_mcp_server() -> Server:
    """Create and configure the MCP server."""
    server = Server("yclients-mcp-server")
    
    register_all_tools(server)
    
    @server.list_tools()
    async def list_tools():
        """Return list of available tools."""
        return server._tool_manager.list_tools()
    
    return server


async def run_stdio():
    """Run the server using stdio transport."""
    logger.info("Starting YCLIENTS MCP Server (stdio mode)")
    server = create_mcp_server()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def create_http_app() -> Starlette:
    """Create Starlette app for HTTP/SSE transport."""
    mcp_server = create_mcp_server()
    sse_transport = SseServerTransport("/mcp")
    
    async def handle_sse(request):
        """Handle SSE connection for MCP."""
        async with sse_transport.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp_server.run(
                streams[0],
                streams[1],
                mcp_server.create_initialization_options(),
            )
    
    async def handle_mcp_post(request):
        """Handle POST requests to /mcp endpoint."""
        return await sse_transport.handle_post_message(
            request.scope, request.receive, request._send
        )
    
    async def health_check(request):
        """Health check endpoint."""
        return JSONResponse({
            "status": "healthy",
            "service": "yclients-mcp-server",
            "version": "1.0.0",
        })
    
    async def tools_list(request):
        """List available tools (for debugging)."""
        tools = []
        for tool in mcp_server._tool_manager.list_tools():
            tools.append({
                "name": tool.name,
                "description": tool.description,
            })
        return JSONResponse({"tools": tools, "count": len(tools)})
    
    @asynccontextmanager
    async def lifespan(app):
        """Application lifespan handler."""
        logger.info(f"Starting YCLIENTS MCP Server on {settings.mcp_host}:{settings.mcp_port}")
        yield
        await yclients_client.close()
        logger.info("YCLIENTS MCP Server stopped")
    
    routes = [
        Route("/mcp", endpoint=handle_sse, methods=["GET"]),
        Route("/mcp", endpoint=handle_mcp_post, methods=["POST"]),
        Route("/health", endpoint=health_check, methods=["GET"]),
        Route("/tools", endpoint=tools_list, methods=["GET"]),
    ]
    
    return Starlette(routes=routes, lifespan=lifespan)


def run_http():
    """Run the server using HTTP/SSE transport."""
    app = create_http_app()
    uvicorn.run(
        app,
        host=settings.mcp_host,
        port=settings.mcp_port,
        log_level=settings.mcp_log_level.lower(),
    )


def main():
    """Main entry point."""
    if not settings.yclients_partner_token:
        logger.error("YCLIENTS_PARTNER_TOKEN environment variable is required")
        sys.exit(1)
    
    if settings.mcp_transport == "stdio":
        asyncio.run(run_stdio())
    else:
        run_http()


if __name__ == "__main__":
    main()
