"""HTTP client for YCLIENTS API with rate limiting."""

import asyncio
import time
from typing import Any, Optional
import httpx
from .config import settings


class RateLimiter:
    """Simple rate limiter: 5 requests/second, 200 requests/minute."""
    
    def __init__(self, requests_per_second: int = 5, requests_per_minute: int = 200):
        self.requests_per_second = requests_per_second
        self.requests_per_minute = requests_per_minute
        self.second_tokens = requests_per_second
        self.minute_tokens = requests_per_minute
        self.last_second_refill = time.monotonic()
        self.last_minute_refill = time.monotonic()
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire a token, waiting if necessary."""
        async with self._lock:
            now = time.monotonic()
            
            second_elapsed = now - self.last_second_refill
            if second_elapsed >= 1.0:
                self.second_tokens = self.requests_per_second
                self.last_second_refill = now
            
            minute_elapsed = now - self.last_minute_refill
            if minute_elapsed >= 60.0:
                self.minute_tokens = self.requests_per_minute
                self.last_minute_refill = now
            
            while self.second_tokens <= 0 or self.minute_tokens <= 0:
                if self.second_tokens <= 0:
                    wait_time = 1.0 - (time.monotonic() - self.last_second_refill)
                    if wait_time > 0:
                        await asyncio.sleep(wait_time)
                    self.second_tokens = self.requests_per_second
                    self.last_second_refill = time.monotonic()
                
                if self.minute_tokens <= 0:
                    wait_time = 60.0 - (time.monotonic() - self.last_minute_refill)
                    if wait_time > 0:
                        await asyncio.sleep(wait_time)
                    self.minute_tokens = self.requests_per_minute
                    self.last_minute_refill = time.monotonic()
            
            self.second_tokens -= 1
            self.minute_tokens -= 1


class YClientsClient:
    """Async HTTP client for YCLIENTS API."""
    
    def __init__(
        self,
        partner_token: Optional[str] = None,
        user_token: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.partner_token = partner_token or settings.yclients_partner_token
        self.user_token = user_token or settings.yclients_user_token
        self.base_url = (base_url or settings.yclients_base_url).rstrip("/")
        self.rate_limiter = RateLimiter()
        self._client: Optional[httpx.AsyncClient] = None
    
    def _get_headers(self, require_user: bool = False) -> dict[str, str]:
        """Build authorization headers."""
        headers = {
            "Accept": "application/vnd.yclients.v2+json",
            "Content-Type": "application/json",
        }
        
        auth_parts = []
        if self.partner_token:
            auth_parts.append(f"Bearer {self.partner_token}")
        if self.user_token and require_user:
            auth_parts.append(f"User {self.user_token}")
        
        if auth_parts:
            headers["Authorization"] = ", ".join(auth_parts)
        
        return headers
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0,
            )
        return self._client
    
    async def close(self):
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
    
    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json_data: Optional[dict] = None,
        require_user: bool = False,
    ) -> dict[str, Any]:
        """Make an API request with rate limiting."""
        await self.rate_limiter.acquire()
        
        client = await self._get_client()
        headers = self._get_headers(require_user=require_user)
        
        response = await client.request(
            method=method,
            url=endpoint,
            params=params,
            json=json_data,
            headers=headers,
        )
        
        response.raise_for_status()
        return response.json()
    
    async def get(self, endpoint: str, params: Optional[dict] = None, **kwargs) -> dict[str, Any]:
        """GET request."""
        return await self.request("GET", endpoint, params=params, **kwargs)
    
    async def post(self, endpoint: str, json_data: Optional[dict] = None, **kwargs) -> dict[str, Any]:
        """POST request."""
        return await self.request("POST", endpoint, json_data=json_data, **kwargs)
    
    async def put(self, endpoint: str, json_data: Optional[dict] = None, **kwargs) -> dict[str, Any]:
        """PUT request."""
        return await self.request("PUT", endpoint, json_data=json_data, **kwargs)
    
    async def delete(self, endpoint: str, **kwargs) -> dict[str, Any]:
        """DELETE request."""
        return await self.request("DELETE", endpoint, **kwargs)


yclients_client = YClientsClient()
