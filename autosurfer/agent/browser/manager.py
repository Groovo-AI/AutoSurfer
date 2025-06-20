from playwright.sync_api import sync_playwright
from pathlib import Path
from playwright.sync_api import sync_playwright

JS_PATH = Path(__file__).parent / "dom" / "annotateDom.js"
JS_CODE = JS_PATH.read_text() if JS_PATH.exists() else ""


class BrowserManager:
    def __init__(self, headless: bool = False, stealth_mode: bool = False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless, args=["--start-maximized"])
        ctx = self.browser.new_context(viewport=None)
        if JS_CODE:
            ctx.add_init_script(JS_CODE)
        self.page = ctx.new_page()
