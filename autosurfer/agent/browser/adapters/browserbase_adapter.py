from autosurfer.logger import logger
from autosurfer.config import Config
from .base import BaseBrowserAdapter, BrowserSettings


class BrowserBaseAdapter(BaseBrowserAdapter):
    """BrowserBase adapter"""

    def __init__(self, settings: BrowserSettings):
        super().__init__(settings)

        try:
            from browserbase import Client

            # Use environment variables for authentication
            api_key = Config.BROWSERBASE_API_KEY
            project_token = Config.BROWSERBASE_PROJECT_TOKEN

            if not api_key:
                raise ValueError(
                    "BROWSERBASE_API_KEY environment variable is required")

            client = Client(api_key=api_key, project_token=project_token)
            self.browser = client.browser()

            self.setup_browser()
            logger.info(f'[BrowserBase Adapter]: Initialized')

        except ImportError:
            logger.error(
                "BrowserBase not installed. Install with: pip install browserbase")
            raise
        except ValueError as e:
            logger.error(f"BrowserBase configuration error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error initializing BrowserBase: {e}")
            raise

    def close(self):
        super().close()
