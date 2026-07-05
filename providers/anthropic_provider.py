from __future__ import annotations

import os
from typing import Any

import requests

from .base_provider import BaseProvider, ProviderResult


class AnthropicProvider(BaseProvider):
    name = "anthropic"
    provider_type = "api"

    def __init__(self, base_url: str = "https://api.anthropic.com/v1/messages", api_key_env: str = "ANTHROPIC_API_KEY", default_model: str = "claude-3-5-sonnet-latest") -> None:
        self.base_url = base_url
        self.api_key_env = api_key_env
        self.default_model = default_model

    def is_available(self) -> tuple[bool, str]:
        if not os.getenv(self.api_key_env):
            return False, f"Missing environment variable {self.api_key_env}."
        return True, f"API key env {self.api_key_env} is set."

    def generate(self, prompt: str, model: str = "", temperature: float = 0.0) -> ProviderResult:
        api_key = os.getenv(self.api_key_env, "")
        model_name = model or self.default_model
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        body: dict[str, Any] = {
            "model": model_name,
            "max_tokens": 1200,
            "temperature": temperature,
            "system": "Use only provided evidence. Unsupported claims must be written exactly as Do not know.",
            "messages": [{"role": "user", "content": prompt}],
        }
        try:
            response = requests.post(self.base_url, headers=headers, json=body, timeout=120)
            response.raise_for_status()
            data = response.json()
            parts = data.get("content", [])
            text = "\n".join(part.get("text", "") for part in parts if part.get("type") == "text")
            return ProviderResult(provider_name=self.name, model=model_name, text=text.strip(), success=True, metadata={"id": data.get("id", "")})
        except Exception as exc:
            return ProviderResult(provider_name=self.name, model=model_name, text="", success=False, error=str(exc))
