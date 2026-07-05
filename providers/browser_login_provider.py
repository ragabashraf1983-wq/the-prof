from __future__ import annotations

from .base_provider import BaseProvider, ProviderResult


class BrowserLoginProvider(BaseProvider):
    name = "browser-login"
    provider_type = "browser-login"

    def is_available(self) -> tuple[bool, str]:
        return False, "Browser-login adapters are disabled by default and require explicit user configuration."

    def generate(self, prompt: str, model: str = "", temperature: float = 0.0) -> ProviderResult:
        return ProviderResult(
            provider_name=self.name,
            model=model or "disabled",
            text="",
            success=False,
            error=(
                "Browser-login provider is disabled. It must never bypass authentication, CAPTCHAs, paywalls, "
                "or rate limits."
            ),
        )
