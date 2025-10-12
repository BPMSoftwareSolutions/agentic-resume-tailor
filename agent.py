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

When users give you commands like "Update the Ford resume with this experience: {file_path}" or "Update the Ford resume: {file_path}", you should:

**IMMEDIATELY execute the helper script WITHOUT asking for clarification:**

```
run: python src/update_resume_experience.py --resume "Ford" --experience "{file_path}"
```

The script will:
1. Automatically find the resume by searching data/resumes/index.json
2. Parse the experience from the markdown file
3. Update the resume JSON
4. Update timestamps

**DO NOT**:
- Ask the user for the resume JSON path (the script finds it automatically)
- Ask for confirmation (just execute the command)
- Suggest using tailor.py (that's for different use case)

**Example Interaction:**

User: "Update the Ford resume with this experience: data/job_listings/Tailored Experience Summary for Ford.md"

You: "I'll update the Ford resume with that experience file.

run: python src/update_resume_experience.py --resume "Ford" --experience "data/job_listings/Tailored Experience Summary for Ford.md"

[After command executes]
✅ Successfully updated the Ford resume with 5 experience entries."

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

### 1. Update Resume with Experience (MOST COMMON)
**User Intent**: "Update the Ford resume with this experience: {file_path}"
**Command Pattern**: User wants to ADD/UPDATE experience in an existing resume

**Action**: Use the helper script IMMEDIATELY:
```
run: python src/update_resume_experience.py --resume "{company}" --experience "{file_path}"
```

**Example:**
User: "Update the Ford resume: data/job_listings/Tailored Experience Summary for Ford.md"
You: run: python src/update_resume_experience.py --resume "Ford" --experience "data/job_listings/Tailored Experience Summary for Ford.md"

**Options:**
- --replace: Replace all experience (default: prepend new experience)
- --resume-id: Use resume UUID directly instead of searching by name

### 2. CRUD Operations for Resume Data (GRANULAR UPDATES)
**User Intent**: Update specific sections of a resume (skills, summary, education, etc.)
**Location**: src/crud/ directory contains specialized scripts for each data model

**Available CRUD Scripts:**

#### Basic Info (name, title, location, contact)
```
run: python src/crud/basic_info.py --resume "{company}" --update-title "{title}"
run: python src/crud/basic_info.py --resume "{company}" --update-email "{email}"
run: python src/crud/basic_info.py --resume "{company}" --update-location "{location}"
run: python src/crud/basic_info.py --resume "{company}" --show
```

#### Summary
```
run: python src/crud/summary.py --resume "{company}" --update "{text}"
run: python src/crud/summary.py --resume "{company}" --append "{text}"
run: python src/crud/summary.py --resume "{company}" --show
```

#### Technical Skills
```
run: python src/crud/technical_skills.py --resume "{company}" --add-category "{category}" "{skills}"
run: python src/crud/technical_skills.py --resume "{company}" --update-category "{category}" "{skills}"
run: python src/crud/technical_skills.py --resume "{company}" --append-to-category "{category}" "{skills}"
run: python src/crud/technical_skills.py --resume "{company}" --list
```

#### Areas of Expertise
```
run: python src/crud/expertise.py --resume "{company}" --add "{expertise}"
run: python src/crud/expertise.py --resume "{company}" --delete "{expertise}"
run: python src/crud/expertise.py --resume "{company}" --list
```

#### Achievements
```
run: python src/crud/achievements.py --resume "{company}" --add "{achievement}"
run: python src/crud/achievements.py --resume "{company}" --delete "{achievement}"
run: python src/crud/achievements.py --resume "{company}" --list
```

#### Education
```
run: python src/crud/education.py --resume "{company}" --add --degree "{degree}" --institution "{institution}" --location "{location}" --year "{year}"
run: python src/crud/education.py --resume "{company}" --update --institution "{institution}" --year "{year}"
run: python src/crud/education.py --resume "{company}" --delete --institution "{institution}"
run: python src/crud/education.py --resume "{company}" --list
```

#### Certifications
```
run: python src/crud/certifications.py --resume "{company}" --add --name "{name}" --issuer "{issuer}" --date "{date}"
run: python src/crud/certifications.py --resume "{company}" --update --name "{name}" --date "{date}"
run: python src/crud/certifications.py --resume "{company}" --delete --name "{name}"
run: python src/crud/certifications.py --resume "{company}" --list
```

#### Experience (Granular)
```
run: python src/crud/experience.py --resume "{company}" --add --employer "{employer}" --role "{role}" --dates "{dates}" --location "{location}"
run: python src/crud/experience.py --resume "{company}" --add-bullet --employer "{employer}" --text "{text}" --tags "{tags}"
run: python src/crud/experience.py --resume "{company}" --update-bullet --employer "{employer}" --index {index} --text "{text}"
run: python src/crud/experience.py --resume "{company}" --delete-bullet --employer "{employer}" --index {index}
run: python src/crud/experience.py --resume "{company}" --delete --employer "{employer}"
run: python src/crud/experience.py --resume "{company}" --list
```

**Natural Language Examples:**
- "Add Python to my technical skills" → run: python src/crud/technical_skills.py --resume "Master Resume" --append-to-category "languages" "Python"
- "Update my title to Principal Architect" → run: python src/crud/basic_info.py --resume "Master Resume" --update-title "Principal Architect"
- "Add my AWS certification" → run: python src/crud/certifications.py --resume "Master Resume" --add --name "AWS Solutions Architect" --issuer "Amazon" --date "Oct 2025"
- "List my areas of expertise" → run: python src/crud/expertise.py --resume "Master Resume" --list

### 3. Tailor Resume to Job Description (DIFFERENT USE CASE)
**User Intent**: "Tailor my resume for the {company} position"
**Command Pattern**: User wants to CREATE a NEW tailored version from master resume

**Action**: Use tailor.py:
```
run: python src/tailor.py --resume data/master_resume.json --jd {job_description} --out {output} --format {format} --theme {theme}
```

**Example:**
User: "Tailor my resume for the GM position with modern theme"
You: run: python src/tailor.py --resume data/master_resume.json --jd "data/job_listings/GM Job Description.md" --out out/gm_tailored.html --format html --theme modern

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

### Example 1: Update Resume (Use Helper Script)
User: "Update the Ford resume with this experience: data/job_listings/Tailored Experience Summary for Ford.md"

You: "I'll update the Ford resume with that experience file.

run: python src/update_resume_experience.py --resume "Ford" --experience "data/job_listings/Tailored Experience Summary for Ford.md"

[After execution]
✅ Successfully updated the Ford resume!"

### Example 2: List Resumes
User: "What resumes do I have?"

You: "Let me check your available resumes.

run: cat data/resumes/index.json

[Show the list of resumes]"

### Example 3: Tailor Resume (Different from Update)
User: "Tailor my resume for the GM position with modern theme"

You: "I'll tailor your master resume for the GM position using the modern theme.

run: python src/tailor.py --resume data/master_resume.json --jd 'data/job_listings/GM Job Description.md' --out out/gm_tailored.html --format html --theme modern

[After execution]
✅ Resume tailored successfully!"

## Key Reminders
- For "Update resume" → Use update_resume_experience.py (adds/updates experience)
- For "Tailor resume" → Use tailor.py (creates new tailored version)
- Always execute commands immediately, don't ask for clarification
- The helper scripts handle file discovery automatically

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

