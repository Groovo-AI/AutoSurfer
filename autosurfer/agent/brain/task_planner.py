from autosurfer.llm.client import get_llm_client
from langchain_core.messages import SystemMessage, HumanMessage
from autosurfer.llm.response_schema.browser_actions import NextActions
from autosurfer.llm.prompts import SYSTEM_PROMPT
from typing import Dict, Any, Optional

llm = get_llm_client("openai")


def next_action(objective: str, ui_elements: list, memory: Optional[list] = None, page_context: Optional[Dict[str, Any]] = None) -> NextActions:
    context_info = []

    if page_context:
        context_info.append(
            f"Current URL: {page_context.get('url', 'Unknown')}")
        context_info.append(
            f"Page Title: {page_context.get('title', 'Unknown')}")
        if page_context.get('retry_count', 0) > 0:
            context_info.append(
                f"Retry Count: {page_context.get('retry_count')}")
        if page_context.get('consecutive_failures', 0) > 0:
            context_info.append(
                f"Consecutive Failures: {page_context.get('consecutive_failures')}")

    context_text = "\n".join(
        context_info) if context_info else "No additional context"

    # Format UI elements for better readability
    formatted_elements = []
    # Limit to first 20 elements
    for i, element in enumerate(ui_elements[:20]):
        element_info = f"{i}: {element.get('tag', 'unknown')}"
        if element.get('id'):
            element_info += f" id='{element['id']}'"
        if element.get('text'):
            element_info += f" text='{element['text'][:50]}'"
        if element.get('testid'):
            element_info += f" testid='{element['testid']}'"
        formatted_elements.append(element_info)

    # Include recent action history
    action_history = ""
    if memory and len(memory) > 0:
        recent_actions = memory[-3:]  # Last 3 actions
        action_history = "\nRecent Actions:\n"
        for i, mem in enumerate(recent_actions):
            if mem.get('success'):
                action_history += f"  {i+1}. ✅ {mem.get('plan', 'Unknown action')}\n"
            else:
                action_history += f"  {i+1}. ❌ {mem.get('plan', 'Unknown action')} (failed)\n"

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=[
                {"type": "text", "text": f"Objective: {objective}"},
                {"type": "text", "text": f"Page Context:\n{context_text}"},
                {"type": "text", "text": f"Available UI Elements:\n" +
                    "\n".join(formatted_elements)},
                {"type": "text", "text": action_history}
            ]
        )
    ]

    return llm.invoke(messages)
