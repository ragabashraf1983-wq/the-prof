from __future__ import annotations

from .provider_router import ProviderRouter


class ProviderTester:
    def __init__(self, router: ProviderRouter) -> None:
        self.router = router

    def test_all(self) -> list[dict[str, str]]:
        return self.router.detect_available_providers()

    def test_one(self, provider_name: str) -> dict[str, str]:
        provider = self.router.get_provider(provider_name)
        available, message = provider.is_available()
        return {"name": provider_name, "available": "yes" if available else "no", "message": message}
