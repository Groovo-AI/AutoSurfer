from autosurfer.logger import logger
from playwright.sync_api import sync_playwright
from typing import Optional


class AutoSurferAgent:
    def __init__(self):
        self.objective: Optional[str] = None
        self.last_action: Optional[str] = None
        self.playwright = None
        self.browser = None
        self.page = None

    def launch_browser(self):
        logger.debug("Launching Playwright browser")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False, args=["--start-maximized"]
        )
        context = self.browser.new_context(viewport=None)
        self.page = context.new_page()

    def run(self, objective: str):
        self.objective = objective
        self.launch_browser()
        self.page.goto("https://instagram.com")
        logger.info(f"🎯 Objective: {self.objective}")
