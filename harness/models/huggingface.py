"""HuggingFace Inference API adapter for open-source bio models."""

from __future__ import annotations

import os
import time

import requests

from .base import ModelAdapter, ModelResponse

# Map friendly names to HuggingFace model IDs
HF_MODEL_IDS: dict[str, str] = {
    "biomed-llm": "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext",
    "biomistral-7b": "BioMistral/BioMistral-7B",
}

HF_API_BASE = "https://api-inference.huggingface.co/models"


class HuggingFaceAdapter(ModelAdapter):
    def __init__(self, model_name: str) -> None:
        super().__init__(model_name)
        self._hf_id = HF_MODEL_IDS.get(model_name.lower(), model_name)
        self._token = os.environ["HF_TOKEN"]
        self._url = f"{HF_API_BASE}/{self._hf_id}"

    def complete(self, system: str, user: str, item_id: str) -> ModelResponse:
        payload = {"inputs": f"{system}\n\n{user}", "parameters": {"max_new_tokens": 512}}
        headers = {"Authorization": f"Bearer {self._token}"}
        t0 = time.monotonic()
        resp = requests.post(self._url, json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        latency_ms = (time.monotonic() - t0) * 1000
        data = resp.json()
        # HF text-generation returns list of {"generated_text": "..."}
        text = data[0].get("generated_text", "") if isinstance(data, list) else str(data)
        return ModelResponse(
            model=self.model_name,
            item_id=item_id,
            response_text=text,
            latency_ms=latency_ms,
            raw=data if isinstance(data, dict) else {"result": data},
        )
