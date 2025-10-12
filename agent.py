#!/usr/bin/env python3
"""
Local AI Agent - Python-based interactive agent with OpenAI integration.
Related to GitHub Issue #8

This agent provides:
- Natural language interaction with OpenAI models
- Local command execution via 'run:' prefix
- Persistent memory across sessions
- Interactive command-line interface
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from openai import OpenAI


class MemoryManager:
    """Manages persistent memory for agent interactions."""
    
    def __init__(self, memory_file: str = "memory.json"):
        """
        Initialize the memory manager.
        
        Args:
            memory_file: Path to the memory JSON file
        """
        self.memory_file = memory_file
        self.memory: List[Dict[str, str]] = []
    
    def load(self) -> None:
        """Load memory from file if it exists."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
                print(f"📚 Loaded {len(self.memory)} messages from memory")
            except json.JSONDecodeError:
                print(f"⚠️  Warning: Could not parse {self.memory_file}, starting fresh")
                self.memory = []
        else:
            print("📝 Starting with fresh memory")
    
    def save(self) -> None:
        """Save current memory to file."""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Warning: Could not save memory: {e}")
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to memory.
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
        """
        self.memory.append({"role": role, "content": content})
    
    def get_messages(self) -> List[Dict[str, str]]:
        """
        Get all messages from memory.
        
        Returns:
            List of message dictionaries
        """
        return self.memory


class CommandExecutor:
    """Executes local system commands."""
    
    def is_command(self, text: str) -> bool:
        """
        Check if text is a command (starts with 'run:').
        
        Args:
            text: Input text to check
            
        Returns:
            True if text is a command
        """
        return text.strip().lower().startswith("run:")
    
    def extract_command(self, text: str) -> str:
        """
        Extract command from input text.
        
        Args:
            text: Input text with 'run:' prefix
            
        Returns:
            Command string without prefix
        """
        return text.strip()[4:].strip()
    
    def execute(self, command: str) -> Dict[str, Any]:
        """
        Execute a system command.
        
        Args:
            command: Command to execute
            
        Returns:
            Dictionary with success status, output, and error
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": "Command timed out after 30 seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }


