"""YCLIENTS MCP Tools - API operations exposed as MCP tools."""

from .companies import register_company_tools
from .services import register_service_tools
from .staff import register_staff_tools
from .clients import register_client_tools
from .records import register_record_tools
from .booking import register_booking_tools
from .schedule import register_schedule_tools
from .analytics import register_analytics_tools


def register_all_tools(mcp_server):
    """Register all YCLIENTS tools with the MCP server."""
    register_company_tools(mcp_server)
    register_service_tools(mcp_server)
    register_staff_tools(mcp_server)
    register_client_tools(mcp_server)
    register_record_tools(mcp_server)
    register_booking_tools(mcp_server)
    register_schedule_tools(mcp_server)
    register_analytics_tools(mcp_server)
