"""
Unit tests for the local AI agent.
Related to GitHub Issue #8
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent import Agent, CommandExecutor, MemoryManager


class TestMemoryManager:
    """Test cases for MemoryManager class."""

    def test_memory_manager_init(self, tmp_path):
        """Test MemoryManager initialization."""
        memory_file = tmp_path / "memory.json"
        manager = MemoryManager(str(memory_file))

        assert manager.memory_file == str(memory_file)
        assert manager.memory == []

    def test_load_memory_empty_file(self, tmp_path):
        """Test loading memory from non-existent file."""
        memory_file = tmp_path / "memory.json"
        manager = MemoryManager(str(memory_file))
        manager.load()

        assert manager.memory == []

    def test_load_memory_existing_file(self, tmp_path):
        """Test loading memory from existing file."""
        memory_file = tmp_path / "memory.json"
        test_memory = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]

        with open(memory_file, "w") as f:
            json.dump(test_memory, f)

        manager = MemoryManager(str(memory_file))
        manager.load()

        assert manager.memory == test_memory

    def test_save_memory(self, tmp_path):
        """Test saving memory to file."""
        memory_file = tmp_path / "memory.json"
        manager = MemoryManager(str(memory_file))

        test_memory = [{"role": "user", "content": "Test message"}]
        manager.memory = test_memory
        manager.save()

        with open(memory_file, "r") as f:
            saved_memory = json.load(f)

        assert saved_memory == test_memory

    def test_add_message(self, tmp_path):
        """Test adding a message to memory."""
        memory_file = tmp_path / "memory.json"
        manager = MemoryManager(str(memory_file))

        manager.add_message("user", "Hello")
        manager.add_message("assistant", "Hi!")

        assert len(manager.memory) == 2
        assert manager.memory[0] == {"role": "user", "content": "Hello"}
        assert manager.memory[1] == {"role": "assistant", "content": "Hi!"}

    def test_get_messages(self, tmp_path):
        """Test getting messages from memory."""
        memory_file = tmp_path / "memory.json"
        manager = MemoryManager(str(memory_file))

        manager.add_message("user", "Test")
        messages = manager.get_messages()

        assert messages == [{"role": "user", "content": "Test"}]


class TestCommandExecutor:
    """Test cases for CommandExecutor class."""

    def test_is_command_true(self):
        """Test detecting command prefix."""
        executor = CommandExecutor()

        assert executor.is_command("run: ls")
        assert executor.is_command("run: git status")
        assert executor.is_command("run:pwd")

    def test_is_command_false(self):
        """Test non-command strings."""
        executor = CommandExecutor()

        assert not executor.is_command("Hello")
        assert not executor.is_command("What is run:")
        assert not executor.is_command("running a test")

    def test_extract_command(self):
        """Test extracting command from input."""
        executor = CommandExecutor()

        assert executor.extract_command("run: ls -la") == "ls -la"
        assert executor.extract_command("run:pwd") == "pwd"
        assert executor.extract_command("run: git status") == "git status"

    @patch("subprocess.run")
    def test_execute_command_success(self, mock_run):
        """Test successful command execution."""
        mock_run.return_value = Mock(returncode=0, stdout="test output", stderr="")

        executor = CommandExecutor()
        result = executor.execute("echo test")

        assert result["success"] is True
        assert result["output"] == "test output"
        assert result["error"] == ""

    @patch("subprocess.run")
    def test_execute_command_failure(self, mock_run):
        """Test failed command execution."""
        mock_run.return_value = Mock(
            returncode=1, stdout="", stderr="command not found"
        )

        executor = CommandExecutor()
        result = executor.execute("invalid_command")

        assert result["success"] is False
        assert result["error"] == "command not found"

    @patch("subprocess.run")
    def test_execute_command_exception(self, mock_run):
        """Test command execution with exception."""
        mock_run.side_effect = Exception("Test error")

        executor = CommandExecutor()
        result = executor.execute("test")

        assert result["success"] is False
        assert "Test error" in result["error"]


class TestAgent:
    """Test cases for Agent class."""

    def test_agent_init(self, tmp_path):
        """Test Agent initialization."""
        memory_file = tmp_path / "memory.json"

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = Agent(memory_file=str(memory_file))

            assert agent.memory_manager is not None
            assert agent.command_executor is not None
            assert agent.llm_provider is not None
            assert agent.provider_name == "openai"

    def test_agent_init_no_api_key(self, tmp_path):
        """Test Agent initialization without API key."""
        memory_file = tmp_path / "memory.json"

        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                Agent(memory_file=str(memory_file))

    def test_process_message_regular(self, tmp_path):
        """Test processing a regular message."""
        memory_file = tmp_path / "memory.json"

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = Agent(memory_file=str(memory_file))

            # Mock the LLM provider's chat_completion method
            with patch.object(agent.llm_provider, "chat_completion") as mock_chat:
                mock_chat.return_value = "Test response"
                response = agent.process_message("Hello")

                assert response == "Test response"
                # Should have system prompt + user + assistant = 3 messages
                assert len(agent.memory_manager.memory) == 3
                assert agent.memory_manager.memory[0]["role"] == "system"
                assert agent.memory_manager.memory[1]["role"] == "user"
                assert agent.memory_manager.memory[2]["role"] == "assistant"

    def test_process_message_command(self, tmp_path):
        """Test processing a command message."""
        memory_file = tmp_path / "memory.json"

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = Agent(memory_file=str(memory_file))

            with patch.object(agent.command_executor, "execute") as mock_execute:
                mock_execute.return_value = {
                    "success": True,
                    "output": "command output",
                    "error": "",
                }

                response = agent.process_message("run: ls")

                assert "command output" in response
                mock_execute.assert_called_once_with("ls")

    def test_should_exit(self, tmp_path):
        """Test exit command detection."""
        memory_file = tmp_path / "memory.json"

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = Agent(memory_file=str(memory_file))

            assert agent.should_exit("exit")
            assert agent.should_exit("quit")
            assert agent.should_exit("EXIT")
            assert agent.should_exit("QUIT")
            assert not agent.should_exit("hello")
