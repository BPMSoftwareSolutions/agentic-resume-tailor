#!/usr/bin/env python3
"""
Unit tests for LLM Provider abstraction layer.
Related to GitHub Issue #30 - Claude 4.x Model Support

Tests:
- LLM provider abstraction interface
- OpenAI provider implementation
- Claude provider implementation
- Model registry functionality
- Token counting for both providers
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from src.agent.llm_provider import LLMProvider, OpenAIProvider, ClaudeProvider
from src.agent.model_registry import (
    get_model_info, 
    get_all_models, 
    get_providers,
    get_default_model,
    get_model_limit,
    estimate_cost,
    format_model_info
)


class TestModelRegistry:
    """Test model registry functionality."""
    
    def test_get_providers(self):
        """Test getting list of providers."""
        providers = get_providers()
        assert 'openai' in providers
        assert 'claude' in providers
        assert len(providers) >= 2
    
    def test_get_default_model_openai(self):
        """Test getting default OpenAI model."""
        model = get_default_model('openai')
        assert model == 'gpt-4'
    
    def test_get_default_model_claude(self):
        """Test getting default Claude model."""
        model = get_default_model('claude')
        assert model == 'claude-3-5-sonnet-20241022'
    
    def test_get_model_info_openai(self):
        """Test getting OpenAI model info."""
        info = get_model_info('openai', 'gpt-4')
        assert info is not None
        assert info['name'] == 'GPT-4'
        assert info['context_window'] == 8192
        assert info['provider'] == 'openai'
        assert 'cost_per_1k_input' in info
        assert 'cost_per_1k_output' in info
    
    def test_get_model_info_claude(self):
        """Test getting Claude model info."""
        info = get_model_info('claude', 'claude-3-5-sonnet-20241022')
        assert info is not None
        assert info['name'] == 'Claude 3.5 Sonnet'
        assert info['context_window'] == 200000
        assert info['provider'] == 'claude'
        assert 'cost_per_1k_input' in info
        assert 'cost_per_1k_output' in info
    
    def test_get_model_info_invalid(self):
        """Test getting info for invalid model."""
        info = get_model_info('invalid', 'invalid-model')
        assert info is None
    
    def test_get_all_models(self):
        """Test getting all models."""
        all_models = get_all_models()
        assert 'openai' in all_models
        assert 'claude' in all_models
        assert 'gpt-4' in all_models['openai']
        assert 'claude-3-5-sonnet-20241022' in all_models['claude']
    
    def test_get_all_models_filtered(self):
        """Test getting models filtered by provider."""
        openai_models = get_all_models('openai')
        assert 'gpt-4' in openai_models
        assert 'claude-3-5-sonnet-20241022' not in openai_models
        
        claude_models = get_all_models('claude')
        assert 'claude-3-5-sonnet-20241022' in claude_models
        assert 'gpt-4' not in claude_models
    
    def test_get_model_limit_openai(self):
        """Test getting token limit for OpenAI model."""
        limit = get_model_limit('openai', 'gpt-4')
        assert limit == 8192
        
        limit = get_model_limit('openai', 'gpt-4-turbo')
        assert limit == 128000
    
    def test_get_model_limit_claude(self):
        """Test getting token limit for Claude model."""
        limit = get_model_limit('claude', 'claude-3-5-sonnet-20241022')
        assert limit == 200000
    
    def test_estimate_cost(self):
        """Test cost estimation."""
        # Test OpenAI GPT-4 cost
        cost = estimate_cost('openai', 'gpt-4', 1000, 500)
        expected = (1000 / 1000) * 0.03 + (500 / 1000) * 0.06
        assert abs(cost - expected) < 0.001
        
        # Test Claude cost
        cost = estimate_cost('claude', 'claude-3-5-sonnet-20241022', 1000, 500)
        expected = (1000 / 1000) * 0.003 + (500 / 1000) * 0.015
        assert abs(cost - expected) < 0.001
    
    def test_format_model_info(self):
        """Test formatting model info."""
        info = format_model_info('openai', 'gpt-4')
        assert 'GPT-4' in info
        assert '8,192' in info
        assert '$0.0300' in info
        
        info = format_model_info('claude', 'claude-3-5-sonnet-20241022')
        assert 'Claude 3.5 Sonnet' in info
        assert '200,000' in info


class TestOpenAIProvider:
    """Test OpenAI provider implementation."""

    @patch('openai.OpenAI')
    def test_initialization(self, mock_openai):
        """Test OpenAI provider initialization."""
        provider = OpenAIProvider('test-api-key', 'gpt-4')
        assert provider.api_key == 'test-api-key'
        assert provider.model == 'gpt-4'
        mock_openai.assert_called_once_with(api_key='test-api-key')

    @patch('openai.OpenAI')
    def test_chat_completion(self, mock_openai):
        """Test OpenAI chat completion."""
        # Mock the OpenAI client response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        provider = OpenAIProvider('test-api-key', 'gpt-4')
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]

        response = provider.chat_completion(messages)
        assert response == "Test response"
        mock_client.chat.completions.create.assert_called_once()

    @patch('openai.OpenAI')
    def test_count_tokens_estimate(self, mock_openai):
        """Test token counting with estimation."""
        provider = OpenAIProvider('test-api-key', 'gpt-4')
        provider.tiktoken_available = False

        messages = [
            {"role": "user", "content": "Hello, how are you?"}
        ]

        tokens = provider.count_tokens(messages)
        assert tokens > 0
        assert isinstance(tokens, int)

    @patch('openai.OpenAI')
    def test_get_model_info(self, mock_openai):
        """Test getting model info."""
        provider = OpenAIProvider('test-api-key', 'gpt-4')
        info = provider.get_model_info()
        assert info['name'] == 'GPT-4'
        assert info['context_window'] == 8192
        assert info['provider'] == 'openai'


class TestClaudeProvider:
    """Test Claude provider implementation."""

    @patch('anthropic.Anthropic')
    def test_initialization(self, mock_anthropic):
        """Test Claude provider initialization."""
        provider = ClaudeProvider('test-api-key', 'claude-3-5-sonnet-20241022')
        assert provider.api_key == 'test-api-key'
        assert provider.model == 'claude-3-5-sonnet-20241022'
        mock_anthropic.assert_called_once_with(api_key='test-api-key')

    @patch('anthropic.Anthropic')
    def test_chat_completion(self, mock_anthropic):
        """Test Claude chat completion."""
        # Mock the Anthropic client response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Test response from Claude"
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        provider = ClaudeProvider('test-api-key', 'claude-3-5-sonnet-20241022')
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]

        response = provider.chat_completion(messages)
        assert response == "Test response from Claude"
        mock_client.messages.create.assert_called_once()

    @patch('anthropic.Anthropic')
    def test_chat_completion_system_message(self, mock_anthropic):
        """Test Claude chat completion with system message separation."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Response"
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        provider = ClaudeProvider('test-api-key', 'claude-3-5-sonnet-20241022')
        messages = [
            {"role": "system", "content": "System prompt"},
            {"role": "user", "content": "User message"}
        ]

        response = provider.chat_completion(messages)

        # Verify system message was passed separately
        call_args = mock_client.messages.create.call_args
        assert 'system' in call_args.kwargs
        assert call_args.kwargs['system'] == "System prompt"

        # Verify messages don't include system message
        assert len(call_args.kwargs['messages']) == 1
        assert call_args.kwargs['messages'][0]['role'] == 'user'

    @patch('anthropic.Anthropic')
    def test_count_tokens_estimate(self, mock_anthropic):
        """Test token counting with estimation."""
        # Mock the client to raise an exception for count_tokens
        mock_client = Mock()
        mock_client.count_tokens.side_effect = Exception("Not available")
        mock_anthropic.return_value = mock_client

        provider = ClaudeProvider('test-api-key', 'claude-3-5-sonnet-20241022')

        messages = [
            {"role": "user", "content": "Hello, how are you?"}
        ]

        tokens = provider.count_tokens(messages)
        assert tokens > 0
        assert isinstance(tokens, int)

    @patch('anthropic.Anthropic')
    def test_get_model_info(self, mock_anthropic):
        """Test getting model info."""
        provider = ClaudeProvider('test-api-key', 'claude-3-5-sonnet-20241022')
        info = provider.get_model_info()
        assert info['name'] == 'Claude 3.5 Sonnet'
        assert info['context_window'] == 200000
        assert info['provider'] == 'claude'