class Agent:
    """Main agent class for interacting with OpenAI and executing commands."""

    # System prompt for resume tailoring capabilities with knowledge base
    SYSTEM_PROMPT = """You are a helpful AI assistant for resume tailoring and job application automation.
You have access to a knowledge base (agent_knowledge_base.json) that contains the codebase structure.

## IMPORTANT: Understanding User Commands

When users give you commands like "Update the Ford resume with this experience: {file_path}", you should:

1. **Parse the command** to extract:
   - Resume identifier (e.g., "Ford", "GM", "Credibly", or full resume name)
   - File path for the experience/content to apply

2. **Find the resume** by:
   - Reading data/resumes/index.json
   - Searching for a resume where the 'name' field contains the identifier (case-insensitive)
   - Example: "Ford" matches "Sidney_Jones_Senior_Software_Engineer_Ford"
   - Extract the 'id' field from the matching resume

3. **Construct the file path**: data/resumes/{id}.json

4. **Execute the update operation** using Python or API calls

## Resume Structure

Resumes are stored in:
- **Index**: data/resumes/index.json (contains metadata: id, name, created_at, updated_at, is_master, description)
- **Files**: data/resumes/{UUID}.json (actual resume content)

Resume naming pattern: {FirstName}_{LastName}_{Role}_{Company}
Examples:
- Sidney_Jones_Senior_Software_Engineer_Ford
- Sidney_Jones_Senior_Software_Engineer_GM
- Sidney_Jones_Senior_Software_Engineer_Credibly

## Job Listings Structure

Job listings and tailored experiences are in:
- **Directory**: data/job_listings/
- **Markdown files**:
  - Job descriptions: "Sr. Software Engineer - at Credibly.md"
  - Tailored experiences: "Tailored Experience Summary for Ford.md"

## Common Operations

### Update Resume with Experience
Command pattern: "Update the {company} resume with {file_path}"

**RECOMMENDED METHOD** - Use the helper script:
run: python src/update_resume_experience.py --resume "{company}" --experience "{file_path}"

This script will:
- Find the resume by company name (e.g., "Ford", "GM", "Credibly")
- Parse experience from the markdown file
- Update the resume JSON automatically
- Update timestamps in index.json

Example:
run: python src/update_resume_experience.py --resume "Ford" --experience "data/job_listings/Tailored Experience Summary for Ford.md"

Options:
- --replace: Replace all experience (default: prepend new experience)
- --resume-id: Use resume UUID directly instead of searching by name

### Tailor Resume
Command: python src/tailor.py --resume {resume_path} --jd {job_description} --out {output} --format {format} --theme {theme}

### List Resumes
Command: run: cat data/resumes/index.json | python -m json.tool

### List Job Listings
Command: run: ls data/job_listings/

## Available Commands

You can execute commands with 'run:' prefix. Whitelisted commands include:
- python src/tailor.py (for resume tailoring)
- python -m pytest (for testing)
- git status, git log, git diff
- ls, dir, pwd, echo, cat

## Example Interactions

User: "Update the Ford resume with this experience: data/job_listings/Tailored Experience Summary for Ford.md"

You should:
1. run: cat data/resumes/index.json
2. Find the resume with "Ford" in the name (e.g., id: "d474d761-18f2-48ab-99b5-9f30c54f75b2")
3. Explain: "I found the Ford resume with ID d474d761-18f2-48ab-99b5-9f30c54f75b2"
4. Read the experience file and update the resume
5. Confirm the update was successful

Available themes: professional, modern, executive, creative
"""

    def __init__(self, memory_file: str = "memory.json", model: str = "gpt-4"):
        """
        Initialize the agent.

        Args:
            memory_file: Path to memory JSON file
            model: OpenAI model to use

        Raises:
            ValueError: If OPENAI_API_KEY is not set
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in your environment or .env file."
            )

        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        self.memory_manager = MemoryManager(memory_file)
        self.command_executor = CommandExecutor()

        # Load existing memory
        self.memory_manager.load()

        # Add system prompt if not already in memory
        if not self.memory_manager.get_messages() or \
           self.memory_manager.get_messages()[0].get("role") != "system":
            self.memory_manager.memory.insert(0, {
                "role": "system",
                "content": self.SYSTEM_PROMPT
            })
    
    def process_message(self, user_input: str) -> str:
        """
        Process user input and return response.
        
        Args:
            user_input: User's input message
            
        Returns:
            Response string
        """
        # Check if it's a command
        if self.command_executor.is_command(user_input):
            command = self.command_executor.extract_command(user_input)
            print(f"🔧 Executing command: {command}")
            
            result = self.command_executor.execute(command)
            
            if result["success"]:
                response = f"✅ Command executed successfully:\n{result['output']}"
            else:
                response = f"❌ Command failed:\n{result['error']}"
            
            # Add to memory
            self.memory_manager.add_message("user", user_input)
            self.memory_manager.add_message("assistant", response)
            self.memory_manager.save()
            
            return response
        
        # Regular message - send to OpenAI
        self.memory_manager.add_message("user", user_input)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.memory_manager.get_messages()
            )
            
            assistant_message = response.choices[0].message.content
            self.memory_manager.add_message("assistant", assistant_message)
            self.memory_manager.save()
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"❌ Error communicating with OpenAI: {str(e)}"
            print(error_msg)
            return error_msg
    
    def should_exit(self, user_input: str) -> bool:
        """
        Check if user wants to exit.
        
        Args:
            user_input: User's input
            
        Returns:
            True if user wants to exit
        """
        return user_input.strip().lower() in ["exit", "quit"]
    
    def run(self) -> None:
        """Run the interactive agent loop."""
        print("🤖 Local AI Agent Started")
        print("=" * 50)
        print("Commands:")
        print("  - Type 'run: <command>' to execute local commands")
        print("  - Type 'exit' or 'quit' to stop")
        print("  - Type anything else to chat with the AI")
        print("=" * 50)
        print()
        
        try:
            while True:
                try:
                    user_input = input("💬 > ").strip()
                    
                    if not user_input:
                        continue
                    
                    if self.should_exit(user_input):
                        print("\n👋 Goodbye!")
                        break
                    
                    response = self.process_message(user_input)
                    print(f"\n🤖 {response}\n")
                    
                except KeyboardInterrupt:
                    print("\n\n👋 Goodbye!")
                    break
                except EOFError:
                    print("\n\n👋 Goodbye!")
                    break
                    
        finally:
            # Save memory on exit
            self.memory_manager.save()
            print("💾 Memory saved")


def main():
    """Main entry point for the agent."""
    try:
        # Get model from environment or use default
        model = os.getenv("OPENAI_MODEL", "gpt-4")
        
        # Initialize and run agent
        agent = Agent(model=model)
        agent.run()
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease set your OPENAI_API_KEY environment variable:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

