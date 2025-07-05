from autosurfer.logger import logger
from autosurfer.config import Config
from playwright.sync_api import sync_playwright
from .base import BaseBrowserAdapter, BrowserSettings


class BrowserBaseAdapter(BaseBrowserAdapter):
    """BrowserBase adapter using Playwright CDP connection"""

    def __init__(self, settings: BrowserSettings):
        super().__init__(settings)

        try:
            from browserbase import Browserbase

            # Validate environment variables
            api_key = Config.BROWSERBASE_API_KEY
            project_id = Config.BROWSERBASE_PROJECT_ID

            if not api_key:
                raise ValueError(
                    "BROWSERBASE_API_KEY environment variable is required")
            if not project_id:
                raise ValueError(
                    "BROWSERBASE_PROJECT_ID environment variable is required")

            # Create BrowserBase session
            self.browserbase = Browserbase(api_key=api_key)
            self.session = self.browserbase.sessions.create(
                project_id=project_id)
            logger.info(
                f'[BrowserBase Adapter]: Session created - {self.session.id}')

            # Connect to remote session
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.connect_over_cdp(
                self.session.connect_url)

            # Use existing context and page
            self.context = self.browser.contexts[0]
            self.page = self.context.pages[0]

            # Apply base class settings to existing page/context
            self._apply_settings_to_page()

            logger.info('[BrowserBase Adapter]: Initialized')

        except ImportError:
            logger.error(
                "BrowserBase not installed. Install with: pip install browserbase")
            raise
        except Exception as e:
            logger.error(f"Error initializing BrowserBase: {e}")
            raise

    def close(self):
        super().close()
        if hasattr(self, 'playwright') and self.playwright:
            self.playwright.stop()
        if hasattr(self, 'session') and self.session:
            logger.info(
                f"Session replay available at: https://browserbase.com/sessions/{self.session.id}")
