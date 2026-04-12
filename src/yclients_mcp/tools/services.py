"""Service management tools for YCLIENTS MCP Server."""

import json
from typing import Any
from ..client import yclients_client


def register_service_tools(mcp):
    """Register service-related tools."""
    
    @mcp.tool()
    async def yclients_get_services(
        company_id: int,
        staff_id: int | None = None,
        category_id: int | None = None,
    ) -> str:
        """
        Get list of services for a company.
        
        Args:
            company_id: The company ID
            staff_id: Filter by staff member ID
            category_id: Filter by service category ID
        
        Returns:
            JSON string with list of services
        """
        params = {}
        if staff_id is not None:
            params["staff_id"] = staff_id
        if category_id is not None:
            params["category_id"] = category_id
        
        result = await yclients_client.get(
            f"/company/{company_id}/services", params=params if params else None
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_service(company_id: int, service_id: int) -> str:
        """
        Get detailed information about a specific service.
        
        Args:
            company_id: The company ID
            service_id: The service ID
        
        Returns:
            JSON string with service details
        """
        result = await yclients_client.get(f"/company/{company_id}/services/{service_id}")
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_create_service(
        company_id: int,
        title: str,
        category_id: int,
        price_min: float,
        price_max: float | None = None,
        duration: int = 3600,
        comment: str | None = None,
    ) -> str:
        """
        Create a new service.
        
        Args:
            company_id: The company ID
            title: Service name
            category_id: Service category ID
            price_min: Minimum price
            price_max: Maximum price (optional)
            duration: Service duration in seconds (default 3600 = 1 hour)
            comment: Service description
        
        Returns:
            JSON string with created service details
        """
        data = {
            "title": title,
            "category_id": category_id,
            "price_min": price_min,
            "seance_length": duration,
        }
        if price_max is not None:
            data["price_max"] = price_max
        if comment:
            data["comment"] = comment
        
        result = await yclients_client.post(
            f"/company/{company_id}/services", json_data=data, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_service_categories(company_id: int) -> str:
        """
        Get list of service categories for a company.
        
        Args:
            company_id: The company ID
        
        Returns:
            JSON string with list of service categories
        """
        result = await yclients_client.get(f"/company/{company_id}/service_categories")
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_create_service_category(
        company_id: int,
        title: str,
        weight: int = 0,
    ) -> str:
        """
        Create a new service category.
        
        Args:
            company_id: The company ID
            title: Category name
            weight: Sort order weight
        
        Returns:
            JSON string with created category details
        """
        data = {"title": title, "weight": weight}
        result = await yclients_client.post(
            f"/company/{company_id}/service_categories", json_data=data, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
