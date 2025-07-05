from autosurfer.logger import logger
from autosurfer.llm.response_schema.browser_actions import NextActions
from playwright.sync_api import Page, Browser, TimeoutError
import time
from typing import Optional
from pathlib import Path


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
            "scroll_to_bottom": self._scroll_to_bottom,
            "scroll_to_top": self._scroll_to_top,
            "done": self._done,
        }

    def execute(self, next_actions: NextActions):
        for item in next_actions.actions:
            logger.info(f"[Agent Thought] {item.thought}")
            fn = self._dispatch.get(item.action.type)
            if not fn:
                logger.warn(f"Unknown action type: {item.action.type}")
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
                elif item.action.type == "scroll_to_bottom":
                    fn()
                elif item.action.type == "scroll_to_top":
                    fn()
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

        # Always inject script to ensure it's available
        js_path = Path(__file__).parent / "dom" / "annotateDom.js"
        self.page.evaluate(js_path.read_text())

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
        try:
            self.page.goto(url, wait_until="networkidle", timeout=30000)
            # Wait a bit for any dynamic content to load
            time.sleep(1)
        except TimeoutError:
            logger.warn(f"Navigation timeout for {url}, but continuing...")
            # Try with a shorter timeout
            self.page.goto(url, wait_until="domcontentloaded", timeout=15000)

    def _click(self, selector: str):
        logger.info(f"Clicking: {selector}")

        # Try multiple selector strategies
        selectors_to_try = []

        if selector.startswith("/"):
            selectors_to_try.append(f"xpath={selector}")
        elif selector.startswith("text="):
            selectors_to_try.append(selector)
        elif selector.startswith(":has-text("):
            selectors_to_try.append(selector)
        else:
            # Try the original selector first
            selectors_to_try.append(selector)

            # If it's a simple text, try text selector
            if not any(char in selector for char in ["#", ".", "[", "="]):
                selectors_to_try.append(f'text="{selector}"')
                selectors_to_try.append(f':has-text("{selector}")')

        for sel in selectors_to_try:
            try:
                # Wait for element to be visible and clickable
                element = self.page.wait_for_selector(
                    sel, timeout=5000, state="visible")
                if element:
                    element.click()
                    return
            except Exception as e:
                logger.debug(f"Selector {sel} failed: {e}")
                continue

        # If all selectors fail, try to find by text content
        try:
            self.page.click(f'text="{selector}"')
        except:
            raise Exception(
                f"Could not click element with selector: {selector}")

    def _fill(self, selector: str, value: str):
        logger.info(f"Filling {selector} with: {value}")

        # Try multiple selector strategies
        selectors_to_try = []

        if selector.startswith("/"):
            selectors_to_try.append(f"xpath={selector}")
        else:
            selectors_to_try.append(selector)

            # If it's a simple text, try to find input by placeholder or label
            if not any(char in selector for char in ["#", ".", "[", "="]):
                selectors_to_try.append(f'input[placeholder*="{selector}"]')
                selectors_to_try.append(f'input[name*="{selector}"]')

        for sel in selectors_to_try:
            try:
                element = self.page.wait_for_selector(
                    sel, timeout=5000, state="visible")
                if element:
                    element.fill(value)
                    return
            except Exception as e:
                logger.debug(f"Fill selector {sel} failed: {e}")
                continue

        raise Exception(f"Could not fill element with selector: {selector}")

    def _press(self, key: str):
        logger.info(f"Pressing key: {key}")
        self.page.keyboard.press(key)

    def _wait(self, seconds: float):
        logger.info(f"Waiting for {seconds} seconds")
        time.sleep(seconds)

    def _scroll(self, direction: str, selector: Optional[str] = None):
        if selector:
            logger.info(f"Scrolling to element: {selector}")
            try:
                if selector.startswith("/"):
                    self.page.locator(
                        f"xpath={selector}").scroll_into_view_if_needed()
                else:
                    self.page.locator(selector).scroll_into_view_if_needed()
            except Exception as e:
                logger.warn(f"Could not scroll to {selector}: {e}")
                # Fallback to general scroll
                if direction == "down":
                    self.page.evaluate("window.scrollBy(0, 500)")
                elif direction == "up":
                    self.page.evaluate("window.scrollBy(0, -500)")
        else:
            logger.info(f"Scrolling {direction}")

            # Remove existing annotations before scrolling
            self.remove_annotation()
            logger.info("Removed existing annotations")
            time.sleep(2)  # Wait for annotations to be fully removed

            if direction == "down":
                # Get window height and scroll by that amount to avoid duplicate content
                window_height = self.page.evaluate("window.innerHeight")
                self.page.evaluate(f"window.scrollBy(0, {window_height})")
            elif direction == "up":
                # Get window height and scroll up by that amount
                window_height = self.page.evaluate("window.innerHeight")
                self.page.evaluate(f"window.scrollBy(0, -{window_height})")

            logger.info(f"Scrolled {direction} by {window_height}px")
            time.sleep(2)  # Wait for scroll to complete and content to load

            # Annotate the new viewport after scrolling
            self.annotate_ui()
            logger.info(f"Annotated new viewport after scrolling {direction}")

    def scroll_to_bottom(self):
        """Scroll to the very bottom of the page"""
        logger.info("Scrolling to bottom of page")
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self):
        """Scroll to the very top of the page"""
        logger.info("Scrolling to top of page")
        self.page.evaluate("window.scrollTo(0, 0)")

    def get_scroll_info(self):
        """Get current scroll position and page dimensions"""
        return self.page.evaluate("""
            () => {
                return {
                    scrollY: window.scrollY,
                    scrollHeight: document.body.scrollHeight,
                    clientHeight: document.documentElement.clientHeight,
                    windowHeight: window.innerHeight,
                    isAtBottom: window.scrollY + window.innerHeight >= document.body.scrollHeight,
                    isAtTop: window.scrollY === 0
                }
            }
        """)

    def _scroll_to_bottom(self):
        """Scroll to the very bottom of the page"""
        logger.info("Scrolling to bottom of page")
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def _scroll_to_top(self):
        """Scroll to the very top of the page"""
        logger.info("Scrolling to top of page")
        self.page.evaluate("window.scrollTo(0, 0)")

    def _scroll_comprehensive(self, description: str):
        """Comprehensive scrolling through the entire page with DOM annotation at each position"""
        logger.info(f"Starting comprehensive scroll: {description}")

        # Get initial scroll info
        scroll_info = self.get_scroll_info()
        total_height = scroll_info['scrollHeight']
        window_height = scroll_info['windowHeight']

        # Annotate the current viewport
        self.annotate_ui()
        logger.info(
            "Initial viewport annotated - agent can now interact with current viewport")

    def _done(self, summary: str):
        logger.info(f"[DONE] {summary}")
