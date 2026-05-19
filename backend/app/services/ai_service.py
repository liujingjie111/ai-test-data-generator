"""Service layer for AI-based data generation."""

import datetime
import json
import time
from typing import Optional

from sqlalchemy.orm import Session

from app.exceptions import DataGenerationError
from app.models.generation_history import GenerationHistory
from app.utils.llm_client import QwenClient


def generate_with_ai(
    db: Session, 
    prompt: str, 
    count: int, 
    api_key: str | None = None, 
    model: str | None = None,
    client_ip: Optional[str] = None,
) -> dict:
    """Generate test data using AI (Qwen API).

    Args:
        db: SQLAlchemy database session.
        prompt: User prompt describing the data to generate.
        count: Number of items to generate.
        api_key: Optional API key from client.
        model: Optional model name from client.
        client_ip: Optional client IP address for history tracking.

    Returns:
        Dictionary with generated data list and metadata.

    Raises:
        DataGenerationError: If AI generation fails.
    """
    system_prompt = (
        "你是一个专业的测试数据生成器。请严格按照以下要求执行：\n"
        "1. 完全按照用户的提示内容生成对应的测试数据，不要回答无关问题。\n"
        "2. 你的返回内容必须只有一个纯JSON数组，不能包含任何其他文字说明、问候语或markdown格式。\n"
        "3. 数组中的每个元素是一个对象，字段和值要符合用户描述的逻辑。\n"
        "4. 例如：如果用户要生成用户信息，返回类似 [{\"name\": \"张三\", \"age\": 25}, ...] 这样的纯JSON数组。\n"
        "5. 不要包含任何自然语言的对话内容，只返回JSON数据！"
    )

    all_data = []
    batch_size = 20  # 每批生成20条
    batches = (count + batch_size - 1) // batch_size

    # 保存历史记录 - 开始
    history_id = None
    history = GenerationHistory(
        generator_type="ai_generation",
        count=count,
        status="running",
        params=json.dumps({
            "prompt": prompt,
            "model": model or "qwen-plus"
        }, ensure_ascii=False),
        client_ip=client_ip,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    history_id = history.id

    start_time = time.time()

    try:
        client = QwenClient(api_key=api_key, model=model or "qwen-plus")

        for i in range(batches):
            current_batch_size = min(batch_size, count - len(all_data))
            full_prompt = f"{prompt}\n\n请生成 {current_batch_size} 条数据。"

            response_text = client.chat(prompt=full_prompt, system_prompt=system_prompt)

            start_idx = response_text.find("[")
            end_idx = response_text.rfind("]") + 1
            if start_idx == -1 or end_idx == 0:
                raise DataGenerationError(
                    message="Invalid response format from AI",
                    details={"response": response_text[:200]},
                )

            json_str = response_text[start_idx:end_idx]
            batch_data = json.loads(json_str)

            # 确保不超过需要的数量
            if len(all_data) + len(batch_data) > count:
                batch_data = batch_data[:count - len(all_data)]

            all_data.extend(batch_data)

        elapsed = int((time.time() - start_time) * 1000)

        # 保存成功历史记录
        history = db.query(GenerationHistory).filter(GenerationHistory.id == history_id).first()
        if history:
            history.status = "completed"
            history.result_data = json.dumps(all_data[:100], ensure_ascii=False)
            history.completed_at = datetime.datetime.utcnow()
            history.duration_ms = elapsed
            db.commit()

        return {
            "prompt": prompt,
            "count": len(all_data),
            "data": all_data,
        }
    except DataGenerationError:
        # 保存失败历史记录
        elapsed = int((time.time() - start_time) * 1000)
        history = db.query(GenerationHistory).filter(GenerationHistory.id == history_id).first()
        if history:
            history.status = "failed"
            history.completed_at = datetime.datetime.utcnow()
            history.duration_ms = elapsed
            history.error_msg = "Data generation failed"
            db.commit()
        raise
    except json.JSONDecodeError as e:
        # 保存失败历史记录
        elapsed = int((time.time() - start_time) * 1000)
        history = db.query(GenerationHistory).filter(GenerationHistory.id == history_id).first()
        if history:
            history.status = "failed"
            history.completed_at = datetime.datetime.utcnow()
            history.duration_ms = elapsed
            history.error_msg = f"Failed to parse AI response as JSON: {str(e)}"
            db.commit()
        raise DataGenerationError(
            message="Failed to parse AI response as JSON",
            details={"error": str(e)},
        ) from e
    except Exception as e:
        # 保存失败历史记录
        elapsed = int((time.time() - start_time) * 1000)
        history = db.query(GenerationHistory).filter(GenerationHistory.id == history_id).first()
        if history:
            history.status = "failed"
            history.completed_at = datetime.datetime.utcnow()
            history.duration_ms = elapsed
            history.error_msg = str(e)
            db.commit()
        raise DataGenerationError(
            message="AI generation failed",
            details={"error": str(e)},
        ) from e
