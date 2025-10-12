# Agent Memory Management Enhancement

## Overview

The AI agent currently has basic memory persistence but lacks advanced memory management capabilities. As conversations grow, the agent will hit token limits, lose context, and become inefficient. We need intelligent memory management with optimization, search, and update capabilities.

## Current State

### What Works ✅
- Basic memory persistence to `memory.json`
- Load/save memory on startup/shutdown
- Clear all memory via API endpoint
- Memory included in OpenAI API calls

### What's Missing ❌

#### 1. Memory Optimization & Token Management
- ❌ No token counting or limit enforcement
- ❌ Memory grows indefinitely until hitting OpenAI limits
- ❌ No automatic pruning of old/irrelevant messages
- ❌ No summarization of long conversations
- ❌ No compression of verbose command outputs

#### 2. Memory Search & Retrieval
- ❌ Can't search past conversations
- ❌ Can't retrieve specific information from history
- ❌ No semantic search capabilities
- ❌ No filtering by date, topic, or command type

#### 3. Memory Categorization & Metadata
- ❌ All messages treated equally (no importance ranking)
- ❌ No tagging or categorization
- ❌ No distinction between commands, results, and conversations
- ❌ No metadata (timestamps, tokens used, cost, etc.)

#### 4. Memory Update & Correction
- ❌ Can't edit or correct mistakes in memory
- ❌ Can't update outdated information
- ❌ Only options are append or clear all
- ❌ No selective deletion

#### 5. Memory Insights & Analytics
- ❌ No conversation pattern analysis
- ❌ No memory usage statistics
- ❌ No cost tracking (OpenAI API usage)
- ❌ No performance metrics

## Proposed Solutions

### Phase 1: Token Management & Optimization (Critical)

**Problem**: Agent will hit OpenAI context limits (8k-128k tokens depending on model)

**Solution**: Implement intelligent memory management

```python
class MemoryManager:
    def __init__(self, memory_file: str, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self.token_counter = TokenCounter()  # Use tiktoken
        
    def optimize_memory(self):
        """Optimize memory to stay within token limits."""
        current_tokens = self.count_tokens()
        
        if current_tokens > self.max_tokens * 0.8:  # 80% threshold
            # Strategy 1: Summarize old conversations
            self.summarize_old_messages()
            
            # Strategy 2: Remove redundant command outputs
            self.compress_command_outputs()
            
            # Strategy 3: Keep only recent + important messages
            self.prune_low_priority_messages()
```

**Features**:
- Token counting using `tiktoken` library
- Automatic summarization when approaching limits
- Configurable token limits per model
- Preserve system prompt and recent context
- Compress verbose command outputs

**Implementation Tasks**:
- [ ] Add `tiktoken` dependency
- [ ] Implement token counting
- [ ] Create summarization logic (use OpenAI API)
- [ ] Add automatic optimization triggers
- [ ] Add manual optimization command

### Phase 2: Memory Search & Retrieval

**Problem**: Can't find information from past conversations

**Solution**: Add search and retrieval capabilities

```python
class MemoryManager:
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search memory for relevant messages."""
        # Option 1: Simple keyword search
        # Option 2: Semantic search using embeddings
        
    def get_by_date_range(self, start: str, end: str) -> List[Dict]:
        """Get messages within date range."""
        
    def get_by_type(self, msg_type: str) -> List[Dict]:
        """Get messages by type (command, result, conversation)."""
```

**Features**:
- Keyword search in memory
- Semantic search using OpenAI embeddings
- Filter by date, type, or tags
- Export search results

**Implementation Tasks**:
- [ ] Add message metadata (timestamp, type, tags)
- [ ] Implement keyword search
- [ ] Add semantic search with embeddings
- [ ] Create search API endpoints
- [ ] Add search UI in web interface

### Phase 3: Memory Update & Correction

**Problem**: Can't fix mistakes or update outdated information

**Solution**: Add edit and update capabilities

```python
class MemoryManager:
    def update_message(self, index: int, new_content: str):
        """Update a specific message."""
        
    def delete_message(self, index: int):
        """Delete a specific message."""
        
    def delete_range(self, start: int, end: int):
        """Delete a range of messages."""
        
    def replace_in_memory(self, old: str, new: str):
        """Find and replace text in memory."""
```

