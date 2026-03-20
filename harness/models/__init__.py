from .base import ModelAdapter, ModelResponse

# Map model name -> (module path, class name) — loaded lazily so missing SDKs
# only fail when that specific model is actually used.
_REGISTRY: dict[str, tuple[str, str]] = {
    # Anthropic Claude
    "claude-opus-4-6":    ("harness.models.claude",      "ClaudeAdapter"),
    "claude-sonnet-4-6":  ("harness.models.claude",      "ClaudeAdapter"),
    "claude-haiku-4-5":   ("harness.models.claude",      "ClaudeAdapter"),
    # OpenAI
    "gpt-4o":             ("harness.models.openai",      "OpenAIAdapter"),
    "gpt-4o-mini":        ("harness.models.openai",      "OpenAIAdapter"),
    "o3":                 ("harness.models.openai",      "OpenAIAdapter"),
    # Google Gemini
    "gemini-2.5-pro":     ("harness.models.gemini",      "GeminiAdapter"),
    "gemini-2.5-flash":   ("harness.models.gemini",      "GeminiAdapter"),
    "gemini-1.5-pro":     ("harness.models.gemini",      "GeminiAdapter"),
    # Open-source (HuggingFace Inference API)
    "biomed-llm":         ("harness.models.huggingface", "HuggingFaceAdapter"),
    "biomistral-7b":      ("harness.models.huggingface", "HuggingFaceAdapter"),
}


def get_adapter(model_name: str) -> ModelAdapter:
    key = model_name.lower()
    if key not in _REGISTRY:
        raise ValueError(
            f"Unknown model '{model_name}'. Available: {sorted(_REGISTRY)}"
        )
    module_path, class_name = _REGISTRY[key]
    import importlib
    module = importlib.import_module(module_path)
    cls = getattr(module, class_name)
    return cls(model_name)
