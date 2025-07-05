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

    context_text = "\n".join(
        context_info) if context_info else "No additional context"

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=[
                {"type": "text", "text": f"Objective: {objective}"},
                {"type": "text", "text": f"Page Context:\n{context_text}"},
                {"type": "text", "text": f"Available UI Elements:\n{ui_elements}"}
            ]
        )
    ]

    return llm.invoke(messages)
