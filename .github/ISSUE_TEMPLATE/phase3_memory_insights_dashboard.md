# Phase 3: Memory Insights Dashboard & Cost Tracking

**Parent Issue**: #23 - Intelligent Agent Memory Management  
**Priority**: 🟢 Medium  
**Estimated Effort**: 10-14 hours

## User Value Delivered

Users will be able to:
1. ✅ **See memory usage dashboard** - Visual representation of memory consumption
2. ✅ **Track API costs** - Know how much each conversation costs
3. ✅ **View conversation analytics** - Most used commands, success rates, patterns
4. ✅ **Get cost projections** - Estimate costs before long conversations
5. ✅ **Export conversation reports** - Save important conversations for reference
6. ✅ **Optimize spending** - Identify expensive operations and optimize

## Problem Statement

Currently:
- ❌ No visibility into memory usage patterns
- ❌ No tracking of API costs (can lead to unexpected bills)
- ❌ Can't see which operations are most expensive
- ❌ No way to export or analyze conversation history
- ❌ Can't identify inefficient usage patterns

## Solution Overview

Combine **metadata enrichment** with **analytics dashboard** to provide comprehensive insights:

### Part A: Rich Metadata
1. Add message classification (command/result/conversation)
2. Track token count per message
3. Calculate cost per message
4. Add importance scoring
5. Add tagging system

### Part B: Analytics Dashboard
1. Memory usage visualization
2. Cost tracking and projections
3. Command usage statistics
4. Success rate analysis
5. Export functionality

## Technical Implementation

### 1. Create Message Class with Rich Metadata

**File**: `src/agent/message.py`
```python
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List, Dict
import tiktoken

@dataclass
class Message:
    """Enhanced message with rich metadata."""
    
    id: str
    role: str
    content: str
    timestamp: str
    message_type: str  # command, result, conversation
    tokens: int
    cost: float
    importance: int  # 1-10
    tags: List[str]
    metadata: Dict
    
    @classmethod
    def create(cls, role: str, content: str, model: str = "gpt-4",
               tags: Optional[List[str]] = None, metadata: Optional[Dict] = None):
        """Create a new message with automatic metadata."""
        import uuid
        
        message_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        message_type = cls._classify_type(role, content)
        tokens = cls._count_tokens(content, model)
        cost = cls._calculate_cost(tokens, model)
        importance = cls._calculate_importance(message_type, content)
        
        return cls(
            id=message_id,
            role=role,
            content=content,
            timestamp=timestamp,
            message_type=message_type,
            tokens=tokens,
            cost=cost,
            importance=importance,
            tags=tags or [],
            metadata=metadata or {}
        )
    
    @staticmethod
    def _classify_type(role: str, content: str) -> str:
        """Classify message type."""
        if role == "system":
            return "system"
        
        # Check for command patterns
        if content.strip().startswith("run:"):
            return "command"
        
        # Check for result patterns
        if any(indicator in content for indicator in ["✅", "❌", "[SUCCESS]", "[ERROR]"]):
            return "result"
        
        return "conversation"
    
    @staticmethod
    def _count_tokens(content: str, model: str) -> int:
        """Count tokens in content."""
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(content))
        except:
            # Fallback: rough estimate
            return len(content) // 4
    
    @staticmethod
    def _calculate_cost(tokens: int, model: str) -> float:
        """Calculate cost based on tokens and model."""
        # Pricing as of Oct 2024 (update as needed)
        pricing = {
            "gpt-3.5-turbo": {"input": 0.0015 / 1000, "output": 0.002 / 1000},
            "gpt-4": {"input": 0.03 / 1000, "output": 0.06 / 1000},
            "gpt-4-turbo": {"input": 0.01 / 1000, "output": 0.03 / 1000},
        }
        
        # Use average of input/output for simplicity
        if model in pricing:
            avg_price = (pricing[model]["input"] + pricing[model]["output"]) / 2
            return tokens * avg_price
        
        return 0.0
    
    @staticmethod
    def _calculate_importance(message_type: str, content: str) -> int:
        """Calculate importance score (1-10)."""
        score = 5  # Default
        
        # Commands are important
        if message_type == "command":
            score = 8
        
        # Results are important
        elif message_type == "result":
            score = 7
        
        # System messages are critical
        elif message_type == "system":
            score = 10
        
        # Adjust based on content length (longer = more important)
        if len(content) > 500:
            score = min(10, score + 1)
        
        # Adjust based on keywords
        important_keywords = ["error", "failed", "success", "created", "updated", "deleted"]
        if any(keyword in content.lower() for keyword in important_keywords):
            score = min(10, score + 1)
        
        return score
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create from dictionary."""
        return cls(**data)
```

### 2. Create Analytics Module

