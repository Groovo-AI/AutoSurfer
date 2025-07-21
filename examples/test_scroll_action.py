from autosurfer.logger import logger
from autosurfer.agent.browser_agent import AutoSurferAgent
from autosurfer.agent.browser.adapters import BrowserSettings, create_browser_adapter


def test_scroll_action():
    logger.info("\n" + "="*60)
    logger.info("🧪 TEST: Scroll Action with Summarize Prompt")
    logger.info("="*60)

    objective = "Go to octifytechnologies.com and summarize this website"
    settings = BrowserSettings(headless=False)
    browser_session = create_browser_adapter("playwright", settings)
    agent = AutoSurferAgent(
        objective=objective,
        browser_session=browser_session,
        enable_memory=True
    )
    agent.run()


if __name__ == "__main__":
    test_scroll_action()
