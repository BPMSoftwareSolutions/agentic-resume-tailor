# Phase 2: Memory Search, Update & Correction

**Parent Issue**: #23 - Intelligent Agent Memory Management  
**Priority**: 🟡 High  
**Estimated Effort**: 8-12 hours

## User Value Delivered

Users will be able to:
1. ✅ **Search past conversations** - Find information from previous sessions
2. ✅ **Update incorrect information** - Fix mistakes in memory without clearing everything
3. ✅ **Delete specific messages** - Remove unwanted or sensitive information
4. ✅ **Ask the agent to recall facts** - "What was the ID of my Ford resume?"
5. ✅ **Correct agent mistakes** - "That email is wrong, update it to..."

## Problem Statement

Currently:
- ❌ Can't search past conversations for specific information
- ❌ Can't fix mistakes in memory (only option: clear everything)
- ❌ Can't delete specific messages
- ❌ Agent can't recall facts from previous conversations
- ❌ Incorrect information persists indefinitely

## Solution Overview

Add **search, update, and correction** capabilities to memory management:

### Part A: Memory Search
1. Keyword search across all messages
2. Filter by date range
3. Filter by message type (user/assistant/system)
4. Natural language queries to agent

### Part B: Memory Update & Correction
1. Update specific messages by index or ID
2. Delete specific messages
3. Find and replace across memory
4. Agent-assisted corrections

## Technical Implementation

### 1. Enhance MemoryManager with Metadata

**File**: `agent.py`

Update `MemoryManager` class:
```python
import uuid
from datetime import datetime

class MemoryManager:
    """Manages persistent memory for agent interactions."""
    
    def __init__(self, memory_file: str = "memory.json"):
        self.memory_file = memory_file
        self.memory: List[Dict[str, Any]] = []
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None) -> str:
        """
        Add a message to memory with metadata.
        
        Returns:
            Message ID (UUID)
        """
        message_id = str(uuid.uuid4())
        message = {
            "id": message_id,
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.memory.append(message)
        return message_id
    
    def search(self, query: str, case_sensitive: bool = False) -> List[Dict]:
        """
        Search memory for messages containing query string.
        
        Args:
            query: Search term
            case_sensitive: Whether search is case-sensitive
            
        Returns:
            List of matching messages with context
        """
        results = []
        
        for i, message in enumerate(self.memory):
            content = message.get("content", "")
            search_content = content if case_sensitive else content.lower()
            search_query = query if case_sensitive else query.lower()
            
            if search_query in search_content:
                results.append({
                    "index": i,
                    "message": message,
                    "context": self._get_context(i, before=1, after=1)
                })
        
        return results
    
    def search_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Search memory by date range.
        
        Args:
            start_date: ISO format date string
            end_date: ISO format date string
            
        Returns:
            List of messages within date range
        """
        results = []
        
        for i, message in enumerate(self.memory):
            timestamp = message.get("timestamp", "")
            if start_date <= timestamp <= end_date:
                results.append({
                    "index": i,
                    "message": message
                })
        
        return results
    
    def search_by_role(self, role: str) -> List[Dict]:
        """
        Search memory by message role.
        
        Args:
            role: Message role (user, assistant, system)
            
        Returns:
            List of messages with specified role
        """
        results = []
        
        for i, message in enumerate(self.memory):
            if message.get("role") == role:
                results.append({
                    "index": i,
                    "message": message
                })
        
        return results
    
    def update_message(self, message_id: str, new_content: str) -> bool:
        """
        Update a message by ID.
        
        Args:
            message_id: Message UUID
            new_content: New content for the message
            
        Returns:
            True if updated, False if not found
        """
        for message in self.memory:
            if message.get("id") == message_id:
                message["content"] = new_content
                message["updated_at"] = datetime.now().isoformat()
                return True
        return False
    
    def delete_message(self, message_id: str) -> bool:
        """
        Delete a message by ID.
        
        Args:
            message_id: Message UUID
            
        Returns:
            True if deleted, False if not found
        """
        for i, message in enumerate(self.memory):
            if message.get("id") == message_id:
                del self.memory[i]
                return True
        return False
    
    def delete_range(self, start_index: int, end_index: int) -> int:
        """
        Delete a range of messages.
        
        Args:
            start_index: Start index (inclusive)
            end_index: End index (inclusive)
            
        Returns:
            Number of messages deleted
        """
        if start_index < 0 or end_index >= len(self.memory):
            return 0
        
        count = end_index - start_index + 1
        del self.memory[start_index:end_index + 1]
        return count
    
    def find_and_replace(self, find: str, replace: str, 
                        case_sensitive: bool = False) -> int:
        """
        Find and replace text across all messages.
        
        Args:
            find: Text to find
            replace: Replacement text
            case_sensitive: Whether search is case-sensitive
            
        Returns:
            Number of replacements made
        """
        count = 0
        
        for message in self.memory:
            content = message.get("content", "")
            
            if case_sensitive:
                if find in content:
                    message["content"] = content.replace(find, replace)
                    message["updated_at"] = datetime.now().isoformat()
                    count += 1
            else:
                import re
                pattern = re.compile(re.escape(find), re.IGNORECASE)
                if pattern.search(content):
                    message["content"] = pattern.sub(replace, content)
                    message["updated_at"] = datetime.now().isoformat()
                    count += 1
        
        return count
    
    def _get_context(self, index: int, before: int = 1, after: int = 1) -> Dict:
        """Get context messages around an index."""
        return {
            "before": self.memory[max(0, index - before):index],
            "after": self.memory[index + 1:min(len(self.memory), index + after + 1)]
        }
    
    def get_statistics(self) -> Dict:
        """Get memory statistics."""
        return {
            "total_messages": len(self.memory),
            "by_role": {
                "user": len([m for m in self.memory if m.get("role") == "user"]),
                "assistant": len([m for m in self.memory if m.get("role") == "assistant"]),
                "system": len([m for m in self.memory if m.get("role") == "system"])
            },
            "oldest_message": self.memory[0].get("timestamp") if self.memory else None,
            "newest_message": self.memory[-1].get("timestamp") if self.memory else None
        }
```

