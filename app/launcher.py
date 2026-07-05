from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from the_prof.agents.registry import AgentRegistry
from the_prof.apis.api_registry import APIRegistry
from the_prof.apis.api_tester import APITester
from the_prof.core.secrets_store import SecretsStore
from the_prof.core.state_store import StateStore
from the_prof.core.workflow_engine import WorkflowEngine
from the_prof.providers.provider_catalog import ProviderCatalog


class AppContext:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.state_store = StateStore(root)
        default_settings_path = root / "the_prof" / "app" / "config" / "default_settings.json"
        default_settings = json.loads(default_settings_path.read_text(encoding="utf-8"))
        self.settings = self.state_store.load_settings(default_settings)
        self.secrets_store = SecretsStore(root)
        self._load_secrets_into_environment()
        self.provider_catalog = ProviderCatalog(
            root / "the_prof" / "app" / "config" / "default_providers.json",
            root / "storage" / "local_db" / "provider_profiles.json",
        )
        self.agent_registry = AgentRegistry(root / "the_prof" / "agents" / "skills")
        self.api_registry = APIRegistry(root / "the_prof" / "apis" / "imported_sources", root / "storage" / "local_db" / "api_registry.json")
        self.api_registry.normalize()
        self.api_tester = APITester(self.api_registry)
        self.workflow_engine = WorkflowEngine(root, self.settings, self.agent_registry, self.api_registry, self.provider_catalog)

    def _load_secrets_into_environment(self) -> None:
        for name in [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GOOGLE_API_KEY",
            "OPENROUTER_API_KEY",
            "GROQ_API_KEY",
            "KIMI_API_KEY",
            "GLM_API_KEY",
            "MISTRAL_API_KEY",
            "CEREBRAS_API_KEY",
            "HUGGINGFACE_API_KEY",
            "SAMBANOVA_API_KEY",
            "CLOUDFLARE_API_TOKEN",
        ]:
            value = self.secrets_store.get_secret(name)
            if value:
                os.environ[name] = value

    def save_settings(self, settings: dict[str, Any]) -> None:
        self.settings = settings
        self.state_store.save_settings(settings)
        self.workflow_engine = WorkflowEngine(self.root, self.settings, self.agent_registry, self.api_registry, self.provider_catalog)
