"""Configuration settings for YCLIENTS MCP Server."""

import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Server configuration from environment variables."""
    
    yclients_partner_token: str = Field(
        default="",
        description="YCLIENTS Partner API token (required)"
    )
    yclients_user_token: str = Field(
        default="",
        description="YCLIENTS User API token (optional, for user-specific operations)"
    )
    yclients_base_url: str = Field(
        default="https://api.yclients.com/api/v1",
        description="YCLIENTS API base URL"
    )
    
    mcp_transport: str = Field(
        default="http",
        description="MCP transport type: 'stdio' or 'http'"
    )
    mcp_host: str = Field(
        default="0.0.0.0",
        description="Host to bind HTTP server"
    )
    mcp_port: int = Field(
        default=8000,
        description="Port for HTTP server"
    )
    mcp_log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    mcp_allowed_hosts: str = Field(
        default="localhost,localhost:*,127.0.0.1,127.0.0.1:*,ycmcp.mybotai.net,ycmcp.mybotai.net:*",
        description="Comma-separated list of allowed Host headers"
    )
    mcp_allowed_origins: str = Field(
        default="http://localhost,http://localhost:*,http://127.0.0.1,http://127.0.0.1:*,https://ycmcp.mybotai.net,http://ycmcp.mybotai.net",
        description="Comma-separated list of allowed Origin headers"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
