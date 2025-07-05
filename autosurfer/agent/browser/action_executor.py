from autosurfer.logger import logger
from autosurfer.llm.response_schema.browser_actions import NextActions
from playwright.sync_api import Page, Browser
import time
from typing import Optional


class BrowserActionExecutor:
    def __init__(self, page: Page, browser_session: Browser):
        self.page = page
        self.browser = browser_session
        self._dispatch = {
            "goto": self._goto,
            "click": self._click,
            "fill": self._fill,
            "press": self._press,
            "wait": self._wait,
            "scroll": self._scroll,
            "done": self._done,
        }

    def execute(self, next_actions: NextActions):
        for item in next_actions.actions:
            logger.info(f"[Agent Thought] {item.thought}")
            fn = self._dispatch.get(item.action.type)
            if not fn:
                continue

            try:
                if item.action.type == "goto":
                    fn(item.action.url)
                elif item.action.type == "click":
                    fn(item.action.selector)
                elif item.action.type == "fill":
                    fn(item.action.selector, item.action.value)
                elif item.action.type == "press":
                    fn(item.action.key)
                elif item.action.type == "wait":
                    fn(item.action.seconds)
                elif item.action.type == "scroll":
                    fn(item.action.direction, item.action.selector)
                elif item.action.type == "done":
                    fn(item.action.summary)
                    return

                time.sleep(0.5)

            except Exception as e:
                logger.error(f"Failed to execute {item.action.type}: {e}")
                raise

    def annotate_ui(self):
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except:
            pass

        elements = self.page.evaluate(
            "() => window.collectInteractive({ highlight: true })")

        return [
            {
                "index": el["index"],
                "tag": el["tag"],
                "id": el.get("id"),
                "testid": el.get("data-testid"),
                "text": el.get("text"),
                "xpath": el.get("xpath"),
            }
            for el in elements
        ]

    def remove_annotation(self):
        self.page.evaluate("() => window.clearInteractiveHighlights()")

    def _goto(self, url):
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="networkidle", timeout=30000)

    def _click(self, selector: str):
        # Simple selector handling - let Playwright handle the rest
        if selector.startswith("/"):
            self.page.click(f"xpath={selector}")
        else:
            self.page.click(selector)

    def _fill(self, selector: str, value: str):
        if selector.startswith("/"):
            self.page.fill(f"xpath={selector}", value)
        else:
            self.page.fill(selector, value)

    def _press(self, key: str):
        self.page.keyboard.press(key)

    def _wait(self, seconds: float):
        time.sleep(seconds)

    def _scroll(self, direction: str, selector: Optional[str] = None):
        if selector:
            if selector.startswith("/"):
                self.page.locator(
                    f"xpath={selector}").scroll_into_view_if_needed()
            else:
                self.page.locator(selector).scroll_into_view_if_needed()
        else:
            if direction == "down":
                self.page.evaluate("window.scrollBy(0, 500)")
            elif direction == "up":
                self.page.evaluate("window.scrollBy(0, -500)")

    def _done(self, summary: str):
        logger.info(f"[DONE] {summary}")
