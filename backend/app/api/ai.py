"""API routes for AI-powered data generation."""

import logging
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.dependencies import get_database_session, verify_api_key
from app.exceptions import DataGenerationError
from app.schemas import AIRequest, AIResponse
from app.services import generate_with_ai

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["AI生成"])


@router.post(
    "/generate",
    response_model=AIResponse,
    status_code=status.HTTP_201_CREATED,
    summary="AI 智能生成数据",
    description="使用通义千问 AI 模型，根据自然语言描述生成测试数据。"
    "\n\n**需要 API 密钥认证** - 请在请求头中添加：`Authorization: Bearer <your_api_key>`"
    "\n\n**支持的功能：**"
    "\n- 按条件生成数据（如年龄范围、地区等）"
    "\n- 生成复杂业务场景数据（如电商订单、用户行为）"
    "\n- 自定义字段组合"
    "\n\n**使用示例：**"
    "\n```json"
    "\n{"
    '\n  "prompt": "生成100个北京地区25-35岁男性用户数据，包含手机号和邮箱",'
    '\n  "count": 10'
    "\n}"
    "\n```"
    "\n\n**提示词示例：**"
    "\n- `生成50个电商订单数据，包含订单号、商品名称、价格、购买时间`"
    "\n- `生成30个企业员工信息，包含姓名、部门、职位、入职日期`"
    "\n- `生成20个学生成绩记录，包含学号、姓名、语文、数学、英语成绩`",
)
def generate_ai_data_endpoint(
    request: AIRequest,
    request_obj: Request,
    db: Session = Depends(get_database_session),
    _: str | None = Depends(verify_api_key),
):
    """使用 AI 生成测试数据。

    Args:
        request: 包含自然语言描述和生成数量的请求体。
        request_obj: FastAPI Request 对象，用于获取客户端 IP。
        db: 数据库会话。
        _: 验证通过的 API 密钥（为了一致性保留）。

    Returns:
        AI 生成的数据。
    """
    if request.count > 100:
        raise DataGenerationError(
            message="生成数量不能超过100条",
            details={"count": request.count},
        )

    client_ip = request_obj.client.host if request_obj.client else None
    
    logger.info(f"收到AI生成请求: prompt={request.prompt}, count={request.count}, model={request.model}")
    try:
        result = generate_with_ai(
            db=db,
            prompt=request.prompt,
            count=request.count,
            api_key=request.api_key,
            model=request.model,
            client_ip=client_ip
        )
        logger.info(f"AI生成成功: 生成了 {result['count']} 条数据")
        return AIResponse(prompt=result["prompt"], count=result["count"], data=result["data"])
    except Exception as e:
        logger.error(f"AI生成失败: {str(e)}", exc_info=True)
        raise