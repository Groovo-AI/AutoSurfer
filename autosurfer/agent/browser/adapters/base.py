from dataclasses import dataclass
from typing import List, Optional, Protocol, Any
from pathlib import Path
from autosurfer.logger import logger


@dataclass
class BrowserSettings:
    headless: bool = False
    stealth_mode: bool = False
    args: Optional[List[str]] = None


class BrowserAdapter(Protocol):
    """Protocol for browser adapters"""
    page: Any
    context: Any
    browser: Any

    def close(self) -> None:
        ...


class BaseBrowserAdapter:
    """Base class for browser adapters"""

    def __init__(self, settings: BrowserSettings):
        self.settings = settings
        self.browser = None
        self.context = None
        self.page = None

        # Load JS code once
        js_path = Path(__file__).parent.parent / "dom" / "annotateDom.js"
        self.js_code = js_path.read_text() if js_path.exists() else ""

    def setup_browser(self):
        """Setup browser, context, and page with common settings"""
        self.context = self.browser.new_context(
            viewport=None,
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        if self.js_code:
            self.context.add_init_script(self.js_code)

        self.page = self.context.new_page()
        self.page.set_default_timeout(30000)
        self.page.set_default_navigation_timeout(30000)

        if self.settings.stealth_mode:
            try:
                from playwright_stealth.stealth import Stealth
                Stealth().apply_stealth_sync(page_or_context=self.page)
            except ImportError:
                logger.warn(
                    "playwright-stealth not installed, stealth mode disabled")

    def close(self):
        """Close browser resources"""
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
