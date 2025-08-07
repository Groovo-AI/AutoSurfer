from typing import Optional
from .base import BrowserAdapter, BrowserSettings
from .playwright_adapter import PlaywrightAdapter
from .browserbase_adapter import BrowserBaseAdapter
from .camoufox_adapter import CamoufoxAdapter


def create_browser_adapter(provider: str = "playwright", settings: Optional[BrowserSettings] = None) -> BrowserAdapter:
    """Create browser adapter based on provider"""
    settings = settings or BrowserSettings()

    adapters = {
        "playwright": PlaywrightAdapter,
        "browserbase": BrowserBaseAdapter,
        "camoufox": CamoufoxAdapter
    }

    adapter_class = adapters.get(provider, PlaywrightAdapter)
    return adapter_class(settings)
