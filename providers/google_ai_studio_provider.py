from __future__ import annotations

import os
from typing import Any

import requests

from .base_provider import BaseProvider, ProviderResult


class GoogleAIStudioProvider(BaseProvider):
    name = "google-ai-studio"
    provider_type = "api"

    def __init__(self, base_url: str, api_key_env: str, default_model: str = "gemini-2.0-flash") -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.default_model = default_model

    def is_available(self) -> tuple[bool, str]:
        if not os.getenv(self.api_key_env):
            return False, f"Missing environment variable {self.api_key_env}."
        return True, f"API key env {self.api_key_env} is set."

    def generate(self, prompt: str, model: str = "", temperature: float = 0.0) -> ProviderResult:
        key = os.getenv(self.api_key_env, "")
        model_name = model or self.default_model
        url = f"{self.base_url}/{model_name}:generateContent?key={key}"
        body: dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": temperature},
        }
        try:
            response = requests.post(url, json=body, timeout=120)
            response.raise_for_status()
            data = response.json()
            candidates = data.get("candidates", [])
            text = ""
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                text = "\n".join(part.get("text", "") for part in parts if part.get("text"))
            return ProviderResult(provider_name=self.name, model=model_name, text=text.strip(), success=True, metadata={"raw": data})
        except Exception as exc:
            return ProviderResult(provider_name=self.name, model=model_name, text="", success=False, error=str(exc))
