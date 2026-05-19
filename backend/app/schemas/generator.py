"""Generator request and response schemas."""

from typing import Any, Optional

from pydantic import BaseModel


class GeneratorRequest(BaseModel):
    """Schema for data generation request."""

    generator_type: str
    count: int = 1
    params: Optional[dict] = None


class TemplateFieldRequest(BaseModel):
    """Schema for a single field in template generation request."""
    type: str
    label: str
    params: Optional[dict] = None


class TemplateGenerationRequest(BaseModel):
    """Schema for template-based data generation request."""
    template_name: Optional[str] = None
    fields: list[TemplateFieldRequest]
    count: int = 1


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


class TemplateGenerationResponse(BaseModel):
    """Schema for template-based generation response."""
    count: int
    data: list[dict[str, Any]]