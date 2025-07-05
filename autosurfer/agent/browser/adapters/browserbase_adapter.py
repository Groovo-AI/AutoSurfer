from autosurfer.logger import logger
from .base import BaseBrowserAdapter, BrowserSettings


class BrowserBaseAdapter(BaseBrowserAdapter):
    """BrowserBase adapter"""

    def __init__(self, settings: BrowserSettings):
        super().__init__(settings)

        try:
            from browserbase import Client

            client = Client()
            self.browser = client.browser()

            self.setup_browser()
            logger.info(f'[BrowserBase Adapter]: Initialized')

        except ImportError:
            logger.error(
                "BrowserBase not installed. Install with: pip install browserbase")
            raise
        except Exception as e:
            logger.error(f"Error initializing BrowserBase: {e}")
            raise

    def close(self):
        super().close()
