"""Service layer for data generation operations."""

import json
import time
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.exceptions import DataGenerationError
from app.models.generation_history import GenerationHistory
from app.utils.data_generators.registry import get_generator


RANGE_VALIDATION_RULES = {
    'age': {
        'min_key': 'min_age',
        'max_key': 'max_age',
        'min_limit': 0,
        'max_limit': 150,
        'label': '年龄',
    },
    'amount': {
        'min_key': 'min_amount',
        'max_key': 'max_amount',
        'min_limit': 0,
        'max_limit': 1000000,
        'label': '金额',
    },
    'price': {
        'min_key': 'min_price',
        'max_key': 'max_price',
        'min_limit': 0,
        'max_limit': 1000000,
        'label': '价格',
    },
    'stock': {
        'min_key': 'min_stock',
        'max_key': 'max_stock',
        'min_limit': 0,
        'max_limit': 10000000,
        'label': '库存',
    },
}


def _validate_range_params(generator_type: str, params: dict | None) -> None:
    """Validate range parameters for generators that support min/max.

    Args:
        generator_type: The type of generator being validated.
        params: Optional parameters to validate.

    Raises:
        DataGenerationError: If range parameters are invalid.
    """
    if not params or generator_type not in RANGE_VALIDATION_RULES:
        return

    rule = RANGE_VALIDATION_RULES[generator_type]
    
    # 向后兼容：支持旧的 min/max 参数名
    # 显式检查 None，避免 0 值被错误忽略
    min_val = params.get(rule['min_key']) if params.get(rule['min_key']) is not None else params.get('min')
    max_val = params.get(rule['max_key']) if params.get(rule['max_key']) is not None else params.get('max')

    if min_val is None or max_val is None:
        return

    if min_val > max_val:
        raise DataGenerationError(
            message=f"{rule['label']}最小值不能大于最大值",
            details={
                "generator_type": generator_type,
                "min": min_val,
                "max": max_val,
            },
        )

    if min_val < rule['min_limit'] or max_val > rule['max_limit']:
        raise DataGenerationError(
            message=f"{rule['label']}范围应在 {rule['min_limit']}-{rule['max_limit']} 之间",
            details={
                "generator_type": generator_type,
                "min": min_val,
                "max": max_val,
                "valid_range": [rule['min_limit'], rule['max_limit']],
            },
        )