**File**: `src/agent/analytics.py`
```python
from typing import List, Dict
from datetime import datetime, timedelta
from collections import Counter

class MemoryAnalytics:
    """Analyzes memory usage and provides insights."""
    
    def __init__(self, messages: List[Dict]):
        self.messages = messages
    
    def get_overview(self) -> Dict:
        """Get overview statistics."""
        total_messages = len(self.messages)
        total_tokens = sum(m.get("tokens", 0) for m in self.messages)
        total_cost = sum(m.get("cost", 0.0) for m in self.messages)
        
        return {
            "total_messages": total_messages,
            "total_tokens": total_tokens,
            "total_cost": round(total_cost, 4),
            "avg_tokens_per_message": round(total_tokens / total_messages, 2) if total_messages > 0 else 0,
            "avg_cost_per_message": round(total_cost / total_messages, 4) if total_messages > 0 else 0
        }
    
    def get_breakdown_by_type(self) -> Dict:
        """Get breakdown by message type."""
        types = Counter(m.get("message_type", "unknown") for m in self.messages)
        
        breakdown = {}
        for msg_type, count in types.items():
            type_messages = [m for m in self.messages if m.get("message_type") == msg_type]
            breakdown[msg_type] = {
                "count": count,
                "tokens": sum(m.get("tokens", 0) for m in type_messages),
                "cost": round(sum(m.get("cost", 0.0) for m in type_messages), 4)
            }
        
        return breakdown
    
    def get_command_statistics(self) -> Dict:
        """Get statistics about commands executed."""
        commands = [m for m in self.messages if m.get("message_type") == "command"]
        results = [m for m in self.messages if m.get("message_type") == "result"]
        
        # Extract command names
        command_names = []
        for cmd in commands:
            content = cmd.get("content", "")
            if "run:" in content:
                # Extract script name
                import re
                match = re.search(r'python\s+src/(\w+\.py)', content)
                if match:
                    command_names.append(match.group(1))
        
        command_counts = Counter(command_names)
        
        # Calculate success rate
        success_count = sum(1 for r in results if "✅" in r.get("content", ""))
        total_results = len(results)
        success_rate = (success_count / total_results * 100) if total_results > 0 else 0
        
        return {
            "total_commands": len(commands),
            "unique_commands": len(command_counts),
            "most_used": command_counts.most_common(5),
            "success_rate": round(success_rate, 2),
            "successful": success_count,
            "failed": total_results - success_count
        }
    
    def get_timeline(self, days: int = 7) -> Dict:
        """Get timeline of usage over last N days."""
        now = datetime.now()
        timeline = {}
        
        for i in range(days):
            date = (now - timedelta(days=i)).date().isoformat()
            timeline[date] = {
                "messages": 0,
                "tokens": 0,
                "cost": 0.0
            }
        
        for message in self.messages:
            timestamp = message.get("timestamp", "")
            if timestamp:
                date = timestamp.split("T")[0]
                if date in timeline:
                    timeline[date]["messages"] += 1
                    timeline[date]["tokens"] += message.get("tokens", 0)
                    timeline[date]["cost"] += message.get("cost", 0.0)
        
        # Round costs
        for date in timeline:
            timeline[date]["cost"] = round(timeline[date]["cost"], 4)
        
        return timeline
    
    def get_cost_projection(self, days: int = 30) -> Dict:
        """Project costs for next N days based on current usage."""
        timeline = self.get_timeline(days=7)
        
        # Calculate average daily cost
        daily_costs = [data["cost"] for data in timeline.values()]
        avg_daily_cost = sum(daily_costs) / len(daily_costs) if daily_costs else 0
        
        projected_cost = avg_daily_cost * days
        
        return {
            "avg_daily_cost": round(avg_daily_cost, 4),
            "projected_cost": round(projected_cost, 2),
            "projection_days": days,
            "based_on_last_days": 7
        }
    
    def get_top_expensive_messages(self, limit: int = 10) -> List[Dict]:
        """Get most expensive messages."""
        sorted_messages = sorted(
            self.messages,
            key=lambda m: m.get("cost", 0.0),
            reverse=True
        )
        
        return [
            {
                "id": m.get("id"),
                "timestamp": m.get("timestamp"),
                "type": m.get("message_type"),
                "tokens": m.get("tokens"),
                "cost": round(m.get("cost", 0.0), 4),
                "preview": m.get("content", "")[:100]
            }
            for m in sorted_messages[:limit]
        ]
    
    def export_report(self, format: str = "json") -> str:
        """Export analytics report."""
        report = {
            "generated_at": datetime.now().isoformat(),
            "overview": self.get_overview(),
            "breakdown_by_type": self.get_breakdown_by_type(),
            "command_statistics": self.get_command_statistics(),
            "timeline": self.get_timeline(),
            "cost_projection": self.get_cost_projection(),
            "top_expensive": self.get_top_expensive_messages()
        }
        
        if format == "json":
            import json
            return json.dumps(report, indent=2)
        
        # Add other formats (CSV, HTML) as needed
        return str(report)
```

