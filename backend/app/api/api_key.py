"""API routes for API key management operations."""

import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_database_session
from app.models.api_key import ApiKey
from app.schemas import ApiKeyCreate, ApiKeyResponse

router = APIRouter(prefix="/api-keys", tags=["API密钥管理"])


@router.get(
    "",
    response_model=list[ApiKeyResponse],
    summary="获取 API 密钥列表",
    description="获取所有已创建的 API 密钥。"
    "\n\n**返回字段：**"
    "\n- `id` - 密钥 ID"
    "\n- `key` - 密钥值（以 `sk-` 开头）"
    "\n- `name` - 密钥名称"
    "\n- `is_active` - 是否启用"
    "\n- `created_at` - 创建时间"
    "\n- `expires_at` - 过期时间（可选）"
    "\n\n**使用方式：**"
    "\n在需要认证的接口请求头中添加：`Authorization: Bearer <your_api_key>`",
)
def list_api_keys_endpoint(db: Session = Depends(get_database_session)):
    """获取所有 API 密钥。

    Args:
        db: 数据库会话。

    Returns:
        API 密钥列表。
    """
    api_keys = db.query(ApiKey).all()
    return api_keys


@router.post(
    "",
    response_model=ApiKeyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="创建 API 密钥",
    description="创建一个新的 API 访问密钥。"
    "\n\n**请求体：**"
    "\n```json"
    "\n{"
    '\n  "name": "我的测试密钥",'
    '\n  "expires_at": "2025-12-31T23:59:59"'
    "\n}"
    "\n```"
    "\n\n- `name` - 密钥名称（必填）"
    "\n- `expires_at` - 过期时间（可选），ISO 8601 格式"
    "\n\n**注意：**"
    "\n- 密钥创建后会立即返回 `key` 字段，请妥善保存"
    "\n- 密钥一旦丢失无法找回，只能重新创建",
)
def create_api_key_endpoint(request: ApiKeyCreate, db: Session = Depends(get_database_session)):
    """创建一个新的 API 密钥。

    Args:
        request: 包含密钥名称和可选过期时间的请求体。
        db: 数据库会话。

    Returns:
        新创建的 API 密钥信息。
    """
    generated_key = f"sk-{secrets.token_hex(32)}"

    db_api_key = ApiKey(
        key=generated_key,
        name=request.name,
        is_active=True,
        expires_at=request.expires_at,
    )
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)

    return db_api_key


@router.delete(
    "/{key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除 API 密钥",
    description="根据 ID 删除一个 API 密钥。删除后立即失效，不可恢复。",
)
def delete_api_key_endpoint(key_id: int, db: Session = Depends(get_database_session)):
    """根据 ID 删除一个 API 密钥。

    Args:
        key_id: 要删除的密钥 ID。
        db: 数据库会话。
    """
    api_key = db.get(ApiKey, key_id)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API key with id '{key_id}' not found",
        )

    db.delete(api_key)
    db.commit()