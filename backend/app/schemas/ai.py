"""AI request and response schemas."""

from pydantic import BaseModel


class AIRequest(BaseModel):
    """Schema for AI data generation request."""

    prompt: str
    count: int = 1


class AIResponse(BaseModel):
    """Schema for AI data generation response."""

    prompt: str
    count: int
    data: list[dict]
