from playwright.sync_api import sync_playwright, Page
from typing import List, Dict, Any
from autosurfer.logger import logger
import time


class BrowserActionExecutor:
    def __init__(self, actions: List[Dict[str, Any]], headless: bool = False):
        self.actions = actions
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless, args=["--start-maximized"])
        self.context = self.browser.new_context(viewport=None)
        self.page: Page = self.context.new_page()

    def execute(self) -> None:
        for step in self.actions:
            thought = step.get("thought", "")
            op = step.get("operation")
            logger.info(f"[Agent Thought] {thought}")
            handler = getattr(self, f"_handle_{op}", None)
            if not handler:
                logger.warning(f"No handler for operation: {op}")
                continue
            handler(step)
            if op == "done":
                break

    def _handle_goto(self, action: Dict[str, Any]) -> None:
        url = action.get("url")
        if not url:
            logger.error("goto action missing 'url'")
            return
        logger.info(f"→ Navigating to {url}")
        self.page.goto(url)

    def _handle_click(self, action: Dict[str, Any]) -> None:
        selector = action.get("selector")
        if not selector:
            logger.error("click action missing 'selector'")
            return
        logger.info(f"→ Clicking element '{selector}'")
        self.page.click(selector)

    def _handle_fill(self, action: Dict[str, Any]) -> None:
        selector = action.get("selector")
        value = action.get("value", "")
        if not selector or value is None:
            logger.error("fill action missing 'selector' or 'value'")
            return
        logger.info(f"→ Filling '{selector}' with '{value}'")
        self.page.fill(selector, value)

    def _handle_press(self, action: Dict[str, Any]) -> None:
        key = action.get("value")
        if not key:
            logger.error("press action missing 'value' key")
            return
        logger.info(f"→ Pressing key '{key}'")
        self.page.keyboard.press(key)

    def _handle_wait(self, action: Dict[str, Any]) -> None:
        seconds = float(action.get("value", 0))
        logger.info(f"→ Waiting for {seconds} seconds")
        time.sleep(seconds)

    def _handle_scroll(self, action: Dict[str, Any]) -> None:
        selector = action.get("selector")
        value = action.get("value", "down")
        logger.info(f"→ Scrolling {value} on '{selector or 'page'}'")
        if selector:
            element = self.page.query_selector(selector)
            if element:
                if value == "down":
                    element.scroll_into_view_if_needed()
                elif value == "up":
                    self.page.evaluate(
                        "el => el.scrollBy(0, -window.innerHeight)", element)
        else:
            if value == "down":
                self.page.keyboard.press("PageDown")
            elif value == "up":
                self.page.keyboard.press("PageUp")

    def _handle_done(self, action: Dict[str, Any]) -> None:
        summary = action.get("thought", "<goal achieved>")
        logger.info(f"[DONE] {summary}")

    def close(self) -> None:
        self.browser.close()
        self.playwright.stop()