### 2. Add Agent Commands for Memory Operations

**File**: `agent.py`

Update `Agent` class to handle memory commands:
```python
def process_message(self, user_input: str) -> str:
    # ... existing code ...
    
    # Check for memory commands
    if user_input.lower().startswith("search memory:"):
        query = user_input[14:].strip()
        return self._handle_memory_search(query)
    
    elif user_input.lower().startswith("update memory:"):
        return self._handle_memory_update(user_input)
    
    elif user_input.lower().startswith("delete memory:"):
        return self._handle_memory_delete(user_input)
    
    # ... rest of existing code ...

def _handle_memory_search(self, query: str) -> str:
    """Handle memory search command."""
    results = self.memory_manager.search(query)
    
    if not results:
        return f"No messages found containing '{query}'"
    
    output = [f"Found {len(results)} message(s) containing '{query}':\n"]
    
    for i, result in enumerate(results, 1):
        msg = result["message"]
        output.append(f"{i}. [{msg['role']}] at {msg['timestamp']}")
        output.append(f"   {msg['content'][:100]}...")
        output.append(f"   Message ID: {msg['id']}\n")
    
    return "\n".join(output)

def _handle_memory_update(self, command: str) -> str:
    """Handle memory update command."""
    # Parse: "update memory: <id> to <new_content>"
    import re
    match = re.match(r'update memory:\s*([a-f0-9-]+)\s+to\s+(.+)', command, re.IGNORECASE)
    
    if not match:
        return "Invalid format. Use: update memory: <message_id> to <new_content>"
    
    message_id = match.group(1)
    new_content = match.group(2)
    
    if self.memory_manager.update_message(message_id, new_content):
        self.memory_manager.save()
        return f"✅ Updated message {message_id}"
    else:
        return f"❌ Message {message_id} not found"

def _handle_memory_delete(self, command: str) -> str:
    """Handle memory delete command."""
    # Parse: "delete memory: <id>"
    import re
    match = re.match(r'delete memory:\s*([a-f0-9-]+)', command, re.IGNORECASE)
    
    if not match:
        return "Invalid format. Use: delete memory: <message_id>"
    
    message_id = match.group(1)
    
    if self.memory_manager.delete_message(message_id):
        self.memory_manager.save()
        return f"✅ Deleted message {message_id}"
    else:
        return f"❌ Message {message_id} not found"
```

