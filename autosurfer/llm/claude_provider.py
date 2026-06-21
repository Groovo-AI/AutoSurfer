from langchain_anthropic import ChatAnthropic
from autosurfer.config import Config
from autosurfer.llm.response_schema.browser_actions import NextActions

def get_claude_client():
    if not Config.ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    anthropic_model = ChatAnthropic(
        model="claude-3-7-sonnet-20250219",
        temperature=0,
    )
    return anthropic_model.with_structured_output(NextActions)
