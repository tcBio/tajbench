"""Anthropic Claude adapter."""

from __future__ import annotations

import os
import time

import anthropic

from .base import ModelAdapter, ModelResponse


class ClaudeAdapter(ModelAdapter):
    def __init__(self, model_name: str) -> None:
        super().__init__(model_name)
        self._client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def complete(self, system: str, user: str, item_id: str) -> ModelResponse:
        t0 = time.monotonic()
        msg = self._client.messages.create(
            model=self.model_name,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        latency_ms = (time.monotonic() - t0) * 1000
        return ModelResponse(
            model=self.model_name,
            item_id=item_id,
            response_text=msg.content[0].text,
            latency_ms=latency_ms,
            input_tokens=msg.usage.input_tokens,
            output_tokens=msg.usage.output_tokens,
            raw=msg.model_dump(),
        )
