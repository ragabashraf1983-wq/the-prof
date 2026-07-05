from __future__ import annotations

from .base_provider import BaseProvider, ProviderResult


class RulesProvider(BaseProvider):
    name = "rules"
    provider_type = "local"

    def is_available(self) -> tuple[bool, str]:
        return True, "Built-in deterministic rule provider is always available."

    def generate(self, prompt: str, model: str = "rules-v1", temperature: float = 0.0) -> ProviderResult:
        text = (
            "Rule-based provider fallback used.\n\n"
            "The Prof kept generation conservative because no external or local LLM was available.\n"
            "Use only the supplied evidence, and mark unsupported content as `Do not know.`"
        )
        return ProviderResult(provider_name=self.name, model=model, text=text, success=True, metadata={"mode": "deterministic"})
