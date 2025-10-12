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

    # System prompt for resume tailoring capabilities
    SYSTEM_PROMPT = """You are a helpful AI assistant for resume tailoring and job application automation.

You can help users tailor their resumes to specific job postings. When a user asks to tailor their resume,
you should:

1. Ask for the job description file path (e.g., data/job_listings/Sr. Software Engineer - at Credibly.md)
   or URL if not provided
2. Ask for the resume JSON file path (e.g., data/resumes/a041bd2e-d54b-488f-adda-e4c707d5332d.json or
   data/master_resume.json) if not provided
3. Ask for output format preferences (HTML with theme, or markdown, and whether DOCX is needed)
4. Generate the appropriate command to execute

Common tailoring intents include phrases like:
- "tailor my resume"
- "fit my resume to this job"
- "customize resume for"
- "adapt my resume"
- "optimize resume for this position"

When you detect a tailoring intent, help gather the required information and suggest the appropriate
command using the 'run:' prefix.

Example commands:
- Markdown: run: python src/tailor.py --resume data/master_resume.json --jd "data/job_listings/job.md" --out out/tailored.md --format markdown
- HTML: run: python src/tailor.py --resume data/master_resume.json --jd "data/job_listings/job.md" --out out/tailored.html --format html --theme professional
- HTML with DOCX: run: python src/tailor.py --resume data/master_resume.json --jd "data/job_listings/job.md" --out out/tailored.html --format html --theme professional --docx

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

