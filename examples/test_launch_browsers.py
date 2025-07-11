#!/usr/bin/env python3
"""
Test script to launch and test both Playwright and BrowserBase adapters.
This demonstrates how to create browser sessions with both adapters.
"""

from autosurfer.logger import logger
from autosurfer.agent.browser.adapters import BrowserSettings, create_browser_adapter
import os
import sys
import time
from pathlib import Path

# Add the autosurfer package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Create .temp directory for screenshots
TEMP_DIR = Path(__file__).parent.parent / ".temp"
TEMP_DIR.mkdir(exist_ok=True)


def test_browserbase_adapter():
    """Test BrowserBase adapter by creating browser and navigating"""
    logger.info("\n" + "="*60)
    logger.info("TESTING BROWSERBASE ADAPTER")
    logger.info("="*60)

    try:
        # Create BrowserBase adapter
        settings = BrowserSettings(headless=True, stealth_mode=False)
        browser_session = create_browser_adapter("browserbase", settings)

        logger.info("✅ BrowserBase adapter created successfully")

        # Test basic browser functionality
        page = browser_session.page
        page.goto("https://example.com")
        title = page.title()
        logger.info(f"✅ Navigated to example.com, title: {title}")

        # Test page interaction
        screenshot_path = TEMP_DIR / "browserbase_test.png"
        page.screenshot(path=str(screenshot_path))
        logger.info(f"✅ Screenshot saved as {screenshot_path}")

        # Close browser
        browser_session.close()
        logger.info("✅ BrowserBase browser closed successfully")

    except Exception as e:
        logger.error(f"❌ BrowserBase adapter test failed: {e}")


def test_playwright_adapter():
    """Test Playwright adapter by creating browser and navigating"""
    logger.info("\n" + "="*60)
    logger.info("TESTING PLAYWRIGHT ADAPTER")
    logger.info("="*60)

    try:
        # Create Playwright adapter
        settings = BrowserSettings(headless=False, stealth_mode=True)
        browser_session = create_browser_adapter("playwright", settings)

        logger.info("✅ Playwright adapter created successfully")

        # Test basic browser functionality
        page = browser_session.page
        page.goto("https://example.com")
        title = page.title()
        logger.info(f"✅ Navigated to example.com, title: {title}")

        # Test page interaction
        screenshot_path = TEMP_DIR / "playwright_test.png"
        page.screenshot(path=str(screenshot_path))
        logger.info(f"✅ Screenshot saved as {screenshot_path}")

        # Close browser
        browser_session.close()
        logger.info("✅ Playwright browser closed successfully")

    except Exception as e:
        logger.error(f"❌ Playwright adapter test failed: {e}")


def test_adapter_comparison():
    """Compare both adapters side by side"""
    logger.info("\n" + "="*60)
    logger.info("COMPARING BOTH ADAPTERS")
    logger.info("="*60)

    test_url = "https://httpbin.org/status/200"

    # Test BrowserBase first
    logger.info("\n--- BROWSERBASE ---")
    try:
        start_time = time.time()
        settings = BrowserSettings(headless=True)
        browser_session = create_browser_adapter("browserbase", settings)

        page = browser_session.page
        page.goto(test_url)
        status = page.content()

        browserbase_time = time.time() - start_time
        browser_session.close()

        logger.info(f"✅ BrowserBase completed in {browserbase_time:.2f}s")
        logger.info(f"   Status: {len(status)} characters received")

    except Exception as e:
        logger.error(f"❌ BrowserBase failed: {e}")
        browserbase_time = None

    # Test Playwright
    logger.info("\n--- PLAYWRIGHT ---")
    try:
        start_time = time.time()
        settings = BrowserSettings(headless=True)
        browser_session = create_browser_adapter("playwright", settings)

        page = browser_session.page
        page.goto(test_url)
        status = page.content()

        playwright_time = time.time() - start_time
        browser_session.close()

        logger.info(f"✅ Playwright completed in {playwright_time:.2f}s")
        logger.info(f"   Status: {len(status)} characters received")

    except Exception as e:
        logger.error(f"❌ Playwright failed: {e}")
        playwright_time = None

    # Comparison
    if playwright_time and browserbase_time:
        logger.info(f"\n📊 COMPARISON:")
        logger.info(f"BrowserBase: {browserbase_time:.2f}s")
        logger.info(f"Playwright: {playwright_time:.2f}s")
        difference = browserbase_time - playwright_time
        logger.info(
            f"Difference: {difference:+.2f}s ({difference/playwright_time*100:+.1f}%)")


def main():
    """Run browser adapter tests"""
    logger.info("🌐 AutoSurfer Browser Adapter Test Suite")
    logger.info("This tests both Playwright and BrowserBase adapters")

    # Check if BrowserBase is available
    try:
        from browserbase import Browserbase
        logger.info("✅ BrowserBase is available")

        # Check if BrowserBase credentials are set
        from autosurfer.config import Config
        if not Config.BROWSERBASE_API_KEY:
            logger.warn(
                "⚠️  BROWSERBASE_API_KEY not set. BrowserBase tests will fail.")
        else:
            logger.info("✅ BrowserBase API key is configured")

        if not Config.BROWSERBASE_PROJECT_ID:
            logger.warn(
                "⚠️  BROWSERBASE_PROJECT_ID not set. BrowserBase tests will fail.")
        else:
            logger.info("✅ BrowserBase project ID is configured")

    except ImportError:
        logger.warn(
            "⚠️  BrowserBase not installed. Install with: pip install browserbase")
        logger.warn("BrowserBase tests will be skipped")
    except Exception as e:
        logger.warn(f"⚠️  BrowserBase import error: {e}")
        logger.warn("BrowserBase tests will be skipped")

    # Run tests - BrowserBase first, then Playwright
    tests = [
        test_browserbase_adapter,
        test_playwright_adapter,
        test_adapter_comparison,
    ]

    for test in tests:
        try:
            test()
            time.sleep(2)  # Brief pause between tests
        except KeyboardInterrupt:
            logger.info("\n⏹️  Test interrupted by user")
            break
        except Exception as e:
            logger.error(f"❌ Test failed with error: {e}")

    logger.info("\n" + "="*60)
    logger.info("BROWSER ADAPTER TEST SUITE COMPLETED")
    logger.info("="*60)


if __name__ == "__main__":
    main()
