"""Analytics tools for YCLIENTS MCP Server."""

import json
from typing import Any
from ..client import yclients_client


def register_analytics_tools(mcp):
    """Register analytics-related tools."""
    
    @mcp.tool()
    async def yclients_get_company_stats(
        company_id: int,
        date_from: str,
        date_to: str,
    ) -> str:
        """
        Get main company statistics for a period.
        
        Args:
            company_id: The company ID
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
        
        Returns:
            JSON string with company statistics
        """
        params = {"date_from": date_from, "date_to": date_to}
        result = await yclients_client.get(
            f"/company/{company_id}/analytics/overall", params=params, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_revenue_by_day(
        company_id: int,
        date_from: str,
        date_to: str,
    ) -> str:
        """
        Get daily revenue breakdown.
        
        Args:
            company_id: The company ID
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
        
        Returns:
            JSON string with daily revenue data
        """
        params = {"date_from": date_from, "date_to": date_to}
        result = await yclients_client.get(
            f"/company/{company_id}/analytics/income", params=params, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_records_by_day(
        company_id: int,
        date_from: str,
        date_to: str,
    ) -> str:
        """
        Get daily records (appointments) count.
        
        Args:
            company_id: The company ID
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
        
        Returns:
            JSON string with daily records count
        """
        params = {"date_from": date_from, "date_to": date_to}
        result = await yclients_client.get(
            f"/company/{company_id}/analytics/records", params=params, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_occupancy_by_day(
        company_id: int,
        date_from: str,
        date_to: str,
    ) -> str:
        """
        Get daily occupancy/utilization data.
        
        Args:
            company_id: The company ID
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
        
        Returns:
            JSON string with daily occupancy data
        """
        params = {"date_from": date_from, "date_to": date_to}
        result = await yclients_client.get(
            f"/company/{company_id}/analytics/workload", params=params, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_records_by_source(
        company_id: int,
        date_from: str,
        date_to: str,
    ) -> str:
        """
        Get records breakdown by source (online, phone, walk-in, etc.).
        
        Args:
            company_id: The company ID
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
        
        Returns:
            JSON string with records by source
        """
        params = {"date_from": date_from, "date_to": date_to}
        result = await yclients_client.get(
            f"/company/{company_id}/analytics/sources", params=params, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_records_by_status(
        company_id: int,
        date_from: str,
        date_to: str,
    ) -> str:
        """
        Get records breakdown by visit status.
        
        Args:
            company_id: The company ID
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
        
        Returns:
            JSON string with records by status
        """
        params = {"date_from": date_from, "date_to": date_to}
        result = await yclients_client.get(
            f"/company/{company_id}/analytics/statuses", params=params, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_z_report(
        company_id: int,
        date_from: str,
        date_to: str,
    ) -> str:
        """
        Get Z-report (end-of-day financial report) data.
        
        Args:
            company_id: The company ID
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
        
        Returns:
            JSON string with Z-report data
        """
        params = {"date_from": date_from, "date_to": date_to}
        result = await yclients_client.get(
            f"/company/{company_id}/z_report", params=params, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
