"""Client management tools for YCLIENTS MCP Server."""

import json
from typing import Any
from ..client import yclients_client


def register_client_tools(mcp):
    """Register client-related tools."""
    
    @mcp.tool()
    async def yclients_search_clients(
        company_id: int,
        page: int = 1,
        page_size: int = 50,
        fields: list[str] | None = None,
        filters: dict | None = None,
        order_by: str | None = None,
        order_by_direction: str = "asc",
    ) -> str:
        """
        Search clients in a company with filters.
        
        Args:
            company_id: The company ID
            page: Page number
            page_size: Results per page (max 200)
            fields: List of fields to return (e.g., ["name", "phone", "email"])
            filters: Filter conditions
            order_by: Field to sort by
            order_by_direction: Sort direction ("asc" or "desc")
        
        Returns:
            JSON string with list of clients
        """
        data = {
            "page": page,
            "page_size": min(page_size, 200),
        }
        if fields:
            data["fields"] = fields
        if filters:
            data["filters"] = filters
        if order_by:
            data["order_by"] = order_by
            data["order_by_direction"] = order_by_direction
        
        result = await yclients_client.post(
            f"/company/{company_id}/clients/search", json_data=data, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_client(company_id: int, client_id: int) -> str:
        """
        Get detailed information about a specific client.
        
        Args:
            company_id: The company ID
            client_id: The client ID
        
        Returns:
            JSON string with client details
        """
        result = await yclients_client.get(
            f"/company/{company_id}/clients/{client_id}", require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_create_client(
        company_id: int,
        name: str,
        phone: str,
        email: str | None = None,
        comment: str | None = None,
        birth_date: str | None = None,
        sex: int | None = None,
    ) -> str:
        """
        Create a new client.
        
        Args:
            company_id: The company ID
            name: Client full name
            phone: Phone number
            email: Email address
            comment: Comment about the client
            birth_date: Birth date in YYYY-MM-DD format
            sex: Gender (1 = male, 2 = female, 0 = not specified)
        
        Returns:
            JSON string with created client details
        """
        data = {"name": name, "phone": phone}
        if email:
            data["email"] = email
        if comment:
            data["comment"] = comment
        if birth_date:
            data["birth_date"] = birth_date
        if sex is not None:
            data["sex"] = sex
        
        result = await yclients_client.post(
            f"/company/{company_id}/clients", json_data=data, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_update_client(
        company_id: int,
        client_id: int,
        name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        comment: str | None = None,
    ) -> str:
        """
        Update client information.
        
        Args:
            company_id: The company ID
            client_id: The client ID
            name: New name
            phone: New phone
            email: New email
            comment: New comment
        
        Returns:
            JSON string with updated client details
        """
        data = {}
        if name:
            data["name"] = name
        if phone:
            data["phone"] = phone
        if email:
            data["email"] = email
        if comment:
            data["comment"] = comment
        
        result = await yclients_client.put(
            f"/company/{company_id}/clients/{client_id}", json_data=data, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_delete_client(company_id: int, client_id: int) -> str:
        """
        Delete a client.
        
        Args:
            company_id: The company ID
            client_id: The client ID to delete
        
        Returns:
            JSON string with deletion result
        """
        result = await yclients_client.delete(
            f"/company/{company_id}/clients/{client_id}", require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_client_visits(
        company_id: int,
        client_id: int,
        page: int = 1,
        count: int = 50,
    ) -> str:
        """
        Get visit history for a client.
        
        Args:
            company_id: The company ID
            client_id: The client ID
            page: Page number
            count: Results per page
        
        Returns:
            JSON string with client visit history
        """
        data = {"page": page, "page_size": count}
        result = await yclients_client.post(
            f"/company/{company_id}/clients/{client_id}/visits/search",
            json_data=data,
            require_user=True,
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
