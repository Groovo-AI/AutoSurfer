from autosurfer.logger import logger
from autosurfer.agent.browser_agent import AutoSurferAgent
from autosurfer.agent.browser.adapters import BrowserSettings, create_browser_adapter


def test_loop_detection():
    logger.info("\n" + "="*60)
    logger.info("🧪 TEST: Loop Detection with Repeated Failing Action")
    logger.info("="*60)

    # This prompt should cause the agent to repeat a failing action (e.g., clicking a non-existent selector)
    objective = "Go to https://example.com and click the button with selector '#nonexistent-button' repeatedly"
    settings = BrowserSettings(headless=False)
    browser_session = create_browser_adapter("playwright", settings)
    agent = AutoSurferAgent(
        objective=objective,
        browser_session=browser_session,
        enable_memory=True
    )
    agent.run()


if __name__ == "__main__":
    test_loop_detection()
