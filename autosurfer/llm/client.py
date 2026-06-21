from langchain_openai import ChatOpenAI
from autosurfer.config import Config
from autosurfer.llm.response_schema.browser_actions import NextActions
from autosurfer.llm.claude_provider import get_claude_client
from langchain_core.utils import get_from_env


def get_llm_client(client=None):
    if client is None:
        client = getattr(Config, "LLM_PROVIDER", "openai")

    if client == "openai":
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        openai_model = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
        )
        return openai_model.with_structured_output(NextActions)
    elif client in ["anthropic", "claude"]:
        return get_claude_client()
    else:
        raise ValueError(f"Unsupported LLM client: {client}")
