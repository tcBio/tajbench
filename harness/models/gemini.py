"""Google Gemini adapter via the google-generativeai SDK."""

from __future__ import annotations

import os
import time

import google.generativeai as genai

from .base import ModelAdapter, ModelResponse


class GeminiAdapter(ModelAdapter):
    def __init__(self, model_name: str) -> None:
        super().__init__(model_name)
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self._system: str | None = None

    def complete(self, system: str, user: str, item_id: str) -> ModelResponse:
        # Re-create model only if system prompt changes (avoids per-call overhead)
        if system != self._system:
            self._system = system
            self._model = genai.GenerativeModel(
                self.model_name, system_instruction=system
            )
        t0 = time.monotonic()
        resp = self._model.generate_content(user)
        latency_ms = (time.monotonic() - t0) * 1000
        usage = getattr(resp, "usage_metadata", None)
        return ModelResponse(
            model=self.model_name,
            item_id=item_id,
            response_text=resp.text,
            latency_ms=latency_ms,
            input_tokens=getattr(usage, "prompt_token_count", 0) if usage else 0,
            output_tokens=getattr(usage, "candidates_token_count", 0) if usage else 0,
            raw={"candidates": [str(c) for c in resp.candidates]},
        )
