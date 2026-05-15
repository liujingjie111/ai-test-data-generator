"""Pydantic schemas for generation history."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class HistoryItem(BaseModel):
    id: int
    generator_type: str
    count: int
    status: str
    error_msg: Optional[str] = None
    client_ip: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None

    class Config:
        from_attributes = True


class HistoryDetail(BaseModel):
    id: int
    generator_type: str
    count: int
    status: str
    params: Optional[dict[str, Any]] = None
    result_data: Optional[list[dict[str, Any]]] = None
    error_msg: Optional[str] = None
    client_ip: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None

    class Config:
        from_attributes = True


class HistoryStats(BaseModel):
    total_count: int
    total_generated: int
    completed_count: int
    failed_count: int


class HistoryListResponse(BaseModel):
    items: list[HistoryItem]
    total: int
    skip: int
    limit: int


class BatchDeleteRequest(BaseModel):
    ids: list[int]