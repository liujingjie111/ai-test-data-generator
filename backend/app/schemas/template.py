"""Template request and response schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TemplateField(BaseModel):
    """Schema for a single template field definition."""

    type: str
    label: str
    required: bool = False
    options: Optional[dict] = None


class TemplateCreate(BaseModel):
    """Schema for creating a new template."""

    name: str
    description: Optional[str] = None
    fields: list[TemplateField]


class TemplateUpdate(BaseModel):
    """Schema for updating an existing template."""

    name: Optional[str] = None
    description: Optional[str] = None
    fields: Optional[list[TemplateField]] = None


class TemplateResponse(BaseModel):
    """Schema for template response data."""

    id: int
    name: str
    description: str
    fields: list[TemplateField]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
