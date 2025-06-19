
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from autosurfer.logger import logger
from autosurfer.llm.response_schema.browser_actions import NextActions

ANNOTATE_JS_PATH = (
    Path(__file__).parent / "dom" / "annotateDom.js"
)

if ANNOTATE_JS_PATH.exists():
    ANNOTATE_JS = ANNOTATE_JS_PATH.read_text()
else:
    ANNOTATE_JS = ""  # fallback – no highlight


class BrowserActionExecutor:
    def __init__(self, next_actions: NextActions, headless: bool = False):
        self.action_items = next_actions.actions
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=["--start-maximized"],
        )
        ctx = self.browser.new_context(viewport=None)
        self.page = ctx.new_page()

        if ANNOTATE_JS:
            self.page.add_init_script(ANNOTATE_JS)

        self._dispatch = {
            "goto": self._goto,
            "click": self._click,
            "fill": self._fill,
            "press": self._press,
            "wait": self._wait,
            "scroll": self._scroll,
            "done": self._done,
        }

    def execute(self):
        """Iterate over ActionItem list and perform each action."""
        for item in self.action_items:
            thought, act = item.thought, item.action
            logger.info(f"[Agent Thought] {thought}")

            fn = self._dispatch.get(act.type)
            if fn is None:
                logger.warning(f"❓ Unrecognised action type: {act.type}")
                continue

            # Dispatch by action type
            if act.type == "goto":
                fn(act.url)
            elif act.type == "click":
                fn(act.selector)
            elif act.type == "fill":
                fn(act.selector, act.value)
            elif act.type == "press":
                fn(act.key)
            elif act.type == "wait":
                fn(act.seconds)
            elif act.type == "scroll":
                fn(act.direction, act.selector)
            elif act.type == "done":
                fn(act.summary)
                break

    def close(self):
        self.browser.close()
        self.playwright.stop()

    def _goto(self, url):
        logger.info(f"→ Navigating to {url}")
        self.page.goto(url, wait_until="networkidle")

    def _click(self, selector):
        logger.info(f"→ Clicking {selector}")
        self.page.click(selector)

    def _fill(self, selector, value):
        logger.info(f"→ Filling {selector} with '{value}'")
        self.page.fill(selector, value)

    def _press(self, key):
        logger.info(f"→ Pressing {key}")
        self.page.keyboard.press(key)

    def _wait(self, seconds):
        logger.info(f"→ Waiting {seconds}s")
        time.sleep(seconds)

    def _scroll(self, direction, selector=None):
        logger.info(f"→ Scrolling {direction} on {selector or 'page'}")
        if selector:
            el = self.page.query_selector(selector)
            if el:
                el.scroll_into_view_if_needed()
        else:
            self.page.keyboard.press(
                "PageDown" if direction == "down" else "PageUp")

    def _done(self, summary):
        logger.info(f"[DONE] {summary}")
