import platform
import os


class Config:
    OS_PLATFORM = platform.system()

    if OS_PLATFORM == "Darwin":
        OS = "mac"
    elif OS_PLATFORM == "linux":
        OS = "linux"
    elif OS_PLATFORM == "Windows":
        OS = "windows"
    else:
        OS = "unknown"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Gemini configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Claude configuration
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    
    # LLM Provider configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai") # Default to openai
    
    # DeepSeek configuration
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    
    # BrowserBase configuration
    BROWSERBASE_API_KEY = os.getenv("BROWSERBASE_API_KEY")
    BROWSERBASE_PROJECT_ID = os.getenv("BROWSERBASE_PROJECT_ID")
