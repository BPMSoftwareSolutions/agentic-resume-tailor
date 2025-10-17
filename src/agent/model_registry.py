#!/usr/bin/env python3
"""
Model Registry - Centralized model configuration and metadata.
Related to GitHub Issue #30 - Claude 4.x Model Support

This module provides:
- Model metadata for all supported providers
- Token limits and pricing information
- Model capabilities and context windows
"""

from typing import Any, Dict, List, Optional

# Model registry with metadata for all supported models
MODEL_REGISTRY: Dict[str, Dict[str, Dict[str, Any]]] = {
    "openai": {
        "gpt-4": {
            "name": "GPT-4",
            "context_window": 8192,
            "cost_per_1k_input": 0.03,
            "cost_per_1k_output": 0.06,
            "provider": "openai",
            "description": "Most capable GPT-4 model for complex tasks",
            "max_output_tokens": 4096,
        },
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "context_window": 128000,
            "cost_per_1k_input": 0.01,
            "cost_per_1k_output": 0.03,
            "provider": "openai",
            "description": "Faster and cheaper GPT-4 with larger context",
            "max_output_tokens": 4096,
        },
        "gpt-4-turbo-preview": {
            "name": "GPT-4 Turbo Preview",
            "context_window": 128000,
            "cost_per_1k_input": 0.01,
            "cost_per_1k_output": 0.03,
            "provider": "openai",
            "description": "Preview version of GPT-4 Turbo",
            "max_output_tokens": 4096,
        },
        "gpt-4-32k": {
            "name": "GPT-4 32K",
            "context_window": 32768,
            "cost_per_1k_input": 0.06,
            "cost_per_1k_output": 0.12,
            "provider": "openai",
            "description": "GPT-4 with extended 32K context window",
            "max_output_tokens": 4096,
        },
        "gpt-3.5-turbo": {
            "name": "GPT-3.5 Turbo",
            "context_window": 4096,
            "cost_per_1k_input": 0.0015,
            "cost_per_1k_output": 0.002,
            "provider": "openai",
            "description": "Fast and efficient model for simpler tasks",
            "max_output_tokens": 4096,
        },
        "gpt-3.5-turbo-16k": {
            "name": "GPT-3.5 Turbo 16K",
            "context_window": 16384,
            "cost_per_1k_input": 0.003,
            "cost_per_1k_output": 0.004,
            "provider": "openai",
            "description": "GPT-3.5 with extended context window",
            "max_output_tokens": 4096,
        },
    },
    "claude": {
        # Current Claude 4.x models (preferred)
        "claude-haiku-4-5-20251001": {
            "name": "Claude Haiku 4.5",
            "context_window": 200000,
            "cost_per_1k_input": 0.002,
            "cost_per_1k_output": 0.008,
            "provider": "claude",
            "description": "Claude 4.5 Haiku - fast and efficient",
            "max_output_tokens": 8192,
        },
        "claude-sonnet-4-5-20250929": {
            "name": "Claude Sonnet 4.5",
            "context_window": 200000,
            "cost_per_1k_input": 0.004,
            "cost_per_1k_output": 0.016,
            "provider": "claude",
            "description": "Claude 4.5 Sonnet - balanced capability",
            "max_output_tokens": 8192,
        },
        "claude-opus-4-1-20250805": {
            "name": "Claude Opus 4.1",
            "context_window": 200000,
            "cost_per_1k_input": 0.01,
            "cost_per_1k_output": 0.04,
            "provider": "claude",
            "description": "Claude 4.1 Opus - highest capability",
            "max_output_tokens": 8192,
        },
        # Keep 3.x entries for backward compatibility but mark as deprecated in code paths
        "claude-3-5-sonnet-20241022": {
            "name": "Claude 3.5 Sonnet",
            "context_window": 200000,
            "cost_per_1k_input": 0.003,
            "cost_per_1k_output": 0.015,
            "provider": "claude",
            "description": "Claude 3.5 Sonnet (deprecated)",
            "max_output_tokens": 8192,
        },
        "claude-3-5-haiku-20241022": {
            "name": "Claude 3.5 Haiku",
            "context_window": 200000,
            "cost_per_1k_input": 0.001,
            "cost_per_1k_output": 0.005,
            "provider": "claude",
            "description": "Claude 3.5 Haiku (deprecated)",
            "max_output_tokens": 8192,
        },
        "claude-3-opus-20240229": {
            "name": "Claude 3 Opus",
            "context_window": 200000,
            "cost_per_1k_input": 0.015,
            "cost_per_1k_output": 0.075,
            "provider": "claude",
            "description": "Claude 3 Opus (deprecated)",
            "max_output_tokens": 4096,
        },
        "claude-3-sonnet-20240229": {
            "name": "Claude 3 Sonnet",
            "context_window": 200000,
            "cost_per_1k_input": 0.003,
            "cost_per_1k_output": 0.015,
            "provider": "claude",
            "description": "Claude 3 Sonnet (deprecated)",
            "max_output_tokens": 4096,
        },
        "claude-3-haiku-20240307": {
            "name": "Claude 3 Haiku",
            "context_window": 200000,
            "cost_per_1k_input": 0.00025,
            "cost_per_1k_output": 0.00125,
            "provider": "claude",
            "description": "Claude 3 Haiku (deprecated)",
            "max_output_tokens": 4096,
        },
    },
}


