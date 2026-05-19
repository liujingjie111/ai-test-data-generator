"""API routes for data generation operations."""

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_database_session, verify_api_key
from app.schemas import (
    ExportRequest, GeneratorRequest, GeneratorResponse,
    TemplateGenerationRequest, TemplateGenerationResponse
)
from app.services import (
    export_to_csv_bytes, export_to_excel, export_to_json, export_to_sql,
    generate_data, generate_template_data
)

router = APIRouter(prefix="/generate", tags=["数据生成"])


@router.post(
    "",
    response_model=GeneratorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="生成测试数据",
    description="根据指定的生成器类型生成测试数据。"
    "\n\n**支持的生成器类型：**"
    "\n- `name` - 姓名"
    "\n- `email` - 邮箱"
    "\n- `phone` - 手机号"
    "\n- `id_card` - 身份证号"
    "\n- `gender` - 性别"
    "\n- `age` - 年龄"
    "\n- `birth_date` - 出生日期"
    "\n- `province` - 省份"
    "\n- `city` - 城市"
    "\n- `district` - 区县"
    "\n- `address` - 详细地址"
    "\n- `postcode` - 邮编"
    "\n- `latitude` - 纬度"
    "\n- `longitude` - 经度"
    "\n- `full_address` - 完整地址"
    "\n- `bank_card` - 银行卡号"
    "\n- `credit_card` - 信用卡号"
    "\n- `bank_name` - 开户行"
    "\n- `amount` - 金额"
    "\n- `company_name` - 公司名称"
    "\n- `credit_code` - 统一社会信用代码"
    "\n- `industry` - 行业"
    "\n- `company_address` - 公司地址"
    "\n- `company_phone` - 公司电话"
    "\n- `product_name` - 商品名称"
    "\n- `sku` - SKU"
    "\n- `price` - 价格"
    "\n- `stock` - 库存"
    "\n- `category` - 分类"
    "\n- `uuid` - UUID"
    "\n- `ip` - IP地址"
    "\n- `mac` - MAC地址"
    "\n- `url` - URL"
    "\n- `timestamp` - 时间戳"
    "\n- `random_string` - 随机字符串"
    "\n\n**使用示例：**"
    "\n```json"
    '\n{'
    '\n  "generator_type": "name",'
    '\n  "count": 10'
    "\n}"
    "\n```",
)
def generate_data_endpoint(
    request: GeneratorRequest,
    request_obj: Request,
    db: Session = Depends(get_database_session),
    _: str | None = Depends(verify_api_key),
):
    """根据指定的生成器类型生成测试数据。

    Args:
        request: 包含生成器类型、数量和可选参数的请求体。
        request_obj: FastAPI Request 对象，用于获取客户端 IP。
        db: 数据库会话，用于记录历史。

    Returns:
        包含生成数据的响应。
    """
    client_ip = request_obj.client.host if request_obj.client else None
    generated_items = generate_data(
        generator_type=request.generator_type,
        count=request.count,
        params=request.params,
        db=db,
        client_ip=client_ip,
    )
    return GeneratorResponse(count=len(generated_items), data=generated_items)


@router.post(
    "/{generator_type}/export",
    summary="生成并导出数据",
    description="根据指定的生成器类型生成数据并导出为文件。"
    "\n\n**支持的导出格式：**"
    "\n- `json` - JSON 文件"
    "\n- `csv` - CSV 表格文件（Excel 可直接打开）"
    "\n- `excel` - Excel (.xlsx) 文件"
    "\n- `sql` - SQL INSERT 语句文件"
    "\n\n**使用示例：**"
    "\n- generator_type: `name`"
    "\n- format: `csv`"
    "\n- Request body: `{\"count\": 100}`"
    "\n\n导出 100 个姓名到 CSV 文件。",
)
def export_data_endpoint(
    generator_type: str,
    format: str,
    request_obj: Request,
    request: ExportRequest | None = None,
    db: Session = Depends(get_database_session),
    _: str | None = Depends(verify_api_key),
):
    """根据指定的生成器类型生成数据并导出为文件。

    Args:
        generator_type: 生成器类型（路径参数）。
        format: 导出格式（查询参数），支持 json/csv/excel/sql。
        request_obj: FastAPI Request 对象，用于获取客户端 IP。
        request: 可选的请求体，包含生成数量和参数。
        db: 数据库会话，用于记录历史。

    Returns:
        文件响应，包含指定格式的数据。
    """
    valid_formats = ["json", "csv", "excel", "sql"]
    if format not in valid_formats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid format. Must be one of: {', '.join(valid_formats)}",
        )

    count = request.count if request else 1
    params = request.params if request else None

    client_ip = request_obj.client.host if request_obj.client else None
    generated_items = generate_data(
        generator_type=generator_type,
        count=count,
        params=params,
        db=db,
        client_ip=client_ip,
    )

    export_data = [item["data"] for item in generated_items]

    if format == "json":
        content = export_to_json(export_data)
        return Response(
            content=content,
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="{generator_type}.json"'},
        )

    if format == "csv":
        content = export_to_csv_bytes(export_data)
        return Response(
            content=content,
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{generator_type}.csv"'},
        )

    if format == "excel":
        content = export_to_excel(export_data)
        return Response(
            content=content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{generator_type}.xlsx"'},
        )

    if format == "sql":
        content = export_to_sql(export_data, table_name=generator_type)
        return Response(
            content=content,
            media_type="text/plain",
            headers={"Content-Disposition": f'attachment; filename="{generator_type}.sql"'},
        )


@router.post(
    "/template",
    response_model=TemplateGenerationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="使用模板生成数据",
    description="使用自定义模板或保存的模板生成多字段测试数据。"
)
def generate_template_data_endpoint(
    request: TemplateGenerationRequest,
    request_obj: Request,
    db: Session = Depends(get_database_session),
    _: str | None = Depends(verify_api_key),
):
    """使用模板生成测试数据，只保存一条历史记录。

    Args:
        request: 包含模板名称、字段定义和数量的请求体。
        request_obj: FastAPI Request 对象，用于获取客户端 IP。
        db: 数据库会话，用于记录历史。

    Returns:
        包含生成数据的响应（每行是一个包含所有字段的对象）。
    """
    client_ip = request_obj.client.host if request_obj.client else None
    fields_dicts = [field.model_dump() for field in request.fields]
    generated_items = generate_template_data(
        template_name=request.template_name,
        fields=fields_dicts,
        count=request.count,
        db=db,
        client_ip=client_ip,
    )
    return TemplateGenerationResponse(count=len(generated_items), data=generated_items)