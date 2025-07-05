from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class MemoryEntry:
    """Single memory entry for an action/event"""
    timestamp: float
    action_type: str
    description: str
    success: bool
    page_url: str
    page_title: str
    attempts: int = 1
    error_message: Optional[str] = None
    ui_elements_count: Optional[int] = None


@dataclass
class AgentMemory:
    """Agent memory system to track progress and accomplishments"""
    objective: str
    start_time: float = field(
        default_factory=lambda: datetime.now().timestamp())
    entries: List[MemoryEntry] = field(default_factory=list)
    accomplishments: List[str] = field(default_factory=list)
    failures: List[str] = field(default_factory=list)
    current_progress: str = "Starting task"

    def add_entry(self, entry: MemoryEntry):
        """Add a new memory entry"""
        self.entries.append(entry)

        # Update progress based on action type
        if entry.success:
            if entry.action_type == "done":
                self.current_progress = f"Task completed: {entry.description}"
                self.accomplishments.append(entry.description)
            elif entry.action_type == "goto":
                self.current_progress = f"Navigated to: {entry.page_title or entry.page_url}"
            elif entry.action_type == "click":
                self.current_progress = f"Clicked: {entry.description}"
            elif entry.action_type == "fill":
                self.current_progress = f"Filled form: {entry.description}"
        else:
            self.failures.append(
                f"{entry.action_type}: {entry.error_message or 'Unknown error'}")

    def get_recent_entries(self, count: int = 5) -> List[MemoryEntry]:
        """Get the most recent memory entries"""
        return self.entries[-count:] if self.entries else []

    def get_accomplishments_summary(self) -> str:
        """Get a summary of what has been accomplished"""
        if not self.accomplishments:
            return "No accomplishments yet"

        summary = "Accomplishments:\n"
        # Last 5 accomplishments
        for i, acc in enumerate(self.accomplishments[-5:], 1):
            summary += f"  {i}. {acc}\n"
        return summary

    def get_failures_summary(self) -> str:
        """Get a summary of recent failures"""
        if not self.failures:
            return "No failures yet"

        summary = "Recent failures:\n"
        for i, failure in enumerate(self.failures[-3:], 1):  # Last 3 failures
            summary += f"  {i}. {failure}\n"
        return summary

    def get_progress_context(self) -> str:
        """Get context about current progress for the LLM"""
        context = f"Objective: {self.objective}\n"
        context += f"Current Progress: {self.current_progress}\n"
        context += f"Total Actions: {len(self.entries)}\n"

        if self.accomplishments:
            context += f"Accomplishments: {len(self.accomplishments)}\n"

        if self.failures:
            context += f"Recent Failures: {len(self.failures)}\n"

        return context

    def get_action_history(self) -> str:
        """Get formatted action history for the LLM"""
        if not self.entries:
            return "No previous actions"

        history = "Recent Actions:\n"
        recent_entries = self.get_recent_entries(3)

        for i, entry in enumerate(recent_entries, 1):
            status = "✅" if entry.success else "❌"
            history += f"  {i}. {status} {entry.action_type}: {entry.description}\n"
            if not entry.success and entry.error_message:
                history += f"     Error: {entry.error_message}\n"

        return history

    def is_stuck(self) -> bool:
        """Check if agent might be stuck in a loop"""
        if len(self.entries) < 5:
            return False

        # Check for repeated failures
        recent_failures = sum(
            1 for entry in self.entries[-5:] if not entry.success)
        if recent_failures >= 4:
            return True

        # Check for repeated actions
        recent_actions = [entry.action_type for entry in self.entries[-5:]]
        if len(set(recent_actions)) <= 2:
            return True

        return False
