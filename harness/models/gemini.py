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
        self._model = genai.GenerativeModel(model_name)

    def complete(self, system: str, user: str, item_id: str) -> ModelResponse:
        full_prompt = f"{system}\n\n{user}"
        t0 = time.monotonic()
        resp = self._model.generate_content(full_prompt)
        latency_ms = (time.monotonic() - t0) * 1000
        return ModelResponse(
            model=self.model_name,
            item_id=item_id,
            response_text=resp.text,
            latency_ms=latency_ms,
            raw={"candidates": [str(c) for c in resp.candidates]},
        )
