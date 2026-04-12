"""Company management tools for YCLIENTS MCP Server."""

import json
from typing import Any
from ..client import yclients_client


def register_company_tools(mcp):
    """Register company-related tools."""
    
    @mcp.tool()
    async def yclients_get_companies(
        group_id: int | None = None,
        my: int = 1,
        active: int | None = None,
        moderated: int | None = None,
        page: int = 1,
        count: int = 50,
    ) -> str:
        """
        Get list of companies available to the user.
        
        Args:
            group_id: Filter by company group ID
            my: 1 to get only user's companies, 0 for all
            active: Filter by active status (1/0)
            moderated: Filter by moderation status (1/0)
            page: Page number for pagination
            count: Number of results per page (max 300)
        
        Returns:
            JSON string with list of companies
        """
        params = {"my": my, "page": page, "count": count}
        if group_id is not None:
            params["group_id"] = group_id
        if active is not None:
            params["active"] = active
        if moderated is not None:
            params["moderated"] = moderated
        
        result = await yclients_client.get("/companies", params=params, require_user=True)
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_get_company(company_id: int) -> str:
        """
        Get detailed information about a specific company.
        
        Args:
            company_id: The company ID
        
        Returns:
            JSON string with company details
        """
        result = await yclients_client.get(f"/company/{company_id}", require_user=True)
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_create_company(
        title: str,
        country_id: int,
        city_id: int,
        business_type_id: int,
        address: str | None = None,
        phone: str | None = None,
        site: str | None = None,
    ) -> str:
        """
        Create a new company.
        
        Args:
            title: Company name
            country_id: Country ID
            city_id: City ID
            business_type_id: Business type ID
            address: Company address
            phone: Contact phone
            site: Website URL
        
        Returns:
            JSON string with created company details
        """
        data = {
            "title": title,
            "country_id": country_id,
            "city_id": city_id,
            "business_type_id": business_type_id,
        }
        if address:
            data["address"] = address
        if phone:
            data["phone"] = phone
        if site:
            data["site"] = site
        
        result = await yclients_client.post("/companies", json_data=data, require_user=True)
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @mcp.tool()
    async def yclients_update_company(
        company_id: int,
        title: str | None = None,
        address: str | None = None,
        phone: str | None = None,
        site: str | None = None,
    ) -> str:
        """
        Update company information.
        
        Args:
            company_id: The company ID to update
            title: New company name
            address: New address
            phone: New phone
            site: New website URL
        
        Returns:
            JSON string with updated company details
        """
        data = {}
        if title:
            data["title"] = title
        if address:
            data["address"] = address
        if phone:
            data["phone"] = phone
        if site:
            data["site"] = site
        
        result = await yclients_client.put(
            f"/company/{company_id}", json_data=data, require_user=True
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
