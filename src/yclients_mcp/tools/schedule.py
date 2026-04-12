"""Schedule management tools for YCLIENTS MCP Server."""

import json
from typing import Any
from ..client import yclients_client


def register_schedule_tools(mcp):
    """Register schedule-related tools."""
    
    @mcp.tool()
    async def yclients_get_schedule(
        company_id: int,
        staff_id: int | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> str:
        """
        Get work schedule for staff members.
        
        Args:
            company_id: The company ID
            staff_id: Filter by staff member ID
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
        
        Returns:
            JSON string with schedule data
        """
        params = {}
        if staff_id is not None:
            params["staff_id"] = staff_id
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        
        result = await yclients_client.get(
            f"/company/{company_id}/schedule", params=params if params else None, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_timetable(
        company_id: int,
        staff_id: int,
        date: str,
    ) -> str:
        """
        Get detailed timetable for a staff member on a specific date.
        
        Args:
            company_id: The company ID
            staff_id: Staff member ID
            date: Date to check (YYYY-MM-DD)
        
        Returns:
            JSON string with timetable data
        """
        result = await yclients_client.get(
            f"/timetable/{company_id}/{staff_id}/{date}", require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_workload(
        company_id: int,
        date_from: str,
        date_to: str,
        staff_id: int | None = None,
    ) -> str:
        """
        Get workload statistics for staff members.
        
        Args:
            company_id: The company ID
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            staff_id: Filter by staff member ID
        
        Returns:
            JSON string with workload data
        """
        params = {"date_from": date_from, "date_to": date_to}
        if staff_id is not None:
            params["staff_id"] = staff_id
        
        result = await yclients_client.get(
            f"/company/{company_id}/workload", params=params, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
