from langchain_openai import ChatOpenAI
from autosurfer.config import Config
from autosurfer.llm.response_schema.browser_actions import NextActions


def get_llm_client(client):
    if client == "openai":
        openai_model = ChatOpenAI(
            model="gpt-4o",
            # temperature=0,
            openai_api_key=Config.OPENAI_API_KEY,
        )
        return openai_model.with_structured_output(NextActions)
