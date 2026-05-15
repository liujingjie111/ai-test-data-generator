"""API Key request and response schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ApiKeyCreate(BaseModel):
    """Schema for creating a new API key."""

    name: str
    expires_at: Optional[datetime] = None


class ApiKeyResponse(BaseModel):
    """Schema for API key response data."""

    id: int
    key: str
    name: str
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
