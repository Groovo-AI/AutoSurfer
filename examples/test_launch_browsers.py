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
        page.screenshot(path="playwright_test.png")
        logger.info("✅ Screenshot saved as playwright_test.png")

        # Close browser
        browser_session.close()
        logger.info("✅ Playwright browser closed successfully")

    except Exception as e:
        logger.error(f"❌ Playwright adapter test failed: {e}")


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
        page.screenshot(path="browserbase_test.png")
        logger.info("✅ Screenshot saved as browserbase_test.png")

        # Close browser
        browser_session.close()
        logger.info("✅ BrowserBase browser closed successfully")

    except Exception as e:
        logger.error(f"❌ BrowserBase adapter test failed: {e}")


def test_adapter_comparison():
    """Compare both adapters side by side"""
    logger.info("\n" + "="*60)
    logger.info("COMPARING BOTH ADAPTERS")
    logger.info("="*60)

    test_url = "https://httpbin.org/status/200"

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

    # Test BrowserBase
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

    # Comparison
    if playwright_time and browserbase_time:
        logger.info(f"\n📊 COMPARISON:")
        logger.info(f"Playwright: {playwright_time:.2f}s")
        logger.info(f"BrowserBase: {browserbase_time:.2f}s")
        difference = browserbase_time - playwright_time
        logger.info(
            f"Difference: {difference:+.2f}s ({difference/playwright_time*100:+.1f}%)")


def main():
    """Run browser adapter tests"""
    logger.info("🌐 AutoSurfer Browser Adapter Test Suite")
    logger.info("This tests both Playwright and BrowserBase adapters")

    # Check if BrowserBase is available
    try:
        from browserbase import Client
        logger.info("✅ BrowserBase is available")
    except ImportError:
        logger.warn(
            "⚠️  BrowserBase not installed. Install with: pip install browserbase")
        logger.warn("BrowserBase tests will be skipped")
    except Exception as e:
        logger.warn(f"⚠️  BrowserBase import error: {e}")
        logger.warn("BrowserBase tests will be skipped")

    # Run tests
    tests = [
        test_playwright_adapter,
        test_browserbase_adapter,
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
