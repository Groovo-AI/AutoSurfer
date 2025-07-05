from langchain_openai import ChatOpenAI
from autosurfer.config import Config
from autosurfer.llm.response_schema.browser_actions import NextActions
from langchain_core.utils import get_from_env


def get_llm_client(client):
    if client == "openai":
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        openai_model = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
        )
        return openai_model.with_structured_output(NextActions)
    else:
        raise ValueError(f"Unsupported LLM client: {client}")
