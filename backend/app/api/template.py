"""API routes for template management operations."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_database_session, verify_api_key
from app.schemas import TemplateCreate, TemplateResponse, TemplateUpdate
from app.services import copy_template, create_template, delete_template, get_template, list_templates, update_template

router = APIRouter(prefix="/templates", tags=["模板管理"])


@router.get(
    "",
    response_model=list[TemplateResponse],
    summary="获取模板列表",
    description="分页获取所有自定义模板。"
    "\n\n**查询参数：**"
    "\n- `skip` - 跳过记录数，默认 0"
    "\n- `limit` - 返回记录数，默认 100，最大 1000"
    "\n\n**使用示例：**"
    "\n```\nGET /api/templates?skip=0&limit=10\n```",
)
def get_templates_endpoint(
    skip: int = Query(default=0, ge=0, description="跳过的记录数"),
    limit: int = Query(default=100, ge=1, le=1000, description="返回的最大记录数"),
    db: Session = Depends(get_database_session),
    _: str | None = Depends(verify_api_key),
):
    """分页获取所有自定义模板。

    Args:
        skip: 跳过的记录数。
        limit: 返回的最大记录数。
        db: 数据库会话。

    Returns:
        模板列表。
    """
    return list_templates(db=db, skip=skip, limit=limit)


@router.post(
    "",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="创建模板",
    description="创建一个新的自定义数据模板。"
    "\n\n**请求体示例：**"
    "\n```json"
    "\n{"
    '\n  "name": "用户信息模板",'
    '\n  "description": "生成用户基本信息",'
    '\n  "fields": ['
    '\n    {"type": "name", "label": "姓名", "required": true},'
    '\n    {"type": "email", "label": "邮箱", "required": true},'
    '\n    {"type": "phone", "label": "手机号", "required": false}'
    "\n  ]"
    "\n}"
    "\n```",
)
def create_template_endpoint(template: TemplateCreate, db: Session = Depends(get_database_session), _: str | None = Depends(verify_api_key)):
    """创建一个新的自定义数据模板。

    Args:
        template: 包含模板名称、描述和字段定义的请求体。
        db: 数据库会话。

    Returns:
        创建成功的模板信息。
    """
    return create_template(db=db, template_data=template)


@router.get(
    "/{template_id}",
    response_model=TemplateResponse,
    summary="获取模板详情",
    description="根据 ID 获取单个模板的详细信息。"
    "\n\n**参数：**"
    "\n- `template_id` - 模板 ID（路径参数）",
)
def get_template_endpoint(template_id: int, db: Session = Depends(get_database_session), _: str | None = Depends(verify_api_key)):
    """根据 ID 获取单个模板的详细信息。

    Args:
        template_id: 模板 ID（路径参数）。
        db: 数据库会话。

    Returns:
        模板详细信息。
    """
    return get_template(db=db, template_id=template_id)


@router.put(
    "/{template_id}",
    response_model=TemplateResponse,
    summary="更新模板",
    description="更新已存在的模板信息。所有字段都是可选的，只会更新提供的字段。",
)
def update_template_endpoint(
    template_id: int,
    template: TemplateUpdate,
    db: Session = Depends(get_database_session),
    _: str | None = Depends(verify_api_key),
):
    """更新已存在的模板。

    Args:
        template_id: 要更新的模板 ID。
        template: 包含更新数据的请求体。
        db: 数据库会话。

    Returns:
        更新后的模板信息。
    """
    return update_template(db=db, template_id=template_id, update_data=template)


@router.delete(
    "/{template_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除模板",
    description="根据 ID 删除一个模板。删除后不可恢复。",
)
def delete_template_endpoint(template_id: int, db: Session = Depends(get_database_session), _: str | None = Depends(verify_api_key)):
    """根据 ID 删除一个模板。

    Args:
        template_id: 要删除的模板 ID。
        db: 数据库会话。
    """
    success = delete_template(db=db, template_id=template_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template with id '{template_id}' not found",
        )


@router.post(
    "/{template_id}/copy",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="复制模板",
    description="复制一个已存在的模板，生成一个名称带\"（副本）\"后缀的新模板。",
)
def copy_template_endpoint(template_id: int, db: Session = Depends(get_database_session), _: str | None = Depends(verify_api_key)):
    """复制一个已存在的模板。

    Args:
        template_id: 要复制的模板 ID。
        db: 数据库会话。

    Returns:
        复制后的新模板信息。
    """
    return copy_template(db=db, template_id=template_id)