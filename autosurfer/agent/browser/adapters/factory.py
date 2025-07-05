from typing import Optional
from .base import BrowserAdapter, BrowserSettings
from .playwright_adapter import PlaywrightAdapter
from .browserbase_adapter import BrowserBaseAdapter


def create_browser_adapter(provider: str = "playwright", settings: Optional[BrowserSettings] = None) -> BrowserAdapter:
    """Create browser adapter based on provider"""
    settings = settings or BrowserSettings()

    adapters = {
        "playwright": PlaywrightAdapter,
        "browserbase": BrowserBaseAdapter
    }

    adapter_class = adapters.get(provider, PlaywrightAdapter)
    return adapter_class(settings)
