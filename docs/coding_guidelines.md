# 🎯 AutoSurfer Coding Guidelines

## Writing Code That Fits the Existing Architecture

### 📋 Core Principles

1. **Follow Existing Patterns**: Study the current codebase and match its style exactly
2. **No Buzzwords**: Use clear, descriptive names that explain purpose
3. **Minimal Dependencies**: Don't add unnecessary libraries
4. **Simple Solutions**: Prefer straightforward implementations over complex abstractions
5. **Consistent Structure**: Match the existing file organization and naming conventions

---

## 🏗️ Architecture Patterns

### File Organization

```
autosurfer/
├── agent/
│   ├── brain/           # Decision making and memory
│   └── browser/         # Browser interaction
├── llm/                 # LLM integration
└── config.py           # Configuration
```

### Class Naming

- **Use descriptive names**: `BrowserActionExecutor`, `CaptchaHandler`, `LoopDetector`
- **Avoid buzzwords**: No "Manager", "Service", "Factory" unless they exist
- **Match existing patterns**: If it's a handler, use "Handler" suffix

### Function Naming

- **Use verb-noun format**: `extract_page_content`, `handle_captcha_detection`
- **Private methods with underscore**: `_log_memory_entry`, `_wait_for_scroll_idle`
- **Clear purpose**: Names should explain what the function does

---

## 📝 Code Style Patterns

### Imports

```python
# Standard library first
import time
from typing import List, Dict, Any, Optional
from pathlib import Path

# Third-party libraries
from playwright.sync_api import Page, Browser, TimeoutError

# Local imports (relative to autosurfer package)
from autosurfer.logger import logger
from autosurfer.agent.brain.memory import AgentMemory, MemoryEntry
```

### Class Structure

```python
class ExampleHandler:
    def __init__(self, page: Page):
        self.page = page
        self._cache = {}  # Private attributes with underscore

    def public_method(self, param: str) -> bool:
        """Clear docstring explaining what this does"""
        # Implementation
        return True

    def _private_method(self) -> None:
        """Private methods for internal use"""
        pass
```

### Error Handling

```python
try:
    # Action that might fail
    self.page.click(selector)
except Exception as e:
    logger.error(f"Failed to click {selector}: {e}")
    raise  # Re-raise to let caller handle
```

### Logging

```python
# Use emojis and descriptive messages
logger.info(f"🎯 Objective: {objective}")
logger.warn(f"❌ Attempt {attempt} failed: {error}")
logger.debug(f"Processing element: {element}")
```

---

## 🔧 Implementation Patterns

### Data Classes

```python
@dataclass
class ExampleEntry:
    """Single entry for tracking something"""
    timestamp: float
    action_type: str
    description: str
    success: bool
    # Optional fields with defaults
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
```

### Action Dispatching

```python
class ActionExecutor:
    def __init__(self):
        self._dispatch = {
            "action1": self._handle_action1,
            "action2": self._handle_action2,
        }

    def execute(self, action):
        fn = self._dispatch.get(action.type)
        if not fn:
            logger.warn(f"Unknown action type: {action.type}")
            return
        fn(action)
```

### Memory Integration

```python
def add_to_memory(self, entry: MemoryEntry):
    """Add entry to memory system"""
    if self.memory:
        self.memory.add_entry(entry)
        # Save immediately
        try:
            self.memory.save_to_file()
        except Exception as e:
            logger.debug(f"Failed to save memory: {e}")
```

### Page Context

```python
page_context = {
    "url": self.page.url,
    "title": self.page.title(),
    "timestamp": time.time(),
    "retry_count": retry_count,
    "consecutive_failures": consecutive_failures
}
```

---

## 🚫 What NOT to Do

### Don't Add Unnecessary Dependencies

```python
# ❌ DON'T add heavy ML libraries unless absolutely necessary
# from transformers import pipeline
# from sklearn.cluster import KMeans

# ✅ DO use simple, existing patterns
import hashlib
import json
import time
```

### Don't Use Buzzword Names

```python
# ❌ DON'T use buzzwords
class ContentAnalysisManager:
class TaskOrchestrationService:
class IntelligentDecisionEngine:

# ✅ DO use clear, descriptive names
class ContentExtractor:
class TaskPlanner:
class DecisionMaker:
```

