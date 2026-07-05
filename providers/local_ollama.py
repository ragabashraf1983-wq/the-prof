from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from .base_provider import BaseProvider, ProviderResult


@dataclass(slots=True)
class OllamaModelInfo:
    name: str
    size: int = 0
    family: str = ""
    parameter_size: str = ""
    quantization_level: str = ""


class LocalOllamaProvider(BaseProvider):
    name = "ollama"
    provider_type = "local"

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def is_available(self) -> tuple[bool, str]:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            response.raise_for_status()
            return True, "Ollama responded to /api/tags."
        except Exception as exc:
            return False, str(exc)

    def list_models(self) -> list[OllamaModelInfo]:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            payload = response.json()
        except Exception:
            return []
        models = []
        for item in payload.get("models", []):
            details = item.get("details", {})
            models.append(
                OllamaModelInfo(
                    name=item.get("name", "unknown"),
                    size=item.get("size", 0),
                    family=details.get("family", ""),
                    parameter_size=details.get("parameter_size", ""),
                    quantization_level=details.get("quantization_level", ""),
                )
            )
        return models

    def generate(self, prompt: str, model: str = "", temperature: float = 0.0) -> ProviderResult:
        model_name = model or "llama3.2"
        payload: dict[str, Any] = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
        try:
            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return ProviderResult(
                provider_name=self.name,
                model=model_name,
                text=str(data.get("response", "")).strip(),
                success=True,
                metadata={"raw": data},
            )
        except Exception as exc:
            return ProviderResult(provider_name=self.name, model=model_name, text="", success=False, error=str(exc))