### 3. Update System Prompt for Memory Operations

**File**: `agent.py`

Add to `SYSTEM_PROMPT`:
```python
## Memory Operations

You can help users search and manage conversation memory:

**Search Memory:**
- "search memory: <query>" - Search for messages containing query
- Example: "search memory: Ford resume"

**Update Memory:**
- "update memory: <message_id> to <new_content>" - Update a specific message
- Example: "update memory: abc-123 to email@example.com"

**Delete Memory:**
- "delete memory: <message_id>" - Delete a specific message
- Example: "delete memory: abc-123"

**Natural Language Queries:**
Users can also ask you to recall information:
- "What was the ID of my Ford resume?"
- "When did I create the GM resume?"
- "What job postings have I worked on?"

When users ask these questions, use the search functionality to find the answer.
```

### 4. Add API Endpoints

**File**: `src/api/app.py`

```python
@app.route('/api/agent/memory/search', methods=['POST'])
def search_memory():
    """
    Search agent memory.
    
    Request body:
        {
            "query": "search term",
            "case_sensitive": false (optional)
        }
    
    Returns:
        JSON response with search results
    """
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        memory = get_memory_manager()
        results = memory.search(
            query=query,
            case_sensitive=data.get('case_sensitive', False)
        )
        
        return jsonify({
            "success": True,
            "results": results,
            "count": len(results)
        })
    
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500


@app.route('/api/agent/memory/<message_id>', methods=['PUT'])
def update_memory_message(message_id):
    """
    Update a specific memory message.
    
    Request body:
        {
            "content": "new content"
        }
    
    Returns:
        JSON response with success status
    """
    try:
        data = request.get_json()
        new_content = data.get('content')
        
        if not new_content:
            return jsonify({"error": "Content is required"}), 400
        
        memory = get_memory_manager()
        success = memory.update_message(message_id, new_content)
        
        if success:
            memory.save()
            return jsonify({
                "success": True,
                "message": f"Updated message {message_id}"
            })
        else:
            return jsonify({"error": "Message not found"}), 404
    
    except Exception as e:
        return jsonify({"error": f"Update failed: {str(e)}"}), 500


@app.route('/api/agent/memory/<message_id>', methods=['DELETE'])
def delete_memory_message(message_id):
    """
    Delete a specific memory message.
    
    Returns:
        JSON response with success status
    """
    try:
        memory = get_memory_manager()
        success = memory.delete_message(message_id)
        
        if success:
            memory.save()
            return jsonify({
                "success": True,
                "message": f"Deleted message {message_id}"
            })
        else:
            return jsonify({"error": "Message not found"}), 404
    
    except Exception as e:
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500
```

## Testing & Verification

### Manual Testing Scenarios

#### Scenario 1: Search Past Conversations

**Steps**:
1. Have a conversation where you create a Ford resume
2. Later, ask: "search memory: Ford"
3. Observe search results

**Expected Output**:
```
Found 3 message(s) containing 'Ford':

1. [user] at 2025-10-12T10:30:00
   Duplicate the Master resume for Ford position...
   Message ID: abc-123-def

2. [assistant] at 2025-10-12T10:30:15
   I'll duplicate the Master resume for Ford...
   Message ID: def-456-ghi

3. [assistant] at 2025-10-12T10:30:20
   ✅ Successfully created resume 'Sidney_Jones_Engineer_Ford'...
   Message ID: ghi-789-jkl
```