class TestProviderIntegration:
    """Integration tests for provider switching."""

    @patch('openai.OpenAI')
    @patch('anthropic.Anthropic')
    def test_provider_interface_consistency(self, mock_anthropic, mock_openai):
        """Test that both providers implement the same interface."""
        # Setup mocks
        mock_openai_client = Mock()
        mock_openai_response = Mock()
        mock_openai_response.choices = [Mock()]
        mock_openai_response.choices[0].message.content = "OpenAI response"
        mock_openai_client.chat.completions.create.return_value = mock_openai_response
        mock_openai.return_value = mock_openai_client

        mock_claude_client = Mock()
        mock_claude_response = Mock()
        mock_claude_response.content = [Mock()]
        mock_claude_response.content[0].text = "Claude response"
        mock_claude_client.messages.create.return_value = mock_claude_response
        mock_anthropic.return_value = mock_claude_client

        # Test OpenAI provider
        openai_provider = OpenAIProvider('test-key', 'gpt-4')
        messages = [{"role": "user", "content": "Test"}]

        openai_response = openai_provider.chat_completion(messages)
        openai_tokens = openai_provider.count_tokens(messages)
        openai_info = openai_provider.get_model_info()

        # Test Claude provider
        claude_provider = ClaudeProvider('test-key', 'claude-3-5-sonnet-20241022')

        claude_response = claude_provider.chat_completion(messages)
        claude_tokens = claude_provider.count_tokens(messages)
        claude_info = claude_provider.get_model_info()

        # Verify both providers return expected types
        assert isinstance(openai_response, str)
        assert isinstance(claude_response, str)
        assert isinstance(openai_tokens, int)
        assert isinstance(claude_tokens, int)
        assert isinstance(openai_info, dict)
        assert isinstance(claude_info, dict)

