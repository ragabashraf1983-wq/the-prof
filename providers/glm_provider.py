from __future__ import annotations

from .openai_provider import OpenAICompatibleProvider


class GLMProvider(OpenAICompatibleProvider):
    def __init__(self) -> None:
        super().__init__(
            name="glm",
            base_url="https://open.bigmodel.cn/api/paas/v4",
            api_key_env="GLM_API_KEY",
            default_model="glm-4-flash",
        )
