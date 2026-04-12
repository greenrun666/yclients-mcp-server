"""Record (appointment) management tools for YCLIENTS MCP Server."""

import json
from typing import Any
from ..client import yclients_client


def register_record_tools(mcp):
    """Register record/appointment-related tools."""
    
    @mcp.tool()
    async def yclients_get_records(
        company_id: int,
        staff_id: int | None = None,
        client_id: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        page: int = 1,
        count: int = 100,
    ) -> str:
        """
        Get list of records (appointments) for a company.
        
        Args:
            company_id: The company ID
            staff_id: Filter by staff member ID
            client_id: Filter by client ID
            start_date: Start date filter (YYYY-MM-DD)
            end_date: End date filter (YYYY-MM-DD)
            page: Page number
            count: Results per page
        
        Returns:
            JSON string with list of records
        """
        params = {"page": page, "count": count}
        if staff_id is not None:
            params["staff_id"] = staff_id
        if client_id is not None:
            params["client_id"] = client_id
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        result = await yclients_client.get(
            f"/company/{company_id}/records", params=params, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_record(company_id: int, record_id: int) -> str:
        """
        Get detailed information about a specific record.
        
        Args:
            company_id: The company ID
            record_id: The record ID
        
        Returns:
            JSON string with record details
        """
        result = await yclients_client.get(
            f"/company/{company_id}/records/{record_id}", require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_create_record(
        company_id: int,
        staff_id: int,
        services: list[dict],
        client: dict,
        datetime: str,
        seance_length: int | None = None,
        save_if_busy: bool = False,
        send_sms: bool = False,
        comment: str | None = None,
    ) -> str:
        """
        Create a new record (appointment).
        
        Args:
            company_id: The company ID
            staff_id: Staff member ID
            services: List of services [{"id": service_id, "cost": price}]
            client: Client info {"phone": "...", "name": "...", "email": "..."}
            datetime: Appointment datetime (ISO 8601 format)
            seance_length: Total duration in seconds (calculated from services if not provided)
            save_if_busy: Save even if time slot is busy
            send_sms: Send SMS notification to client
            comment: Appointment comment
        
        Returns:
            JSON string with created record details
        """
        data = {
            "staff_id": staff_id,
            "services": services,
            "client": client,
            "datetime": datetime,
            "save_if_busy": save_if_busy,
            "send_sms": send_sms,
        }
        if seance_length:
            data["seance_length"] = seance_length
        if comment:
            data["comment"] = comment
        
        result = await yclients_client.post(
            f"/company/{company_id}/records", json_data=data, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_update_record(
        company_id: int,
        record_id: int,
        staff_id: int | None = None,
        datetime: str | None = None,
        comment: str | None = None,
        attendance: int | None = None,
    ) -> str:
        """
        Update an existing record.
        
        Args:
            company_id: The company ID
            record_id: The record ID
            staff_id: New staff member ID
            datetime: New datetime
            comment: New comment
            attendance: Attendance status (0=not set, 1=confirmed, 2=client came, -1=client didn't come)
        
        Returns:
            JSON string with updated record details
        """
        data = {}
        if staff_id is not None:
            data["staff_id"] = staff_id
        if datetime:
            data["datetime"] = datetime
        if comment:
            data["comment"] = comment
        if attendance is not None:
            data["attendance"] = attendance
        
        result = await yclients_client.put(
            f"/company/{company_id}/records/{record_id}", json_data=data, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_delete_record(company_id: int, record_id: int) -> str:
        """
        Delete a record (appointment).
        
        Args:
            company_id: The company ID
            record_id: The record ID to delete
        
        Returns:
            JSON string with deletion result
        """
        result = await yclients_client.delete(
            f"/company/{company_id}/records/{record_id}", require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
