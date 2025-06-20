from autosurfer.agent.browser.manager import BrowserManager
from autosurfer.agent.browser.action_executor import BrowserActionExecutor

session = BrowserManager()

executor = BrowserActionExecutor(
    browser_session=session.browser,
    page=session.page
)

executor._goto("https://www.google.com")
