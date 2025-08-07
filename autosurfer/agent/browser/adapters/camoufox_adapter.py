from autosurfer.logger import logger
from .base import BaseBrowserAdapter, BrowserSettings


class CamoufoxAdapter(BaseBrowserAdapter):
    """Camoufox browser adapter using the official camoufox Python library"""

    def __init__(self, settings: BrowserSettings):
        super().__init__(settings)

        try:
            from camoufox.sync_api import Camoufox

            # Create Camoufox browser instance with minimal settings
            self.camoufox = Camoufox(headless=False)

            # Start Camoufox to initialize the browser
            self.camoufox.start()

            # Get the browser from Camoufox
            self.browser = self.camoufox.browser

            # Create context and page
            self.context = self.browser.new_context()
            self.page = self.context.new_page()

            # Apply base class settings
            self._apply_settings_to_page()

            logger.info('[Camoufox Adapter]: Initialized')

        except ImportError:
            logger.error(
                "Camoufox not installed. Install with: pip install camoufox")
            raise
        except Exception as e:
            logger.error(f"Error initializing Camoufox: {e}")
            raise

    def close(self):
        """Close browser resources"""
        super().close()

        if hasattr(self, 'browser') and self.browser:
            self.browser.close()
