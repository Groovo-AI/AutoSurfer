from langchain_openai import ChatOpenAI
from autosurfer.config import Config
from autosurfer.llm.response_schema.browser_actions import NextActions
from langchain_core.utils import get_from_env
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic


def get_llm_client():
    llm_provider = Config.LLM_PROVIDER.lower()
    
    if llm_provider == "openai":
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI")
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
        )
    elif llm_provider == "gemini":
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required for Gemini")
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0,
        )
    elif llm_provider == "claude":
        if not Config.CLAUDE_API_KEY:
            raise ValueError("CLAUDE_API_KEY environment variable is required for Claude")
        llm = ChatAnthropic(
            model="claude-3-opus-20240229", # Or another suitable Claude model
            temperature=0,
        )
    elif llm_provider == "deepseek":
        if not Config.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY environment variable is required for DeepSeek")
        llm = ChatOpenAI(
            model="deepseek-chat",
            temperature=0,
            openai_api_base="https://api.deepseek.com"
        )
    else:
        raise ValueError(f"Unsupported LLM client: {llm_provider}")
        
    return llm.with_structured_output(NextActions)