def generate_data(
    generator_type: str,
    count: int,
    params: dict | None = None,
    db: Optional[Session] = None,
    client_ip: Optional[str] = None,
    api_key_id: Optional[int] = None,
) -> list[dict[str, Any]]:
    """Generate test data using the specified generator type.

    Args:
        generator_type: The type of data to generate (e.g., 'name', 'email', 'phone').
        count: Number of items to generate (1-100000).
        params: Optional parameters to pass to the generator function.
        db: Optional database session for recording history.
        client_ip: Optional client IP address for history tracking.
        api_key_id: Optional API key ID for history tracking.

    Returns:
        List of generated data dictionaries.

    Raises:
        DataGenerationError: If generator_type is not found or generation fails.
    """
    if count < 1 or count > 100000:
        raise DataGenerationError(
            message="Count must be between 1 and 100000",
            details={"count": count},
        )

    try:
        generator_func = get_generator(generator_type)
    except ValueError as e:
        raise DataGenerationError(
            message=str(e),
            details={"generator_type": generator_type},
        ) from e

    _validate_range_params(generator_type, params)

    # 准备传递给生成器的参数，处理兼容性
    generator_params = {}
    if params:
        if generator_type in RANGE_VALIDATION_RULES:
                rule = RANGE_VALIDATION_RULES[generator_type]
                # 优先使用新的参数名
                # 显式检查 None，避免 0 值被错误忽略
                generator_params[rule['min_key']] = params.get(rule['min_key']) if params.get(rule['min_key']) is not None else params.get('min')
                generator_params[rule['max_key']] = params.get(rule['max_key']) if params.get(rule['max_key']) is not None else params.get('max')
                # 移除None值
                generator_params = {k: v for k, v in generator_params.items() if v is not None}
        else:
            generator_params = params

    history_id = None
    if db is not None:
        history = GenerationHistory(
            generator_type=generator_type,
            count=count,
            status="running",
            params=json.dumps(params or {}, ensure_ascii=False),
            client_ip=client_ip,
            api_key_id=api_key_id,
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        history_id = history.id

    start_time = time.time()
    try:
        result = []
        for _ in range(count):
            if generator_params:
                value = generator_func(**generator_params)
            else:
                value = generator_func()
            result.append({"data": value})

        elapsed = int((time.time() - start_time) * 1000)

        if history_id is not None and db is not None:
            history = db.query(GenerationHistory).filter(GenerationHistory.id == history_id).first()
            if history:
                history.status = "completed"
                history.result_data = json.dumps(result[:100], ensure_ascii=False)
                history.completed_at = __import__("datetime").datetime.utcnow()
                history.duration_ms = elapsed
                db.commit()

        return result
    except Exception as e:
        elapsed = int((time.time() - start_time) * 1000)
        if history_id is not None and db is not None:
            history = db.query(GenerationHistory).filter(GenerationHistory.id == history_id).first()
            if history:
                history.status = "failed"
                history.error_msg = str(e)
                history.completed_at = __import__("datetime").datetime.utcnow()
                history.duration_ms = elapsed
                db.commit()

        raise DataGenerationError(
            message="Failed to generate data",
            details={"generator_type": generator_type, "error": str(e)},
        ) from e


def generate_template_data(
    template_name: Optional[str],
    fields: list[dict[str, Any]],
    count: int,
    db: Optional[Session] = None,
    client_ip: Optional[str] = None,
    api_key_id: Optional[int] = None,
) -> list[dict[str, Any]]:
    """Generate data from a template with multiple fields, recording only one history entry.

    Args:
        template_name: Name of the template being used.
        fields: List of field definitions with type, label, and params.
        count: Number of items to generate.
        db: Optional database session for recording history.
        client_ip: Optional client IP address for history tracking.
        api_key_id: Optional API key ID for history tracking.

    Returns:
        List of generated data dictionaries (each dict has all field labels as keys).

    Raises:
        DataGenerationError: If any field generation fails.
    """
    if count < 1 or count > 100000:
        raise DataGenerationError(
            message="Count must be between 1 and 100000",
            details={"count": count},
        )

    # Validate all field generators first
    generators = []
    field_labels = []
    for field in fields:
        try:
            generator_func = get_generator(field['type'])
            params = field.get('params', {})
            
            # 准备传递给生成器的参数，处理兼容性
            generator_params = {}
            if params:
                if field['type'] in RANGE_VALIDATION_RULES:
                    rule = RANGE_VALIDATION_RULES[field['type']]
                    # 优先使用新的参数名
                    # 显式检查 None，避免 0 值被错误忽略
                    generator_params[rule['min_key']] = params.get(rule['min_key']) if params.get(rule['min_key']) is not None else params.get('min')
                    generator_params[rule['max_key']] = params.get(rule['max_key']) if params.get(rule['max_key']) is not None else params.get('max')
                    # 移除None值
                    generator_params = {k: v for k, v in generator_params.items() if v is not None}
                else:
                    generator_params = params
            
            generators.append((generator_func, generator_params))
            field_labels.append(field['label'])
            _validate_range_params(field['type'], params)
        except ValueError as e:
            raise DataGenerationError(
                message=f"Invalid field type '{field['type']}': {str(e)}",
                details={"field": field},
            ) from e

    # Create history entry
    history_id = None
    generator_type_display = f"template:{template_name or 'custom'}"
    if db is not None:
        history = GenerationHistory(
            generator_type=generator_type_display,
            count=count,
            status="running",
            params=json.dumps({"template_name": template_name, "fields": fields}, ensure_ascii=False),
            client_ip=client_ip,
            api_key_id=api_key_id,
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        history_id = history.id

    start_time = time.time()
    try:
        # Generate all field data first
        all_field_results = []
        for generator_func, params in generators:
            field_result = []
            for _ in range(count):
                if params:
                    value = generator_func(**params)
                else:
                    value = generator_func()
                field_result.append(value)
            all_field_results.append(field_result)

        # Combine into rows
        result = []
        for i in range(count):
            row = {}
            for field_idx, label in enumerate(field_labels):
                row[label] = all_field_results[field_idx][i]
            result.append(row)

        elapsed = int((time.time() - start_time) * 1000)

        if history_id is not None and db is not None:
            history = db.query(GenerationHistory).filter(GenerationHistory.id == history_id).first()
            if history:
                history.status = "completed"
                history.result_data = json.dumps(result[:100], ensure_ascii=False)
                history.completed_at = __import__("datetime").datetime.utcnow()
                history.duration_ms = elapsed
                db.commit()

        return result
    except Exception as e:
        elapsed = int((time.time() - start_time) * 1000)
        if history_id is not None and db is not None:
            history = db.query(GenerationHistory).filter(GenerationHistory.id == history_id).first()
            if history:
                history.status = "failed"
                history.error_msg = str(e)
                history.completed_at = __import__("datetime").datetime.utcnow()
                history.duration_ms = elapsed
                db.commit()

        raise DataGenerationError(
            message="Failed to generate template data",
            details={"error": str(e)},
        ) from e
