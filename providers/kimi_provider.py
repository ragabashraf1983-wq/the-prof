from __future__ import annotations

from .openai_provider import OpenAICompatibleProvider


class KimiProvider(OpenAICompatibleProvider):
    def __init__(self) -> None:
        super().__init__(
            name="kimi",
            base_url="https://api.moonshot.cn/v1",
            api_key_env="KIMI_API_KEY",
            default_model="moonshot-v1-8k",
        )
