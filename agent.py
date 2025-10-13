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

# Import agent modules for result analysis and token management
try:
    from src.agent.result_analyzer import ResultAnalyzer
    from src.agent.token_manager import TokenManager
except ImportError:
    # Fallback if running from different directory
    sys.path.insert(0, str(Path(__file__).parent))
    from src.agent.result_analyzer import ResultAnalyzer
    from src.agent.token_manager import TokenManager

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    try:
        # Set console to UTF-8 mode
        os.system('chcp 65001 > nul')
        # Reconfigure stdout/stderr to use UTF-8
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        # If reconfiguration fails, continue without emoji support
        pass


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
                encoding='utf-8',
                errors='replace',  # Replace invalid characters instead of failing
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

### 3. Duplicate Resume (CREATE NEW EDITABLE RESUME)
**User Intent**: "Using the Ford resume, create a new one for X" or "Duplicate the Ford resume" or "Create a new resume for X"
**Command Pattern**: User wants to CREATE A NEW RESUME JSON FILE that can be edited later

**IMPORTANT DISTINCTION**:
- "Create a new resume" = duplicate_resume.py (creates editable JSON in database)
- "Export/generate HTML" = tailor.py (creates one-time HTML output)

**Action**: Use duplicate_resume.py script:
```
run: python src/duplicate_resume.py --resume "{source_resume}" --new-name "{new_name}"
```

**Examples:**
User: "Using the Ford resume, create a new one for the Subscription Billing position"
You: I'll create a new resume based on your Ford resume for the Subscription Billing position.

run: python src/duplicate_resume.py --resume "Ford" --new-name "Sidney_Jones_Engineering_Manager_Subscription_Billing"

User: "Duplicate the Master Resume for a new company"
You: run: python src/duplicate_resume.py --resume "Master Resume" --new-name "Sidney_Jones_Senior_Engineer_NewCo"

User: "Copy my Ford resume"
You: run: python src/duplicate_resume.py --resume "Ford" --new-name "Sidney_Jones_Senior_Engineer_Ford_Copy"

**Optional**: Add description with --description flag:
```
run: python src/duplicate_resume.py --resume "Ford" --new-name "New_Resume" --description "Tailored for X position"
```

**WORKFLOW**: After duplicating, you can optionally:
1. Update sections with CRUD scripts
2. Generate HTML/DOCX output with tailor.py

### 4. Tailor Resume to Job Description (EXPORT TO HTML/DOCX)
**User Intent**: "Export my resume as HTML" or "Generate a tailored HTML for {job}" or "Create an HTML version"
**Command Pattern**: User wants to EXPORT an existing resume to HTML/DOCX format (one-time output, not editable)

**IMPORTANT**: When user says "Using the {Company} Resume" or "Use the {Company} resume", they want to use that specific company's resume as the base, NOT the master resume!

**Action**: Use tailor.py with the correct resume:
```
# If user specifies a company resume (e.g., "Ford Resume"):
run: python src/tailor.py --resume "{company}" --jd "{job_description}" --out "{output}" --format html --theme modern

# If user doesn't specify, use master resume:
run: python src/tailor.py --resume "Master Resume" --jd "{job_description}" --out "{output}" --format html --theme modern
```

**The tailor.py script now supports resume lookup by name!** Just pass the company name or "Master Resume" and it will find the correct file automatically.

**Examples:**
User: "Export the Ford Resume as HTML for this job posting: X.md"
You: run: python src/tailor.py --resume "Ford" --jd "data/job_listings/X.md" --out "out/ford_tailored.html" --format html --theme modern

User: "Generate an HTML version of my resume for the GM position"
You: run: python src/tailor.py --resume "Master Resume" --jd "data/job_listings/GM Job Description.md" --out "out/gm_tailored.html" --format html --theme modern

User: "Create a tailored HTML for the Credibly job"
You: run: python src/tailor.py --resume "Master Resume" --jd "data/job_listings/Sr. Software Engineer - at Credibly.md" --out "out/credibly.html" --format html --theme modern

### List Resumes (Formatted Table)
Command: run: python src/utils/list_resumes.py
Options:
  --format table   # Default: formatted table with details
  --format simple  # Simple numbered list
  --format json    # JSON output

### List Job Listings (Formatted Table)
Command: run: python src/utils/list_job_listings.py
Options:
  --format table   # Default: formatted table with details
  --format simple  # Simple numbered list
  --format json    # JSON output

## Available Commands

**IMPORTANT - Cross-Platform Compatibility:**
- The system may be running on Windows, Linux, or Mac
- ALWAYS use Python commands when possible (they work everywhere)
- AVOID Unix-specific commands like `cat`, `ls`, `grep` on Windows
- Use `python -m json.tool` instead of `cat file.json | python -m json.tool`
- Use `dir` on Windows or `ls` on Unix, OR use Python: `python -c "import os; print(os.listdir('path'))"`