#### Scenario 2: Natural Language Recall

**Steps**:
1. Create a resume with specific ID
2. Later, ask: "What was the ID of my Ford resume?"
3. Agent should search memory and provide answer

**Expected Output**:
```
🤖 Let me search my memory for that information.

[Searches memory for "Ford resume"]

Based on our previous conversation, your Ford resume has ID: abc-123-def-456
It was created on 2025-10-12 at 10:30:20.
```

#### Scenario 3: Update Incorrect Information

**Steps**:
1. Agent stores incorrect email: "old@email.com"
2. User says: "That email is wrong, it should be new@email.com"
3. Agent should offer to update memory

**Expected Output**:
```
🤖 I apologize for the error. Would you like me to update that in my memory?

I found the incorrect email in message abc-123. I can update it to new@email.com.

Should I proceed? (yes/no)

[User: yes]

✅ Updated message abc-123
The email has been corrected to new@email.com in my memory.
```

#### Scenario 4: Delete Sensitive Information

**Steps**:
1. User accidentally shares sensitive info
2. User says: "delete memory: <message_id>"
3. Message should be deleted

**Expected Output**:
```
✅ Deleted message abc-123-def
The message has been removed from memory.
```

### Unit Tests

**File**: `tests/test_memory_search.py`
```python
def test_search_memory():
    """Test memory search functionality."""
    manager = MemoryManager("test_memory.json")
    
    # Add test messages
    manager.add_message("user", "Create Ford resume")
    manager.add_message("assistant", "Creating Ford resume...")
    manager.add_message("user", "Create GM resume")
    
    # Search for "Ford"
    results = manager.search("Ford")
    
    assert len(results) == 2
    assert "Ford" in results[0]["message"]["content"]

def test_update_message():
    """Test message update functionality."""
    manager = MemoryManager("test_memory.json")
    
    # Add message
    msg_id = manager.add_message("user", "old content")
    
    # Update it
    success = manager.update_message(msg_id, "new content")
    
    assert success == True
    
    # Verify update
    messages = manager.get_messages()
    assert messages[0]["content"] == "new content"
    assert "updated_at" in messages[0]

def test_delete_message():
    """Test message deletion."""
    manager = MemoryManager("test_memory.json")
    
    # Add messages
    msg_id1 = manager.add_message("user", "message 1")
    msg_id2 = manager.add_message("user", "message 2")
    
    # Delete first message
    success = manager.delete_message(msg_id1)
    
    assert success == True
    assert len(manager.get_messages()) == 1
    assert manager.get_messages()[0]["id"] == msg_id2
```

## Success Criteria

- [ ] Users can search memory with keyword queries
- [ ] Users can filter by date range and role
- [ ] Users can ask agent to recall facts from past conversations
- [ ] Users can update specific messages
- [ ] Users can delete specific messages
- [ ] Agent offers to correct mistakes when user points them out
- [ ] All messages have unique IDs and timestamps
- [ ] Search results include context (surrounding messages)
- [ ] API endpoints work correctly
- [ ] All unit tests pass (10+ tests)
- [ ] Manual testing scenarios work as expected
- [ ] Backward compatible with existing memory files

## Documentation Updates

- [ ] Update `README.md` with memory search examples
- [ ] Update `docs/LOCAL_AI_AGENT.md` with memory operations section
- [ ] Create `docs/MEMORY_OPERATIONS.md` with detailed guide
- [ ] Update API documentation with new endpoints

## Estimated Effort Breakdown

- MemoryManager enhancements: 3-4 hours
- Agent command handlers: 2-3 hours
- System prompt updates: 1 hour
- API endpoints: 2-3 hours
- Unit tests: 2-3 hours
- Documentation: 1-2 hours
- **Total: 8-12 hours**

## Related Issues

- #23 - Parent issue (Intelligent Agent Memory Management)
- Phase 1 - Auto-Verification (prerequisite)

