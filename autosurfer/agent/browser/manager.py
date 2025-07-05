from playwright.sync_api import sync_playwright, Playwright, Browser
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
from autosurfer.logger import logger
from playwright_stealth.stealth import Stealth


JS_PATH = Path(__file__).parent / "dom" / "annotateDom.js"
JS_CODE = JS_PATH.read_text() if JS_PATH.exists() else ""


@dataclass
class BrowserSettings:
    headless: bool = False
    stealth_mode: bool = False
    args: Optional[List[str]] = None


class BrowserManager:
    def __init__(self, settings: BrowserSettings):
        self.settings = settings
        self.playwright: Playwright = sync_playwright().start()

        # Enhanced browser arguments for better compatibility
        browser_args = [
            "--start-maximized",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor"
        ]
        if settings.args:
            browser_args.extend(settings.args)

        self.browser: Browser = self.playwright.chromium.launch(
            headless=settings.headless,
            args=browser_args
        )

        # Enhanced context settings
        self.context = self.browser.new_context(
            viewport=None,
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        if JS_CODE:
            self.context.add_init_script(JS_CODE)

        self.page = self.context.new_page()

        # Set default timeouts
        self.page.set_default_timeout(30000)
        self.page.set_default_navigation_timeout(30000)

        if settings.stealth_mode:
            Stealth().apply_stealth_sync(page_or_context=self.page)

        logger.info(f'[Browser Settings]: {self.settings}')

    def close(self):
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
