"""API routes for generation history."""

import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.dependencies import get_database_session, verify_api_key
from app.models.generation_history import GenerationHistory
from app.schemas.generation_history import (
    HistoryDetail, 
    HistoryItem, 
    HistoryListResponse, 
    HistoryStats,
    BatchDeleteRequest
)

router = APIRouter(prefix="/history", tags=["历史记录"])


@router.get(
    "",
    response_model=HistoryListResponse,
    summary="获取历史记录列表",
    description="分页获取数据生成的历史记录。"
    "\n\n**查询参数：**"
    "\n- `skip` - 跳过记录数，默认 0"
    "\n- `limit` - 返回记录数，默认 50，最大 200"
    "\n- `generator_type` - 按生成器类型筛选"
    "\n- `status` - 按状态筛选：completed / failed"
    "\n- `date_from` - 起始时间（ISO格式）"
    "\n- `date_to` - 结束时间（ISO格式）",
)
def get_history_endpoint(
    request: Request,
    skip: int = Query(default=0, ge=0, description="跳过的记录数"),
    limit: int = Query(default=50, ge=1, le=200, description="返回的最大记录数"),
    generator_type: str | None = Query(default=None, description="按生成器类型筛选"),
    status: str | None = Query(default=None, description="按状态筛选"),
    date_from: str | None = Query(default=None, description="起始时间"),
    date_to: str | None = Query(default=None, description="结束时间"),
    db: Session = Depends(get_database_session),
    _: str | None = Depends(verify_api_key),
):
    query = db.query(GenerationHistory)

    if generator_type:
        query = query.filter(GenerationHistory.generator_type == generator_type)
    if status:
        query = query.filter(GenerationHistory.status == status)
    if date_from:
        query = query.filter(GenerationHistory.created_at >= datetime.fromisoformat(date_from))
    if date_to:
        query = query.filter(GenerationHistory.created_at <= datetime.fromisoformat(date_to))

    total = query.count()
    items = query.order_by(GenerationHistory.id.desc()).offset(skip).limit(limit).all()

    return HistoryListResponse(
        items=[HistoryItem.model_validate(item) for item in items],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/stats",
    response_model=HistoryStats,
    summary="获取历史统计",
    description="获取历史记录的统计信息，包括总次数、总生成数、成功/失败次数。",
)
def get_history_stats_endpoint(
    request: Request,
    db: Session = Depends(get_database_session),
    _: str | None = Depends(verify_api_key),
):

    total_count = db.query(GenerationHistory).count()
    completed_count = db.query(GenerationHistory).filter(GenerationHistory.status == "completed").count()
    failed_count = db.query(GenerationHistory).filter(GenerationHistory.status == "failed").count()
    total_generated = (
        db.query(GenerationHistory).with_entities(GenerationHistory.count).filter(
            GenerationHistory.status == "completed"
        ).all()
    )
    total_generated = sum(row.count for row in total_generated)

    return HistoryStats(
        total_count=total_count,
        total_generated=total_generated,
        completed_count=completed_count,
        failed_count=failed_count,
    )


@router.get(
    "/{history_id}",
    response_model=HistoryDetail,
    summary="获取历史记录详情",
    description="根据 ID 获取单条历史记录的详细信息，包含生成的数据预览。",
)
def get_history_detail_endpoint(
    request: Request,
    history_id: int,
    db: Session = Depends(get_database_session),
    _: str | None = Depends(verify_api_key),
):
    history = db.query(GenerationHistory).filter(GenerationHistory.id == history_id).first()
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="历史记录不存在")

    result_data = None
    if history.result_data:
        try:
            result_data = json.loads(history.result_data)
        except (json.JSONDecodeError, TypeError):
            result_data = None

    params = None
    if history.params:
        try:
            params = json.loads(history.params)
        except (json.JSONDecodeError, TypeError):
            params = None

    return HistoryDetail(
        id=history.id,
        generator_type=history.generator_type,
        count=history.count,
        status=history.status,
        params=params,
        result_data=result_data,
        error_msg=history.error_msg,
        client_ip=history.client_ip,
        created_at=history.created_at,
        completed_at=history.completed_at,
        duration_ms=history.duration_ms,
    )


@router.delete(
    "/{history_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除历史记录",
    description="根据 ID 删除一条历史记录。",
)
def delete_history_endpoint(
    request: Request,
    history_id: int,
    db: Session = Depends(get_database_session),
    _: str | None = Depends(verify_api_key),
):
    history = db.query(GenerationHistory).filter(GenerationHistory.id == history_id).first()
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="历史记录不存在")

    db.delete(history)
    db.commit()


@router.post(
    "/batch-delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="批量删除历史记录",
    description="根据 ID 列表批量删除历史记录。",
)
def batch_delete_history_endpoint(
    request: Request,
    body: BatchDeleteRequest,
    db: Session = Depends(get_database_session),
    _: str | None = Depends(verify_api_key),
):
    if not body.ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="请选择要删除的历史记录")
    
    # 删除指定的记录
    db.query(GenerationHistory).filter(GenerationHistory.id.in_(body.ids)).delete(synchronize_session=False)
    db.commit()