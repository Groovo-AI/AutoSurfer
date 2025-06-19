from autosurfer.logger import logger
from playwright.sync_api import sync_playwright
from typing import Optional
import os
import time


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

    def annotate_ui_elements(self):
        logger.info("Injecting highlight script")
        path = os.path.join(
            os.path.dirname(__file__),
            "browser", "dom", "annotateDom.js"
        )
        with open(path, "r") as f:
            js_code = f.read()
        self.page.add_init_script(js_code)
        self.page.evaluate(js_code)
        elements = self.page.evaluate(
            "() => window.collectInteractive({ highlight: true })")
        for el in elements:
            logger.debug(
                f"[{el['index']}] {el['tag']}: {el['text']} - {el['xpath']}")
        return elements

    def clear_ui_elements_annotations(self):
        self.page.evaluate("() => window.clearInteractiveHighlights()")

    def run(self, objective: str):
        self.objective = objective
        self.launch_browser()
        self.page.goto("https://instagram.com", wait_until="networkidle")
        logger.info(f"🎯 Objective: {self.objective}")
        elements = self.annotate_ui_elements()
        logger.info(f"🔍 Found {len(elements)} interactive elements")
        time.sleep(10)
        self.clear_ui_elements_annotations()
        # Prevent script from exiting immediately
        logger.info("Browser will remain open. Press CTRL+C to quit.")
        try:
            while True:
                pass  # Infinite loop to keep browser open
        except KeyboardInterrupt:
            logger.info("Exiting without closing browser.")
