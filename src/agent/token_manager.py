#!/usr/bin/env python3
"""
Token Manager - Intelligent token counting and memory management.
Related to GitHub Issue #24 - Phase 1: Auto-Verification & Result Analysis
Updated for GitHub Issue #30 - Multi-provider support

This module provides:
- Accurate token counting for OpenAI and Claude models
- Warning at 80% token capacity
- Critical alert at 95% token capacity
- Memory optimization suggestions
- Token usage statistics
"""

import json
from typing import Any, Dict, List, Optional


class TokenManager:
    """Manages token counting and provides memory usage warnings."""

    # Model token limits (conservative estimates)
    MODEL_LIMITS = {
        # OpenAI models
        "gpt-4": 8192,
        "gpt-4-turbo": 128000,
        "gpt-4-turbo-preview": 128000,
        "gpt-4-32k": 32768,
        "gpt-3.5-turbo": 4096,
        "gpt-3.5-turbo-16k": 16384,
        # Claude models
        "claude-3-5-sonnet-20241022": 200000,
        "claude-3-5-haiku-20241022": 200000,
        "claude-3-opus-20240229": 200000,
        "claude-3-sonnet-20240229": 200000,
        "claude-3-haiku-20240307": 200000,
    }

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4",
        max_tokens: Optional[int] = None,
    ):
        """
        Initialize the token manager.

        Args:
            provider: LLM provider ('openai' or 'claude')
            model: Model name
            max_tokens: Maximum token limit (if None, uses model default)
        """
        self.provider = provider
        self.model = model
        self.max_tokens = max_tokens or self._get_model_limit(model)
        self.warning_threshold = 0.80  # Warn at 80%
        self.critical_threshold = 0.95  # Critical at 95%

        # Try to import tiktoken for accurate counting (OpenAI models)
        self.tiktoken_available = False
        self.encoding = None
        if provider == "openai":
            try:
                import tiktoken

                self.encoding = tiktoken.encoding_for_model(model)
                self.tiktoken_available = True
            except ImportError:
                # Fall back to estimation if tiktoken not available
                pass
            except KeyError:
                # Model not found in tiktoken, use cl100k_base as default
                try:
                    import tiktoken

                    self.encoding = tiktoken.get_encoding("cl100k_base")
                    self.tiktoken_available = True
                except:
                    pass

    def _get_model_limit(self, model: str) -> int:
        """
        Get token limit for a model.

        Args:
            model: Model name

        Returns:
            Token limit
        """
        # Check exact match
        if model in self.MODEL_LIMITS:
            return self.MODEL_LIMITS[model]

        # Check partial matches
        for key, limit in self.MODEL_LIMITS.items():
            if key in model:
                return limit

        # Default to gpt-4 limit
        return self.MODEL_LIMITS["gpt-4"]

    def count_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Count total tokens in message list.

        Args:
            messages: List of message dictionaries with 'role' and 'content'

        Returns:
            Total token count
        """
        if self.tiktoken_available and self.encoding:
            return self._count_tokens_accurate(messages)
        else:
            return self._count_tokens_estimate(messages)

    def _count_tokens_accurate(self, messages: List[Dict[str, str]]) -> int:
        """
        Count tokens accurately using tiktoken.

        Args:
            messages: List of message dictionaries

        Returns:
            Accurate token count
        """
        total = 0

        for message in messages:
            # Count tokens for role
            role = message.get("role", "")
            total += len(self.encoding.encode(role))

            # Count tokens for content
            content = message.get("content", "")
            total += len(self.encoding.encode(content))

            # Add message overhead (4 tokens per message)
            total += 4

        # Add conversation overhead
        total += 2

        return total

    def _count_tokens_estimate(self, messages: List[Dict[str, str]]) -> int:
        """
        Estimate token count when tiktoken is not available.
        Uses rough approximation: 1 token ≈ 4 characters.

        Args:
            messages: List of message dictionaries

        Returns:
            Estimated token count
        """
        total_chars = 0

        for message in messages:
            role = message.get("role", "")
            content = message.get("content", "")
            total_chars += len(role) + len(content)

        # Rough estimate: 1 token ≈ 4 characters
        # Add 10% overhead for message formatting
        estimated_tokens = int((total_chars / 4) * 1.1)

        return estimated_tokens

    def check_limit(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Check if messages are approaching token limit.

        Args:
            messages: List of message dictionaries

        Returns:
            Dictionary with:
                - token_count: current token count
                - max_tokens: maximum allowed tokens
                - percentage: usage percentage (0-100)
                - warning: bool, True if at warning threshold
                - critical: bool, True if at critical threshold
                - message: warning message if applicable
        """
        token_count = self.count_tokens(messages)
        percentage = (token_count / self.max_tokens) * 100

        warning = percentage >= (self.warning_threshold * 100)
        critical = percentage >= (self.critical_threshold * 100)

        message = None
        if critical:
            message = self._format_critical_warning(token_count, percentage)
        elif warning:
            message = self._format_warning(token_count, percentage)

        return {
            "token_count": token_count,
            "max_tokens": self.max_tokens,
            "percentage": round(percentage, 1),
            "warning": warning,
            "critical": critical,
            "message": message,
            "estimation_method": "accurate" if self.tiktoken_available else "estimated",
        }

    def _format_warning(self, token_count: int, percentage: float) -> str:
        """
        Format warning message for 80% threshold.

        Args:
            token_count: Current token count
            percentage: Usage percentage

        Returns:
            Formatted warning message
        """
        return f"""⚠️  WARNING: Memory at {percentage:.1f}% capacity ({token_count}/{self.max_tokens} tokens).
Consider clearing memory if conversation continues.

Suggestions:
  • Clear old conversation history: Use 'clear memory' command
  • Start a new conversation session
  • Export important information before clearing"""

    def _format_critical_warning(self, token_count: int, percentage: float) -> str:
        """
        Format critical warning message for 95% threshold.

        Args:
            token_count: Current token count
            percentage: Usage percentage

        Returns:
            Formatted critical warning message
        """
        return f"""🚨 CRITICAL: Memory at {percentage:.1f}% capacity ({token_count}/{self.max_tokens} tokens).
You are very close to the limit!

IMMEDIATE ACTION REQUIRED:
  • Clear memory now: Use 'clear memory' command
  • Start a new conversation session
  • The next message may fail due to token limit"""

    def get_stats(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Get detailed token usage statistics.

        Args:
            messages: List of message dictionaries

        Returns:
            Dictionary with detailed statistics
        """
        limit_check = self.check_limit(messages)

        # Count messages by role
        role_counts = {}
        role_tokens = {}

        for message in messages:
            role = message.get("role", "unknown")
            role_counts[role] = role_counts.get(role, 0) + 1

            # Count tokens for this message
            if self.tiktoken_available and self.encoding:
                msg_tokens = len(self.encoding.encode(message.get("content", "")))
            else:
                msg_tokens = len(message.get("content", "")) // 4

            role_tokens[role] = role_tokens.get(role, 0) + msg_tokens

        return {
            "total_tokens": limit_check["token_count"],
            "max_tokens": self.max_tokens,
            "percentage": limit_check["percentage"],
            "warning": limit_check["warning"],
            "critical": limit_check["critical"],
            "message_count": len(messages),
            "role_counts": role_counts,
            "role_tokens": role_tokens,
            "estimation_method": limit_check["estimation_method"],
            "model": self.model,
        }

    def suggest_optimization(self, messages: List[Dict[str, str]]) -> List[str]:
        """
        Suggest memory optimization strategies.

        Args:
            messages: List of message dictionaries

        Returns:
            List of optimization suggestions
        """
        stats = self.get_stats(messages)
        suggestions = []

        if stats["percentage"] > 80:
            suggestions.append("Clear old conversation history to free up memory")

        if stats["message_count"] > 50:
            suggestions.append(
                f"You have {stats['message_count']} messages. Consider starting a new session"
            )

        # Check for large system messages
        system_tokens = stats["role_tokens"].get("system", 0)
        if system_tokens > 2000:
            suggestions.append("System prompt is large. Consider optimizing it")

        # Check for command output accumulation
        assistant_tokens = stats["role_tokens"].get("assistant", 0)
        if assistant_tokens > stats["total_tokens"] * 0.6:
            suggestions.append(
                "Command outputs are accumulating. Consider clearing old results"
            )

        if not suggestions:
            suggestions.append("Memory usage is healthy. No optimization needed")

        return suggestions
