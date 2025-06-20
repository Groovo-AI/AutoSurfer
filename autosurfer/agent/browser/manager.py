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
        self.browser: Browser = self.playwright.chromium.launch(
            headless=settings.headless, args=["--start-maximized"].append(self.settings.args))
        self.context = self.browser.new_context(viewport=None)
        if JS_CODE:
            self.context.add_init_script(JS_CODE)
        self.page = self.context.new_page()

        if settings.stealth_mode:
            Stealth().apply_stealth_sync(page_or_context=self.page)
        logger.info(f'[Browser Settings]: {self.settings}')

    def close(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
