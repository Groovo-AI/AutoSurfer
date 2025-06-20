from autosurfer.agent.browser.manager import BrowserManager, BrowserSettings
from autosurfer.agent.browser.action_executor import BrowserActionExecutor

settings = BrowserSettings(
    stealth_mode=True,
    headless=False
)
session = BrowserManager(
    settings=settings
)

executor = BrowserActionExecutor(
    browser_session=session.browser,
    page=session.page
)

executor._goto("https://www.google.com")
