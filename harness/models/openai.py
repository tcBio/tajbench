"""OpenAI adapter."""

from __future__ import annotations

import os
import time

import openai

from .base import ModelAdapter, ModelResponse


class OpenAIAdapter(ModelAdapter):
    def __init__(self, model_name: str) -> None:
        super().__init__(model_name)
        self._client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY") or os.environ["openai_api"])

    # OpenAI reasoning models (o1, o3, etc.) use max_completion_tokens
    _REASONING_PREFIXES = ("o1", "o3")

    def complete(self, system: str, user: str, item_id: str) -> ModelResponse:
        is_reasoning = any(self.model_name.startswith(p) for p in self._REASONING_PREFIXES)
        t0 = time.monotonic()
        kwargs: dict = dict(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        if is_reasoning:
            kwargs["max_completion_tokens"] = 4096
        else:
            kwargs["max_tokens"] = 1024
        resp = self._client.chat.completions.create(**kwargs)
        latency_ms = (time.monotonic() - t0) * 1000
        choice = resp.choices[0]
        return ModelResponse(
            model=self.model_name,
            item_id=item_id,
            response_text=choice.message.content or "",
            latency_ms=latency_ms,
            input_tokens=resp.usage.prompt_tokens,
            output_tokens=resp.usage.completion_tokens,
            raw=resp.model_dump(),
        )
