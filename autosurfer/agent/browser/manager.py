# Re-export from adapters module for backward compatibility
from .adapters import (
    BrowserAdapter,
    BrowserSettings,
    PlaywrightAdapter,
    BrowserBaseAdapter,
    create_browser_adapter
)

__all__ = [
    'BrowserAdapter',
    'BrowserSettings',
    'PlaywrightAdapter',
    'BrowserBaseAdapter',
    'create_browser_adapter'
]
