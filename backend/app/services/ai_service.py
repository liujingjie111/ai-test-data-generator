"""Service layer for AI-based data generation."""

import json

from app.exceptions import DataGenerationError
from app.utils.llm_client import QwenClient


def generate_with_ai(db, prompt: str, count: int) -> dict:
    """Generate test data using AI (Qwen API).

    Args:
        db: SQLAlchemy database session.
        prompt: User prompt describing the data to generate.
        count: Number of items to generate.

    Returns:
        Dictionary with generated data list and metadata.

    Raises:
        DataGenerationError: If AI generation fails.
    """
    system_prompt = (
        "你是一个专业的测试数据生成器。请根据用户的提示生成JSON格式的测试数据。"
        "返回格式必须是一个JSON数组，每个元素是一个对象。不要包含任何其他解释。"
    )

    full_prompt = f"{prompt}\n\n请生成 {count} 条数据。"

    try:
        client = QwenClient()
        response_text = client.chat(prompt=full_prompt, system_prompt=system_prompt)

        start_idx = response_text.find("[")
        end_idx = response_text.rfind("]") + 1
        if start_idx == -1 or end_idx == 0:
            raise DataGenerationError(
                message="Invalid response format from AI",
                details={"response": response_text[:200]},
            )

        json_str = response_text[start_idx:end_idx]
        data = json.loads(json_str)

        return {
            "prompt": prompt,
            "count": len(data),
            "data": data,
        }
    except DataGenerationError:
        raise
    except json.JSONDecodeError as e:
        raise DataGenerationError(
            message="Failed to parse AI response as JSON",
            details={"error": str(e)},
        ) from e
    except Exception as e:
        raise DataGenerationError(
            message="AI generation failed",
            details={"error": str(e)},
        ) from e
