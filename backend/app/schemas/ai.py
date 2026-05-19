"""AI request and response schemas."""

from pydantic import BaseModel, Field
from typing import Optional


class AIRequest(BaseModel):
    """Schema for AI data generation request."""

    prompt: str
    count: int = 1
    api_key: Optional[str] = None
    model: Optional[str] = Field(default="qwen-plus", description="AI模型名称")


class AIResponse(BaseModel):
    """Schema for AI data generation response."""

    prompt: str
    count: int
    data: list[dict]
