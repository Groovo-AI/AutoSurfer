from typing import Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from autosurfer.config import Config
from autosurfer.llm.prompts import SYSTEM_PROMPT_BROWSER
from autosurfer.llm.response_schema.browser_actions import NextActions
from typing import List, Dict, Any


def ask_step(
    objective: str,
    last_action: Optional[str] = None,
) -> List[Dict[str, Any]]:
    # Instantiate base model
    base_model = ChatOpenAI(
        model="gpt-4o",
        # temperature=0,
        openai_api_key=Config.OPENAI_API_KEY,
    )
    """Ask the LLM for the next 1–2 browser steps"""
    llm = base_model.with_structured_output(NextActions)

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT_BROWSER.format(
                operating_system=Config.OS,
                screen_size=f"{Config.LOGICAL_SCREEN_WIDTH}×{Config.LOGICAL_SCREEN_HEIGHT}"
            )
        ),
        HumanMessage(
            content=[
                {"type": "text", "text": f"Objective: {objective}"},
                {"type": "text", "text": f"Last Action: {last_action or ''}"},
            ]
        ),
    ]

    response: NextActions = llm.invoke(messages)
    return [item.model_dump() for item in response.actions]