### Don't Over-Engineer

```python
# ❌ DON'T create complex abstractions
class AbstractContentProcessor:
    def process(self, content: AbstractContent) -> ProcessedResult:
        pass

# ✅ DO use simple, direct approaches
def extract_text_content(page) -> str:
    return page.evaluate("() => document.body.innerText")
```

### Don't Hardcode Values

```python
# ❌ DON'T hardcode magic numbers
if len(entries) > 10:
    return True

# ✅ DO use configuration or clear constants
MAX_ACTIONS_WITHOUT_MEMORY = 10
if len(entries) > MAX_ACTIONS_WITHOUT_MEMORY:
    return True
```

---

## ✅ What TO Do

### Follow Existing Patterns

```python
# ✅ DO match existing class structure
class PageContentExtractor:
    def __init__(self, page: Page):
        self.page = page

    def extract_content(self) -> Dict[str, Any]:
        """Extract all content from current page"""
        try:
            content = self.page.evaluate("() => document.body.innerText")
            return {"text": content, "url": self.page.url}
        except Exception as e:
            logger.error(f"Failed to extract content: {e}")
            return {"text": "", "url": self.page.url}
```

### Use Simple Data Structures

```python
# ✅ DO use simple dicts and lists
content_data = {
    "headings": ["h1", "h2", "h3"],
    "paragraphs": ["p1", "p2"],
    "links": ["link1", "link2"]
}

# ✅ DO use existing patterns for complex data
@dataclass
class ContentSummary:
    title: str
    main_content: str
    links: List[str]
    timestamp: float
```

### Integrate with Existing Systems

```python
# ✅ DO integrate with memory system
def log_content_extraction(self, content: str, success: bool):
    entry = MemoryEntry(
        timestamp=time.time(),
        action_type="content_extraction",
        description=f"Extracted {len(content)} characters",
        success=success,
        page_url=self.page.url,
        page_title=self.page.title()
    )
    self.memory.add_entry(entry)
```

---

## 🎯 Specific Guidelines for AutoSurfer

### Content Extraction

- Use `page.evaluate()` for JavaScript execution
- Extract text content, not HTML structure
- Handle errors gracefully with fallbacks
- Log extraction attempts and results

### Loop Detection

- Use existing `LoopDetector` patterns
- Add semantic analysis, not just fingerprints
- Track progress, not just repetition
- Provide clear exit conditions

### Task Completion

- Enhance existing `DoneAction` with output
- Generate summaries based on extracted content
- Store results in memory for retrieval
- Provide structured output, not just logs

### Error Recovery

- Use existing retry patterns
- Add context-aware error handling
- Provide fallback strategies
- Don't create complex error hierarchies

---

## 📋 Checklist for New Code

Before writing any code, ensure:

- [ ] **Matches existing patterns** in similar files
- [ ] **Uses descriptive names** (no buzzwords)
- [ ] **Integrates with memory system** if needed
- [ ] **Handles errors gracefully** with proper logging
- [ ] **Uses simple data structures** (dicts, lists, dataclasses)
- [ ] **Follows existing import patterns**
- [ ] **Uses existing configuration** where possible
- [ ] **Adds minimal dependencies** (prefer standard library)
- [ ] **Includes proper logging** with emojis
- [ ] **Has clear docstrings** explaining purpose

---

## 🔍 Code Review Questions

When reviewing code, ask:

1. **Does this match existing patterns?** Look at similar files
2. **Are the names clear and descriptive?** No buzzwords
3. **Is this the simplest solution?** Avoid over-engineering
4. **Does it integrate properly?** Use existing systems
5. **Are errors handled?** Graceful failure with logging
6. **Is it testable?** Simple, focused functions
7. **Does it add unnecessary complexity?** Prefer simple solutions

---

## 🎯 End Goal

The goal is to enhance AutoSurfer's intelligence while maintaining its clean, simple architecture. Focus on:

1. **Better content extraction** and analysis
2. **Smarter loop detection** with semantic understanding
3. **Meaningful task completion** with output generation
4. **Improved error recovery** with context awareness
5. **Enhanced decision making** based on page content

All while keeping the code simple, maintainable, and consistent with the existing codebase.
