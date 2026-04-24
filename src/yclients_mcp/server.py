"""YCLIENTS MCP Server - Main entry point."""

import logging
import contextlib
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route, Mount

from .config import settings
from .client import yclients_client
from .tools import register_all_tools


logging.basicConfig(
    level=getattr(logging, settings.mcp_log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("yclients-mcp")

_allowed_hosts = [h.strip() for h in settings.mcp_allowed_hosts.split(",") if h.strip()]
_allowed_origins = [o.strip() for o in settings.mcp_allowed_origins.split(",") if o.strip()]

mcp = FastMCP(
    "yclients-mcp-server",
    stateless_http=True,
    json_response=True,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=_allowed_hosts,
        allowed_origins=_allowed_origins,
    ),
)

mcp.settings.host = settings.mcp_host
mcp.settings.port = settings.mcp_port

register_all_tools(mcp)


async def health(request: Request):
    """Health check endpoint."""
    return JSONResponse({"status": "ok", "service": "yclients-mcp-server"})


async def root(request: Request):
    """Root endpoint with service info."""
    return JSONResponse({
        "service": "yclients-mcp-server",
        "version": "1.0.0",
        "endpoints": {
            "mcp": "/mcp/",
            "health": "/health",
            "webhook": "/webhook",
        },
    })


async def yclients_webhook(request: Request):
    """Webhook endpoint for YCLIENTS events/fiscal integration."""
    try:
        payload = await request.json()
    except Exception:
        payload = None

    logger.info("YCLIENTS webhook received: %s", payload)

    # Если это запрос на фискализацию (содержит document_id + positions) -
    # возвращаем pending-ответ согласно спецификации YCLIENTS.
    if isinstance(payload, dict) and payload.get("id") and "positions" in payload:
        return JSONResponse({
            "id": payload.get("id"),
            "status": "pending",
            "code": 0,
            "message": "Document received",
        })

    return JSONResponse({"status": "ok"})


def create_app() -> Starlette:
    """Create Starlette app combining MCP + webhook + health routes."""
    mcp_app = mcp.streamable_http_app()

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette):
        async with mcp_app.router.lifespan_context(app):
            yield

    return Starlette(
        routes=[
            Route("/", root, methods=["GET"]),
            Route("/health", health, methods=["GET"]),
            Route("/webhook", yclients_webhook, methods=["POST", "GET"]),
            Route("/webhook/yclients", yclients_webhook, methods=["POST", "GET"]),
            Mount("/", app=mcp_app),
        ],
        lifespan=lifespan,
    )


def main():
    """Main entry point."""
    if not settings.yclients_partner_token:
        logger.warning("YCLIENTS_PARTNER_TOKEN not set - API calls will fail until configured")

    logger.info(f"Starting YCLIENTS MCP Server on {settings.mcp_host}:{settings.mcp_port}")
    logger.info(f"Allowed hosts: {_allowed_hosts}")

    if settings.mcp_transport == "stdio":
        mcp.run(transport="stdio")
    else:
        import uvicorn
        uvicorn.run(
            create_app(),
            host=settings.mcp_host,
            port=settings.mcp_port,
            log_level=settings.mcp_log_level.lower(),
            proxy_headers=True,
            forwarded_allow_ips="*",
        )


if __name__ == "__main__":
    main()
