from playwright.sync_api import sync_playwright, Playwright, Browser
from autosurfer.logger import logger
from .base import BaseBrowserAdapter, BrowserSettings


class PlaywrightAdapter(BaseBrowserAdapter):
    """Playwright browser adapter"""

    def __init__(self, settings: BrowserSettings):
        super().__init__(settings)

        self.playwright: Playwright = sync_playwright().start()

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

        self.setup_browser()
        logger.info('[Playwright Adapter]: Initialized')

    def close(self):
        super().close()
        if self.playwright:
            self.playwright.stop()
