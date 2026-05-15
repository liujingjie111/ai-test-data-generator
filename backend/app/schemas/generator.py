"""Generator request and response schemas."""

from typing import Any, Optional

from pydantic import BaseModel


class GeneratorRequest(BaseModel):
    """Schema for data generation request."""

    generator_type: str
    count: int = 1
    params: Optional[dict] = None


class ExportRequest(BaseModel):
    """Schema for data export request (optional count only)."""

    count: int = 1
    params: Optional[dict] = None


class GeneratedItem(BaseModel):
    """Schema for a single generated data item."""

    data: Any


class GeneratorResponse(BaseModel):
    """Schema for data generation response."""

    count: int
    data: list[GeneratedItem]