"""Online booking tools for YCLIENTS MCP Server."""

import json
from typing import Any
from ..client import yclients_client


def register_booking_tools(mcp):
    """Register online booking-related tools."""
    
    @mcp.tool()
    async def yclients_get_booking_settings(company_id: int) -> str:
        """
        Get booking form settings for a company.
        
        Args:
            company_id: The company ID
        
        Returns:
            JSON string with booking settings
        """
        result = await yclients_client.get(f"/book_form/{company_id}")
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_available_dates(
        company_id: int,
        staff_id: int | None = None,
        service_ids: list[int] | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> str:
        """
        Get list of dates available for booking.
        
        Args:
            company_id: The company ID
            staff_id: Filter by staff member ID
            service_ids: List of service IDs
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
        
        Returns:
            JSON string with available dates
        """
        params = {}
        if staff_id is not None:
            params["staff_id"] = staff_id
        if service_ids:
            params["service_ids[]"] = service_ids
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        
        result = await yclients_client.get(
            f"/book_dates/{company_id}", params=params if params else None
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_available_times(
        company_id: int,
        staff_id: int,
        date: str,
        service_ids: list[int] | None = None,
    ) -> str:
        """
        Get available time slots for booking on a specific date.
        
        Args:
            company_id: The company ID
            staff_id: Staff member ID
            date: Date to check (YYYY-MM-DD)
            service_ids: List of service IDs
        
        Returns:
            JSON string with available time slots
        """
        params = {"staff_id": staff_id, "date": date}
        if service_ids:
            params["service_ids[]"] = service_ids
        
        result = await yclients_client.get(f"/book_times/{company_id}", params=params)
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_available_staff(
        company_id: int,
        service_ids: list[int] | None = None,
        datetime: str | None = None,
    ) -> str:
        """
        Get list of staff available for booking.
        
        Args:
            company_id: The company ID
            service_ids: Filter by service IDs
            datetime: Filter by specific datetime
        
        Returns:
            JSON string with available staff
        """
        params = {}
        if service_ids:
            params["service_ids[]"] = service_ids
        if datetime:
            params["datetime"] = datetime
        
        result = await yclients_client.get(
            f"/book_staff/{company_id}", params=params if params else None
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_available_services(
        company_id: int,
        staff_id: int | None = None,
    ) -> str:
        """
        Get list of services available for booking.
        
        Args:
            company_id: The company ID
            staff_id: Filter by staff member ID
        
        Returns:
            JSON string with available services
        """
        params = {}
        if staff_id is not None:
            params["staff_id"] = staff_id
        
        result = await yclients_client.get(
            f"/book_services/{company_id}", params=params if params else None
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_create_booking(
        company_id: int,
        staff_id: int,
        services: list[dict],
        client: dict,
        datetime: str,
        comment: str | None = None,
    ) -> str:
        """
        Create a new online booking.
        
        Args:
            company_id: The company ID
            staff_id: Staff member ID
            services: List of services [{"id": service_id}]
            client: Client info {"phone": "...", "name": "...", "email": "..."}
            datetime: Booking datetime (ISO 8601 format)
            comment: Booking comment
        
        Returns:
            JSON string with created booking details
        """
        data = {
            "staff_id": staff_id,
            "services": services,
            "client": client,
            "datetime": datetime,
        }
        if comment:
            data["comment"] = comment
        
        result = await yclients_client.post(f"/book_record/{company_id}", json_data=data)
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_nearest_available(
        company_id: int,
        service_ids: list[int],
        staff_id: int | None = None,
    ) -> str:
        """
        Get nearest available time slots for booking.
        
        Args:
            company_id: The company ID
            service_ids: List of service IDs
            staff_id: Filter by staff member ID
        
        Returns:
            JSON string with nearest available slots
        """
        params = {"service_ids[]": service_ids}
        if staff_id is not None:
            params["staff_id"] = staff_id
        
        result = await yclients_client.get(f"/book_times/nearest/{company_id}", params=params)
        return json.dumps(result, ensure_ascii=False, indent=2)
