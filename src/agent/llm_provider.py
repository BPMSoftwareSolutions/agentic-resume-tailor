#!/usr/bin/env python3
"""
LLM Provider Abstraction Layer - Multi-provider support for AI models.
Related to GitHub Issue #30 - Claude 4.x Model Support

This module provides:
- Abstract base class for LLM providers
- OpenAI provider implementation
- Anthropic Claude provider implementation
- Unified interface for chat completions and token counting
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, api_key: str, model: str):
        """
        Initialize the LLM provider.
        
        Args:
            api_key: API key for the provider
            model: Model name to use
        """
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate chat completion.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated response text
        """
        pass
    
    @abstractmethod
    def count_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Count tokens in messages.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Total token count
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model metadata (limits, pricing, etc.).
        
        Returns:
            Dictionary with model information
        """
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI implementation of LLM provider."""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key
            model: OpenAI model name
        """
        super().__init__(api_key, model)
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. "
                "Install it with: pip install openai"
            )
        
        # Try to import tiktoken for accurate token counting
        self.tiktoken_available = False
        self.encoding = None
        try:
            import tiktoken
            self.encoding = tiktoken.encoding_for_model(model)
            self.tiktoken_available = True
        except ImportError:
            pass
        except KeyError:
            # Model not found in tiktoken, use cl100k_base as default
            try:
                import tiktoken
                self.encoding = tiktoken.get_encoding("cl100k_base")
                self.tiktoken_available = True
            except:
                pass
    
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate chat completion using OpenAI.
        
        Args:
            messages: List of message dictionaries
            **kwargs: Additional OpenAI parameters (temperature, max_tokens, etc.)
            
        Returns:
            Generated response text
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    def count_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Count tokens in messages using tiktoken.
        
        Args:
            messages: List of message dictionaries
            
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
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get OpenAI model metadata.
        
        Returns:
            Dictionary with model information
        """
        from .model_registry import MODEL_REGISTRY
        
        if 'openai' in MODEL_REGISTRY and self.model in MODEL_REGISTRY['openai']:
            return MODEL_REGISTRY['openai'][self.model]
        
        # Return default info if model not in registry
        return {
            'name': self.model,
            'context_window': 8192,
            'provider': 'openai'
        }


class ClaudeProvider(LLMProvider):
    """Anthropic Claude implementation of LLM provider."""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize Claude provider.
        
        Args:
            api_key: Anthropic API key
            model: Claude model name
        """
        super().__init__(api_key, model)
        
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError(
                "Anthropic package not installed. "
                "Install it with: pip install anthropic"
            )
    
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate chat completion using Claude.
        
        Args:
            messages: List of message dictionaries
            **kwargs: Additional Claude parameters (temperature, max_tokens, etc.)
            
        Returns:
            Generated response text
        """
        # Claude API requires system message to be separate
        system_message = None
        claude_messages = []
        
        for msg in messages:
            if msg['role'] == 'system':
                system_message = msg['content']
            else:
                claude_messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        # Set default max_tokens if not provided
        if 'max_tokens' not in kwargs:
            kwargs['max_tokens'] = 4096
        
        # Create message with Claude API
        request_params = {
            'model': self.model,
            'messages': claude_messages,
            **kwargs
        }
        
        if system_message:
            request_params['system'] = system_message
        
        response = self.client.messages.create(**request_params)
        
        return response.content[0].text
    
    def count_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Count tokens in messages using Claude's token counting.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Total token count
        """
        try:
            # Use Claude's built-in token counting if available
            total = 0
            for message in messages:
                content = message.get("content", "")
                # Use Anthropic's count_tokens method
                total += self.client.count_tokens(content)
            return total
        except:
            # Fall back to estimation
            return self._count_tokens_estimate(messages)
    
    def _count_tokens_estimate(self, messages: List[Dict[str, str]]) -> int:
        """
        Estimate token count for Claude.
        Claude uses similar tokenization to GPT models.
        
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
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get Claude model metadata.
        
        Returns:
            Dictionary with model information
        """
        from .model_registry import MODEL_REGISTRY
        
        if 'claude' in MODEL_REGISTRY and self.model in MODEL_REGISTRY['claude']:
            return MODEL_REGISTRY['claude'][self.model]
        
        # Return default info if model not in registry
        return {
            'name': self.model,
            'context_window': 200000,
            'provider': 'claude'
        }