**Features**:
- Edit individual messages
- Delete specific messages or ranges
- Find and replace across memory
- Undo/redo functionality
- Memory versioning/backups

**Implementation Tasks**:
- [ ] Add message IDs for tracking
- [ ] Implement update operations
- [ ] Add delete operations
- [ ] Create memory backup system
- [ ] Add undo/redo functionality

### Phase 4: Memory Categorization & Metadata

**Problem**: All messages treated equally, no context

**Solution**: Add rich metadata and categorization

```python
class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
        self.timestamp = datetime.now()
        self.tokens = count_tokens(content)
        self.type = self._classify_type()  # command, result, conversation
        self.importance = self._calculate_importance()  # 1-10
        self.tags = []
        self.cost = self._calculate_cost()  # API cost
```

**Features**:
- Automatic message classification
- Importance scoring
- Tagging system
- Cost tracking
- Token usage per message

**Implementation Tasks**:
- [ ] Create Message class with metadata
- [ ] Implement automatic classification
- [ ] Add importance scoring algorithm
- [ ] Add tagging system
- [ ] Track API costs

### Phase 5: Memory Insights & Analytics

**Problem**: No visibility into memory usage and patterns

**Solution**: Add analytics and insights

```python
class MemoryAnalytics:
    def get_statistics(self) -> Dict:
        """Get memory usage statistics."""
        return {
            "total_messages": len(self.memory),
            "total_tokens": self.count_tokens(),
            "total_cost": self.calculate_total_cost(),
            "commands_executed": self.count_commands(),
            "success_rate": self.calculate_success_rate(),
            "most_used_commands": self.get_top_commands(),
            "conversation_topics": self.extract_topics()
        }
```

**Features**:
- Memory usage dashboard
- Token usage over time
- Cost tracking and projections
- Command success rates
- Topic analysis
- Export analytics reports

**Implementation Tasks**:
- [ ] Create analytics module
- [ ] Add statistics calculations
- [ ] Create analytics API endpoints
- [ ] Build analytics dashboard UI
- [ ] Add export functionality

## Implementation Priority

### High Priority (Phase 1) 🔴
**Token Management & Optimization** - Critical to prevent hitting context limits

### Medium Priority (Phase 2 & 3) 🟡
**Search & Update** - Important for usability and accuracy

### Low Priority (Phase 4 & 5) 🟢
**Metadata & Analytics** - Nice to have, improves experience

## Technical Considerations

### Dependencies
- `tiktoken` - Token counting for OpenAI models
- `numpy` - For embeddings and semantic search
- `scikit-learn` - For clustering and topic analysis (optional)

### Storage
- Current: Single `memory.json` file
- Proposed: 
  - Keep JSON for compatibility
  - Add SQLite for advanced queries (optional)
  - Add vector database for semantic search (optional)

### API Changes
New endpoints needed:
- `POST /api/agent/memory/optimize` - Trigger memory optimization
- `GET /api/agent/memory/search?q=query` - Search memory
- `PUT /api/agent/memory/{id}` - Update message
- `DELETE /api/agent/memory/{id}` - Delete message
- `GET /api/agent/memory/stats` - Get statistics

### Backward Compatibility
- Maintain existing `memory.json` format
- Add migration script for new features
- Graceful degradation if features unavailable

## Success Criteria

- [ ] Agent can handle conversations > 10k tokens without losing context
- [ ] Memory automatically optimizes when approaching limits
- [ ] Users can search past conversations
- [ ] Users can edit/delete specific messages
- [ ] Memory usage and costs are visible
- [ ] All existing functionality continues to work

## Related Issues

- #8 - Local AI Agent (original implementation)
- #12 - AI Agent Web Integration
- #17 - CRUD Scripts
- #19 - Resume Duplication

## Estimated Effort

- Phase 1: 8-12 hours
- Phase 2: 6-8 hours
- Phase 3: 4-6 hours
- Phase 4: 6-8 hours
- Phase 5: 8-10 hours
- **Total: 32-44 hours**

## Notes

- Start with Phase 1 (token management) as it's critical
- Consider using existing libraries (langchain, llama-index) for memory management
- Test with different OpenAI models (gpt-3.5, gpt-4, gpt-4-turbo)
- Monitor API costs during development

