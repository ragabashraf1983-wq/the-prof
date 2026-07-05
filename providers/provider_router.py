from __future__ import annotations

from pathlib import Path
from typing import Any

from .anthropic_provider import AnthropicProvider
from .base_provider import BaseProvider, ProviderResult
from .browser_login_provider import BrowserLoginProvider
from .google_ai_studio_provider import GoogleAIStudioProvider
from .local_ollama import LocalOllamaProvider
from .openai_provider import OpenAICompatibleProvider
from .provider_catalog import ProviderCatalog
from .provider_usage import ProviderUsageTracker
from .rules_provider import RulesProvider


class ProviderRouter:
    def __init__(self, settings: dict[str, Any], root: Path, provider_catalog: ProviderCatalog | None = None) -> None:
        self.settings = settings
        self.root = root
        self.catalog = provider_catalog
        self.usage = ProviderUsageTracker()
        self.providers: dict[str, BaseProvider] = self._build_providers()
        self.failures: dict[str, int] = {}

    def _provider_from_profile(self, profile: dict[str, Any]) -> BaseProvider | None:
        adapter = profile.get("adapter", "")
        name = profile.get("name", "")
        base_url = profile.get("base_url", "")
        model = profile.get("model", "")
        api_key_env = profile.get("api_key_env", "")
        if adapter == "ollama":
            return LocalOllamaProvider(base_url or self.settings.get("ollama_base_url", "http://localhost:11434"))
        if adapter == "rules":
            return RulesProvider()
        if adapter == "anthropic":
            return AnthropicProvider(base_url=base_url or "https://api.anthropic.com/v1/messages", api_key_env=api_key_env or "ANTHROPIC_API_KEY", default_model=model or "claude-3-5-sonnet-latest")
        if adapter == "google-ai-studio":
            return GoogleAIStudioProvider(base_url=base_url or "https://generativelanguage.googleapis.com/v1beta/models", api_key_env=api_key_env or "GOOGLE_API_KEY", default_model=model or "gemini-2.0-flash")
        if adapter == "browser-login":
            return BrowserLoginProvider()
        if adapter in {"openai-compatible", "openai"}:
            return OpenAICompatibleProvider(name=name, base_url=base_url, api_key_env=api_key_env, default_model=model)
        if adapter == "cloudflare-workers-ai":
            return OpenAICompatibleProvider(name=name, base_url=base_url, api_key_env=api_key_env, default_model=model)
        return None

    def _build_providers(self) -> dict[str, BaseProvider]:
        profiles = self.catalog.load() if self.catalog else []
        providers: dict[str, BaseProvider] = {}
        for profile in profiles:
            provider = self._provider_from_profile(profile)
            if provider:
                providers[profile["name"]] = provider
        if "rules" not in providers:
            providers["rules"] = RulesProvider()
        return providers

    def detect_available_providers(self) -> list[dict[str, str]]:
        rows = []
        profile_map = {profile["name"]: profile for profile in (self.catalog.load() if self.catalog else [])}
        for name, provider in self.providers.items():
            available, message = provider.is_available()
            profile = profile_map.get(name, {})
            rows.append(
                {
                    "name": name,
                    "label": profile.get("label", name),
                    "category": profile.get("category", provider.provider_type),
                    "available": "yes" if available else "no",
                    "enabled": "yes" if profile.get("enabled", True) else "no",
                    "message": message,
                    "model": profile.get("model", ""),
                    "endpoint": profile.get("base_url", ""),
                }
            )
        return rows

    def get_provider(self, name: str) -> BaseProvider:
        return self.providers[name]

    def _effective_order(self, preferred_order: list[str] | None = None) -> list[str]:
        if preferred_order:
            return preferred_order
        configured = self.settings.get("provider_fallback_order", ["ollama", "rules"])
        if self.settings.get("local_only_mode", True):
            return [name for name in configured if name in {"ollama", "rules"}] or ["rules"]
        return configured

    def _enabled(self, provider_name: str) -> bool:
        if not self.catalog:
            return True
        for profile in self.catalog.load():
            if profile.get("name") == provider_name:
                return bool(profile.get("enabled", False))
        return True

    def generate(self, task: str, prompt: str, preferred_order: list[str] | None = None, model: str = "") -> ProviderResult:
        order = self._effective_order(preferred_order)
        max_failures = int(self.settings.get("max_provider_failures_before_fallback", 2))
        last_error = ""
        for idx, provider_name in enumerate(order):
            provider = self.providers.get(provider_name)
            if provider is None:
                continue
            if not self._enabled(provider_name):
                last_error = f"Provider {provider_name} is disabled."
                self.usage.record(provider_name, model or "", task, False, last_error)
                continue
            available, message = provider.is_available()
            if not available:
                last_error = message
                self.usage.record(provider_name, model or "", task, False, message)
                continue
            result = provider.generate(prompt, model=model)
            self.usage.record(provider_name, result.model, task, result.success, result.error)
            if result.success:
                if idx > 0:
                    self.usage.mark_fallback()
                return result
            self.failures[provider_name] = self.failures.get(provider_name, 0) + 1
            last_error = result.error
            if self.failures[provider_name] >= max_failures:
                self.usage.mark_fallback()
                continue
        return ProviderResult(provider_name="none", model=model, text="", success=False, error=last_error or "No provider succeeded.")

    def provider_usage_rows(self) -> list[dict[str, Any]]:
        return self.usage.summary()