### 3. Add Analytics API Endpoints

**File**: `src/api/app.py`

```python
@app.route('/api/agent/analytics/overview', methods=['GET'])
def get_analytics_overview():
    """Get analytics overview."""
    try:
        memory = get_memory_manager()
        analytics = MemoryAnalytics(memory.get_messages())
        
        return jsonify({
            "success": True,
            "data": analytics.get_overview()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agent/analytics/breakdown', methods=['GET'])
def get_analytics_breakdown():
    """Get breakdown by message type."""
    try:
        memory = get_memory_manager()
        analytics = MemoryAnalytics(memory.get_messages())
        
        return jsonify({
            "success": True,
            "data": analytics.get_breakdown_by_type()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agent/analytics/commands', methods=['GET'])
def get_command_statistics():
    """Get command statistics."""
    try:
        memory = get_memory_manager()
        analytics = MemoryAnalytics(memory.get_messages())
        
        return jsonify({
            "success": True,
            "data": analytics.get_command_statistics()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agent/analytics/timeline', methods=['GET'])
def get_usage_timeline():
    """Get usage timeline."""
    try:
        days = request.args.get('days', 7, type=int)
        memory = get_memory_manager()
        analytics = MemoryAnalytics(memory.get_messages())
        
        return jsonify({
            "success": True,
            "data": analytics.get_timeline(days=days)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agent/analytics/projection', methods=['GET'])
def get_cost_projection():
    """Get cost projection."""
    try:
        days = request.args.get('days', 30, type=int)
        memory = get_memory_manager()
        analytics = MemoryAnalytics(memory.get_messages())
        
        return jsonify({
            "success": True,
            "data": analytics.get_cost_projection(days=days)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agent/analytics/export', methods=['GET'])
def export_analytics():
    """Export analytics report."""
    try:
        format = request.args.get('format', 'json')
        memory = get_memory_manager()
        analytics = MemoryAnalytics(memory.get_messages())
        
        report = analytics.export_report(format=format)
        
        return jsonify({
            "success": True,
            "report": report
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### 4. Create Analytics Dashboard UI

**File**: `src/web/analytics.html`

Create a new analytics dashboard page with:
- Memory usage charts (Chart.js)
- Cost tracking visualization
- Command statistics
- Timeline graphs
- Export functionality

## Testing & Verification

### Manual Testing Scenarios

#### Scenario 1: View Memory Dashboard

**Steps**:
1. Open web interface
2. Navigate to Analytics tab
3. View dashboard

**Expected Output**:
- Total messages: 45
- Total tokens: 12,543
- Total cost: $0.38
- Breakdown by type (pie chart)
- Timeline graph (last 7 days)

#### Scenario 2: Track Command Usage

**Steps**:
1. Execute several commands
2. View command statistics
3. See most used commands

**Expected Output**:
```
Command Statistics:
- Total commands: 15
- Success rate: 93.3%
- Most used:
  1. duplicate_resume.py (5 times)
  2. update_resume_experience.py (4 times)
  3. tailor.py (3 times)
```

#### Scenario 3: Cost Projection

**Steps**:
1. View cost projection
2. See estimated monthly cost

**Expected Output**:
```
Cost Projection (30 days):
- Average daily cost: $0.12
- Projected monthly cost: $3.60
- Based on last 7 days of usage
```

#### Scenario 4: Export Report

**Steps**:
1. Click "Export Report" button
2. Download JSON report
3. Verify contents

**Expected Output**:
JSON file with complete analytics data

## Success Criteria

- [ ] Dashboard shows real-time memory usage
- [ ] Cost tracking is accurate (within 5%)
- [ ] Command statistics show success rates
- [ ] Timeline visualization works
- [ ] Cost projections are reasonable
- [ ] Export functionality works
- [ ] All API endpoints return correct data
- [ ] UI is responsive and user-friendly
- [ ] Charts render correctly
- [ ] All unit tests pass

## Documentation Updates

- [ ] Create `docs/MEMORY_ANALYTICS.md`
- [ ] Update `README.md` with analytics features
- [ ] Add API documentation for analytics endpoints
- [ ] Create user guide for dashboard

## Estimated Effort Breakdown

- Message class with metadata: 2-3 hours
- Analytics module: 3-4 hours
- API endpoints: 2-3 hours
- Dashboard UI: 3-4 hours
- Testing: 2-3 hours
- Documentation: 1-2 hours
- **Total: 10-14 hours**

## Related Issues

- #23 - Parent issue
- Phase 1 - Auto-Verification (prerequisite)
- Phase 2 - Memory Search & Update (prerequisite)

