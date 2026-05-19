"""HTTP client for Qwen API integration."""

import httpx

from app.config import settings


class QwenClient:
    """Client for interacting with Qwen LLM API."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None, model: str = "qwen-plus"):
        """Initialize the Qwen client.

        Args:
            api_key: API key for authentication. Defaults to config settings.
            base_url: Base URL for the API. Defaults to config settings.
            model: Model name to use.
        """
        self.api_key = api_key or settings.qwen_api_key
        self.base_url = base_url or settings.qwen_base_url
        self.model = model
        self.timeout = 300.0

    def chat(self, prompt: str, system_prompt: str = "你是一个有用的助手。") -> str:
        """Send a chat message to the Qwen API.

        Args:
            prompt: User message content.
            system_prompt: System prompt to guide the model behavior.

        Returns:
            Text response from the model.

        Raises:
            RuntimeError: If API key is not configured.
            httpx.HTTPError: If the HTTP request fails.
        """
        if not self.api_key:
            raise RuntimeError("Qwen API key is not configured")

        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
