from autosurfer.llm.client import get_llm_client
from langchain_core.messages import SystemMessage, HumanMessage
from autosurfer.llm.response_schema.browser_actions import NextActions

llm = get_llm_client("openai")

SYSTEM_PROMPT = (
    "You are a browser‑based AI agent. "
    "Given the objective, a JSON list of UI elements (with indexes), and memory of previous actions, "
    "decide the next 1–2 steps that move toward the goal. "
    "Respond strictly in the requested JSON schema."
)


def next_action(objective, ui_elements, memory=None) -> NextActions:
    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT
        ),
        HumanMessage(
            content=[
                {"type": "text", "text": f"Objective: {objective}"},
                {"type": "text", "text": f"UI Elements:\n{ui_elements}"},
                {"type": "text", "text": f"Memory:\n{memory}"}
            ]
        )

    ]

    response = llm.invoke(messages)
    return response
    # return [item.model_dump() for item in response.actions]