You can execute commands with 'run:' prefix. Whitelisted commands include:
- python src/duplicate_resume.py (for duplicating resumes)
- python src/tailor.py (for resume tailoring)
- python src/update_resume_experience.py (for updating resume experience)
- python src/crud/*.py (for granular CRUD operations)
- python -m pytest (for testing)
- git status, git log, git diff
- ls, dir, pwd, echo, cat

## Example Interactions

### Example 1: Create New Resume (Duplicate + Optional Tailor)
User: "Using the Ford resume, create a new one for the Subscription Billing position"

You: "I'll create a new resume based on your Ford resume for the Subscription Billing position.

run: python src/duplicate_resume.py --resume "Ford" --new-name "Sidney_Jones_Engineering_Manager_Subscription_Billing"

[After execution]
✅ Successfully duplicated resume!
   New Resume ID: a04640bf-d6bb-4d7f-a949-69026acdb212
   New Resume Name: Sidney_Jones_Engineering_Manager_Subscription_Billing

This creates a new editable resume in the database. Would you like me to:
1. Export it as HTML/DOCX for the job posting?
2. Update specific sections first?
3. Leave it as-is for now?"

**IMPORTANT**: If user says "create a new resume", ALWAYS use duplicate_resume.py first, NOT tailor.py!
- duplicate_resume.py = Creates editable JSON in database
- tailor.py = Exports to HTML/DOCX (one-time output)

### Example 2: Update Resume (Use Helper Script)
User: "Update the Ford resume with this experience: data/job_listings/Tailored Experience Summary for Ford.md"

You: "I'll update the Ford resume with that experience file.

run: python src/update_resume_experience.py --resume "Ford" --experience "data/job_listings/Tailored Experience Summary for Ford.md"

[After execution]
✅ Successfully updated the Ford resume!"

### Example 3: List Resumes
User: "What resumes do I have?"

You: "Let me check your available resumes.

run: python src/utils/list_resumes.py

[Shows formatted table with resume names, master status, updated dates, and descriptions]"

### Example 4: Intelligent Resume Tailoring (NEW - Phase 2)
User: "Tailor my Ford resume for the GM Subscription Billing position"

You: "I'll analyze the job posting and intelligently tailor your Ford resume.

run: python src/orchestrator/crud_orchestrator.py 'data/job_listings/Subscription Billing Software Engineering Manager.md' 'data/resumes/{resume_id}.json' 'Ford'

[After execution - shows match score and operations]
✅ Generated 10 tailoring operations:
   - Update title to match job
   - Add missing skills (aws, azure, zuora, etc.)
   - Add relevant expertise areas
   - Suggestions for manual updates

Would you like me to execute these operations to update your resume?"

### Example 5: Export Resume (HTML/DOCX)
User: "Export my Ford resume as HTML with modern theme"

You: "I'll export your Ford resume to HTML.

run: python src/tailor.py --resume 'Ford' --jd 'data/job_listings/Ford Job Description.md' --out out/ford_resume.html --format html --theme modern --docx

[After execution]
✅ Resume exported successfully!"

## Key Reminders
- For "Create/duplicate resume" → Use duplicate_resume.py (creates a copy of existing resume)
- For "Update resume" → Use update_resume_experience.py (adds/updates experience)
- For "Tailor resume intelligently" → Use crud_orchestrator.py (analyzes job and generates CRUD operations)
- For "Export resume" → Use tailor.py (creates HTML/DOCX output files)
- Always execute commands immediately, don't ask for clarification
- The helper scripts handle file discovery automatically

## INTELLIGENT RESUME TAILORING (Phase 2 - NEW)

The system now includes intelligent orchestration for automated resume tailoring:

### Orchestration Modules (src/orchestrator/)

#### 1. Resume Matcher
**Purpose**: Analyze how well a resume matches a job posting
**Command**: `python src/orchestrator/resume_matcher.py <job_file.md> <resume_file.json>`
**Output**:
- Match score (0-100%)
- Matching skills
- Missing skills
- Relevant experience entries
- Improvement suggestions

#### 2. CRUD Orchestrator
**Purpose**: Generate and execute sequences of CRUD operations to tailor resumes
**Command**: `python src/orchestrator/crud_orchestrator.py <job_file.md> <resume_file.json> <resume_name>`
**Features**:
- Analyzes job requirements vs resume content
- Generates prioritized CRUD operations
- Supports dry-run mode (default)
- Categorizes skills automatically (languages, cloud, devops, billing, AI)

**Operation Types Generated**:
1. Update title to match job
2. Add missing technical skills (categorized)
3. Update summary (manual suggestion)
4. Add relevant expertise areas
5. Highlight compliance experience (manual suggestion)

**Example Usage**:
```
run: python src/orchestrator/crud_orchestrator.py 'data/job_listings/GM Job.md' 'data/resumes/{id}.json' 'Ford'
```

### Parser Modules (src/parsers/)

#### 1. Job Posting Parser
**Purpose**: Extract structured data from job posting markdown files
**Command**: `python src/parsers/job_posting_parser.py <job_file.md>`
**Extracts**: title, company, location, skills, responsibilities, experience requirements

#### 2. Experience Parser
**Purpose**: Parse markdown experience files
**Command**: `python src/parsers/experience_parser.py <experience_file.md>`
**Format**: `### **Employer - Role (Dates)**`

#### 3. Natural Language Command Parser
**Purpose**: Map natural language to CRUD commands
**Examples**:
- "Add Python to my technical skills" → technical_skills.py command
- "Update my title to Principal Architect" → basic_info.py command

### When to Use What

**Intelligent Tailoring** (Recommended for job applications):
```
run: python src/orchestrator/crud_orchestrator.py <job_file> <resume_file> <resume_name>
```
Use when: User wants to tailor resume for a specific job posting

**Manual CRUD Operations** (For specific updates):
```
run: python src/crud/technical_skills.py --resume "Ford" --add-category "languages" "Python, Java"
```
Use when: User wants to update a specific section

**Export to HTML/DOCX** (For final output):
```
run: python src/tailor.py --resume "Ford" --jd <job_file> --out <output> --format html --docx
```
Use when: User wants to export resume for submission

## IMPORTANT: Verify Command Results
After executing CRUD operations, ALWAYS review the output to verify success:

1. **Check for success indicators**: Look for "[SUCCESS]" or "Successfully" messages
2. **Verify the data**: If the output shows IDs, names, or counts, mention them to the user
3. **Offer next steps**: After successful operations, suggest logical follow-up actions

**Example:**
After duplicating a resume, you should say:
"✅ Successfully duplicated resume!
   - New Resume ID: a04640bf-d6bb-4d7f-a949-69026acdb212
   - New Resume Name: Sidney_Jones_Engineering_Manager_Subscription_Billing

Would you like me to:
1. Update specific sections of this new resume?
2. Tailor it to a job posting?
3. List all your resumes?"

**If an error occurs**, explain what went wrong and suggest solutions.

Available themes: professional, modern, executive, creative
"""

    def __init__(self, memory_file: str = "memory.json", model: str = "gpt-4",
                 auto_execute: bool = True, confirm_execution: bool = True):
        """
        Initialize the agent.

        Args:
            memory_file: Path to memory JSON file
            model: OpenAI model to use
            auto_execute: Whether to auto-execute commands from agent responses
            confirm_execution: Whether to ask for confirmation before executing

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
        self.auto_execute = auto_execute
        self.confirm_execution = confirm_execution
        self.client = OpenAI(api_key=self.api_key)
        self.memory_manager = MemoryManager(memory_file)
        self.command_executor = CommandExecutor()

        # Initialize result analyzer and token manager (Issue #24)
        self.result_analyzer = ResultAnalyzer()
        self.token_manager = TokenManager(model=model)

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
        # Check token usage before processing (Issue #24)
        token_status = self.token_manager.check_limit(self.memory_manager.get_messages())
        if token_status['warning'] and token_status['message']:
            print(f"\n{token_status['message']}\n")

        # Check if it's a command
        if self.command_executor.is_command(user_input):
            command = self.command_executor.extract_command(user_input)
            print(f"🔧 Executing command: {command}")

            result = self.command_executor.execute(command)

            # Use result analyzer for intelligent feedback (Issue #24)
            analysis = self.result_analyzer.analyze(command, result)

            # Format response with analysis
            response = analysis['message']

            # Add suggestions if available
            if analysis['suggestions']:
                response += f"\n\n💡 What would you like to do next?\n"
                for i, suggestion in enumerate(analysis['suggestions'], 1):
                    response += f"   {i}. {suggestion}\n"

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

            # Check if response contains a command to auto-execute
            if self.auto_execute:
                command = self._extract_command_from_response(assistant_message)
                if command:
                    # Ask for confirmation if enabled
                    should_execute = True
                    if self.confirm_execution:
                        should_execute = self._confirm_execution(command)

                    if should_execute:
                        print(f"🔧 Executing command: {command}")
                        result = self.command_executor.execute(command)

                        # Use result analyzer for intelligent feedback (Issue #24)
                        analysis = self.result_analyzer.analyze(command, result)
                        execution_result = analysis['message']

                        # Add suggestions if available
                        if analysis['suggestions']:
                            execution_result += f"\n\n💡 What would you like to do next?\n"
                            for i, suggestion in enumerate(analysis['suggestions'], 1):
                                execution_result += f"   {i}. {suggestion}\n"

                        # Add execution result to memory
                        self.memory_manager.add_message("user", f"run: {command}")
                        self.memory_manager.add_message("assistant", execution_result)
                        self.memory_manager.save()

                        # Append execution result to response
                        assistant_message += f"\n\n{execution_result}"

            return assistant_message

        except Exception as e:
            error_msg = f"❌ Error communicating with OpenAI: {str(e)}"
            print(error_msg)
            return error_msg
    
    def _extract_command_from_response(self, response: str) -> Optional[str]:
        """
        Extract command from agent response (looks for 'run:' pattern).

        Args:
            response: Agent response text

        Returns:
            Command string if found, None otherwise
        """
        import re
        pattern = r'run:\s*(.+?)(?:\n|$)'
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def _confirm_execution(self, command: str) -> bool:
        """
        Ask user to confirm command execution.

        Args:
            command: Command to execute

        Returns:
            True if user confirms execution, False otherwise
        """
        print(f"\n❓ Execute this command? (y/n/edit): ", end="", flush=True)
        try:
            response = input().strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n⏭️  Skipping command execution")
            return False

        if response in ['y', 'yes']:
            return True
        elif response == 'edit':
            print(f"✏️  Edit command: ", end="", flush=True)
            try:
                edited_command = input().strip()
                if edited_command:
                    # Execute edited command
                    print(f"🔧 Executing edited command: {edited_command}")
                    result = self.command_executor.execute(edited_command)
                    print(self._format_execution_result(result))
            except (KeyboardInterrupt, EOFError):
                print("\n⏭️  Skipping command execution")
            return False
        else:
            print("⏭️  Skipping command execution")
            return False

    def _format_execution_result(self, result: Dict[str, Any]) -> str:
        """
        Format command execution result.

        Args:
            result: Execution result dictionary

        Returns:
            Formatted result string
        """
        if result["success"]:
            return f"✅ Command executed successfully:\n{result['output']}"
        else:
            return f"❌ Command failed:\n{result['error']}"

    def should_exit(self, user_input: str) -> bool:
        """
        Check if user wants to exit.

        Args:
            user_input: User's input

        Returns:
            True if user wants to exit
        """
        return user_input.strip().lower() in ["exit", "quit"]

    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get memory usage statistics (Issue #24).

        Returns:
            Dictionary with token usage statistics
        """
        return self.token_manager.get_stats(self.memory_manager.get_messages())
    
    def run(self) -> None:
        """Run the interactive agent loop."""
        print("🤖 Local AI Agent Started")
        print("=" * 50)
        print("Commands:")
        print("  - Type 'run: <command>' to execute local commands")
        print("  - Type 'exit' or 'quit' to stop")
        print("  - Type anything else to chat with the AI")
        print()
        print("Settings:")
        print(f"  - Auto-execute: {'✅ Enabled' if self.auto_execute else '❌ Disabled'}")
        if self.auto_execute:
            print(f"  - Confirmation: {'✅ Required' if self.confirm_execution else '❌ Disabled'}")

        # Show token usage (Issue #24)
        try:
            stats = self.get_memory_stats()
            print(f"  - Memory: {stats['total_tokens']}/{stats['max_tokens']} tokens ({stats['percentage']}%)")
        except Exception as e:
            print(f"  - Memory: Unable to calculate token usage")

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
    import argparse

    parser = argparse.ArgumentParser(
        description="Local AI Agent with OpenAI integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings (auto-execute with confirmation)
  python agent.py

  # Disable auto-execution
  python agent.py --no-auto-execute

  # Auto-execute without confirmation
  python agent.py --no-confirm

  # Use a different model
  python agent.py --model gpt-4-turbo
        """
    )

    parser.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", "gpt-4"),
        help="OpenAI model to use (default: gpt-4 or OPENAI_MODEL env var)"
    )
    parser.add_argument(
        "--memory",
        default="memory.json",
        help="Memory file path (default: memory.json)"
    )
    parser.add_argument(
        "--auto-execute",
        action="store_true",
        default=True,
        dest="auto_execute",
        help="Auto-execute commands from agent responses (default: enabled)"
    )
    parser.add_argument(
        "--no-auto-execute",
        action="store_false",
        dest="auto_execute",
        help="Disable auto-execution of commands"
    )
    parser.add_argument(
        "--no-confirm",
        action="store_false",
        dest="confirm_execution",
        default=True,
        help="Skip confirmation prompts before executing commands"
    )

    args = parser.parse_args()

    try:
        # Initialize and run agent
        agent = Agent(
            memory_file=args.memory,
            model=args.model,
            auto_execute=args.auto_execute,
            confirm_execution=args.confirm_execution
        )
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

