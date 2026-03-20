"""Abstract base for all model adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModelResponse:
    model: str
    item_id: str
    response_text: str
    latency_ms: float
    input_tokens: int = 0
    output_tokens: int = 0
    raw: dict = field(default_factory=dict)  # full API response for debugging


class ModelAdapter(ABC):
    """Wraps a single model API and returns ModelResponse objects."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    @abstractmethod
    def complete(self, system: str, user: str, item_id: str) -> ModelResponse:
        """Call the model with a system+user prompt, return ModelResponse."""
        ...

    def build_prompt(self, prompt: str, context: str) -> tuple[str, str]:
        """Split item fields into (system, user) strings."""
        system = (
            "You are an expert population geneticist and bioinformatician. "
            "Answer the following question about genomic data precisely and concisely. "
            "Do not add caveats or hedging beyond what the data supports."
        )
        user = f"{prompt}\n\n--- DATA ---\n{context}"
        return system, user
