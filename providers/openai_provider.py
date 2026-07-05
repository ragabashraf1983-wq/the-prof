from __future__ import annotations

import os
from typing import Any

import requests

from .base_provider import BaseProvider, ProviderResult


class OpenAICompatibleProvider(BaseProvider):
    name = "openai-compatible"
    provider_type = "api"

    def __init__(self, name: str, base_url: str, api_key_env: str, default_model: str = "") -> None:
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.default_model = default_model

    def _headers(self) -> dict[str, str]:
        api_key = os.getenv(self.api_key_env, "")
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def is_available(self) -> tuple[bool, str]:
        if not os.getenv(self.api_key_env):
            return False, f"Missing environment variable {self.api_key_env}."
        return True, f"API key env {self.api_key_env} is set."

    def generate(self, prompt: str, model: str = "", temperature: float = 0.0) -> ProviderResult:
        model_name = model or self.default_model
        body: dict[str, Any] = {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "Use only provided evidence. Unsupported claims must be written exactly as Do not know.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
        }
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=self._headers(), json=body, timeout=120)
            response.raise_for_status()
            data = response.json()
            text = data["choices"][0]["message"]["content"]
            return ProviderResult(provider_name=self.name, model=model_name, text=text.strip(), success=True, metadata={"id": data.get("id", "")})
        except Exception as exc:
            return ProviderResult(provider_name=self.name, model=model_name, text="", success=False, error=str(exc))
