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

    # BrowserBase configuration
    BROWSERBASE_API_KEY = os.getenv("BROWSERBASE_API_KEY")
    BROWSERBASE_PROJECT_ID = os.getenv("BROWSERBASE_PROJECT_ID")