def get_model_info(provider: str, model: str) -> Optional[Dict[str, Any]]:
    """
    Get model information from registry.

    Args:
        provider: Provider name ('openai' or 'claude')
        model: Model name

    Returns:
        Model information dictionary or None if not found
    """
    if provider in MODEL_REGISTRY and model in MODEL_REGISTRY[provider]:
        return MODEL_REGISTRY[provider][model]
    return None


def get_all_models(provider: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """
    Get all models, optionally filtered by provider.

    Args:
        provider: Optional provider name to filter by

    Returns:
        Dictionary of models
    """
    if provider:
        return MODEL_REGISTRY.get(provider, {})
    return MODEL_REGISTRY


def get_providers() -> List[str]:
    """
    Get list of all supported providers.

    Returns:
        List of provider names
    """
    return list(MODEL_REGISTRY.keys())


def get_default_model(provider: str) -> Optional[str]:
    """
    Get default model for a provider.

    Args:
        provider: Provider name

    Returns:
        Default model name or None
    """
    defaults = {"openai": "gpt-4", "claude": "claude-sonnet-4-5-20250929"}
    return defaults.get(provider)


def get_model_limit(provider: str, model: str) -> int:
    """
    Get token limit for a model.

    Args:
        provider: Provider name
        model: Model name

    Returns:
        Token limit (context window size)
    """
    info = get_model_info(provider, model)
    if info:
        return info.get("context_window", 8192)

    # Default limits by provider
    if provider == "claude":
        return 200000
    else:  # openai
        return 8192


def estimate_cost(
    provider: str, model: str, input_tokens: int, output_tokens: int
) -> float:
    """
    Estimate cost for a request.

    Args:
        provider: Provider name
        model: Model name
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Estimated cost in USD
    """
    info = get_model_info(provider, model)
    if not info:
        return 0.0

    input_cost = (input_tokens / 1000) * info.get("cost_per_1k_input", 0)
    output_cost = (output_tokens / 1000) * info.get("cost_per_1k_output", 0)

    return input_cost + output_cost


def format_model_info(provider: str, model: str) -> str:
    """
    Format model information as a human-readable string.

    Args:
        provider: Provider name
        model: Model name

    Returns:
        Formatted model information
    """
    info = get_model_info(provider, model)
    if not info:
        return f"Unknown model: {provider}:{model}"

    return (
        f"{info['name']} - "
        f"{info['context_window']:,} token context, "
        f"${info['cost_per_1k_input']:.4f}/1K input, "
        f"${info['cost_per_1k_output']:.4f}/1K output"
    )
