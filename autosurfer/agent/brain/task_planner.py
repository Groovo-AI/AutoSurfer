from autosurfer.llm.client import get_llm_client
from langchain_core.messages import SystemMessage, HumanMessage
from autosurfer.llm.response_schema.browser_actions import NextActions
from autosurfer.llm.prompts import SYSTEM_PROMPT
from autosurfer.agent.brain.memory import AgentMemory
from typing import Dict, Any, Optional

llm = get_llm_client("gemini")


def next_action(objective: str, ui_elements: list, memory: Optional[AgentMemory] = None, page_context: Optional[Dict[str, Any]] = None) -> NextActions:
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

    # Include memory context
    memory_context = ""
    action_history = ""

    if memory:
        memory_context = memory.get_progress_context()
        action_history = memory.get_action_history()

        # Add accomplishments and failures if any
        accomplishments = memory.get_accomplishments_summary()
        failures = memory.get_failures_summary()

        if accomplishments != "No accomplishments yet":
            memory_context += f"\n{accomplishments}"

        if failures != "No failures yet":
            memory_context += f"\n{failures}"

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=[
                {"type": "text", "text": f"Objective: {objective}"},
                {"type": "text", "text": f"Memory Context:\n{memory_context}"},
                {"type": "text", "text": f"Page Context:\n{context_text}"},
                {"type": "text", "text": f"Available UI Elements:\n" +
                    "\n".join(formatted_elements)},
                {"type": "text", "text": action_history}
            ]
        )
    ]

    response = llm.invoke(messages)
    return response
