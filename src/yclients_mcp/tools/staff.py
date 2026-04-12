"""Staff management tools for YCLIENTS MCP Server."""

import json
from typing import Any
from ..client import yclients_client


def register_staff_tools(mcp):
    """Register staff-related tools."""
    
    @mcp.tool()
    async def yclients_get_staff(
        company_id: int,
        with_deleted: int = 0,
    ) -> str:
        """
        Get list of staff members for a company.
        
        Args:
            company_id: The company ID
            with_deleted: Include deleted staff (1/0)
        
        Returns:
            JSON string with list of staff members
        """
        params = {}
        if with_deleted:
            params["with_deleted"] = with_deleted
        
        result = await yclients_client.get(
            f"/company/{company_id}/staff", params=params if params else None
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_staff_member(company_id: int, staff_id: int) -> str:
        """
        Get detailed information about a specific staff member.
        
        Args:
            company_id: The company ID
            staff_id: The staff member ID
        
        Returns:
            JSON string with staff member details
        """
        result = await yclients_client.get(f"/company/{company_id}/staff/{staff_id}")
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_create_staff(
        company_id: int,
        name: str,
        specialization: str | None = None,
        position_id: int | None = None,
        weight: int = 0,
        hidden: int = 0,
    ) -> str:
        """
        Create a new staff member (quick creation).
        
        Args:
            company_id: The company ID
            name: Staff member name
            specialization: Specialization description
            position_id: Position ID
            weight: Sort order weight
            hidden: Hidden from booking (1/0)
        
        Returns:
            JSON string with created staff member details
        """
        data = {"name": name, "weight": weight, "hidden": hidden}
        if specialization:
            data["specialization"] = specialization
        if position_id:
            data["position_id"] = position_id
        
        result = await yclients_client.post(
            f"/company/{company_id}/staff", json_data=data, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_update_staff(
        company_id: int,
        staff_id: int,
        name: str | None = None,
        specialization: str | None = None,
        hidden: int | None = None,
    ) -> str:
        """
        Update staff member information.
        
        Args:
            company_id: The company ID
            staff_id: The staff member ID
            name: New name
            specialization: New specialization
            hidden: Hidden from booking (1/0)
        
        Returns:
            JSON string with updated staff member details
        """
        data = {}
        if name:
            data["name"] = name
        if specialization:
            data["specialization"] = specialization
        if hidden is not None:
            data["hidden"] = hidden
        
        result = await yclients_client.put(
            f"/company/{company_id}/staff/{staff_id}", json_data=data, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_delete_staff(company_id: int, staff_id: int) -> str:
        """
        Delete a staff member.
        
        Args:
            company_id: The company ID
            staff_id: The staff member ID to delete
        
        Returns:
            JSON string with deletion result
        """
        result = await yclients_client.delete(
            f"/company/{company_id}/staff/{staff_id}", require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_positions(company_id: int) -> str:
        """
        Get list of staff positions for a company.
        
        Args:
            company_id: The company ID
        
        Returns:
            JSON string with list of positions
        """
        result = await yclients_client.get(f"/company/{company_id}/positions")
        return json.dumps(result, ensure_ascii=False, indent=2)
