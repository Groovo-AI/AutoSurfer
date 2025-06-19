# autosurfer/agent/browser/action_executor.py
from pathlib import Path
from playwright.sync_api import sync_playwright
from autosurfer.logger import logger
from autosurfer.llm.response_schema.browser_actions import NextActions

JS_PATH = Path(__file__).parent / "dom" / "annotateDom.js"
JS_CODE = JS_PATH.read_text() if JS_PATH.exists() else ""


class BrowserActionExecutor:
    def __init__(self, headless: bool = False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless, args=["--start-maximized"])
        ctx = self.browser.new_context(viewport=None)
        if JS_CODE:
            ctx.add_init_script(JS_CODE)
        self.page = ctx.new_page()
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

    def annotate_ui(self):
        self.page.wait_for_load_state("networkidle")
        elements = self.page.evaluate(
            "() => window.collectInteractive({ highlight: true })")
        return [
            {
                "index": el["index"],
                "tag": el["tag"],
                "id": el.get("id"),
                "testid": el.get("testid"),
                "text": el.get("text"),
                "xpath": el.get("xpath")
            }
            for el in elements
        ]

    def remove_annotation(self):
        self.page.evaluate("() => window.clearInteractiveHighlights()")

    def close(self):
        self.browser.close()
        self.playwright.stop()

    def _goto(self, url):
        self.page.goto(url, wait_until="networkidle")

    def _click(self, selector):
        self.page.click(selector)

    def _fill(self, selector, value):
        self.page.fill(selector, value)

    def _press(self, key):
        self.page.keyboard.press(key)

    def _wait(self, seconds):
        import time
        time.sleep(seconds)

    def _scroll(self, direction, selector=None):
        if selector:
            el = self.page.query_selector(selector)
            if el:
                el.scroll_into_view_if_needed()
        else:
            key = "PageDown" if direction == "down" else "PageUp"
            self.page.keyboard.press(key)

    def _done(self, summary):
        logger.info(f"[DONE] {summary}")
