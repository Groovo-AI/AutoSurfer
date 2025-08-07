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

        launch_options = {
            "headless": settings.headless,
            "args": browser_args
        }

        if settings.user_data_dir:
            launch_options["user_data_dir"] = settings.user_data_dir

        self.browser: Browser = self.playwright.chromium.launch(
            **launch_options)

        self.setup_browser()
        logger.info('[Playwright Adapter]: Initialized')

    def close(self):
        super().close()
        if self.playwright:
            self.playwright.stop()
