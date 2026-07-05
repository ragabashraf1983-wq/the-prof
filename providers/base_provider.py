from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ProviderResult:
    provider_name: str
    model: str
    text: str
    success: bool
    error: str = ""
    metadata: dict[str, Any] | None = None


class BaseProvider(ABC):
    name: str = "base"
    provider_type: str = "base"

    @abstractmethod
    def is_available(self) -> tuple[bool, str]:
        raise NotImplementedError

    @abstractmethod
    def generate(self, prompt: str, model: str = "", temperature: float = 0.0) -> ProviderResult:
        raise NotImplementedError
