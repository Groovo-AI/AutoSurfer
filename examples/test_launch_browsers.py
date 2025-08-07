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


def test_camoufox_adapter():
    """Test Camoufox adapter by creating browser and navigating"""
    logger.info("\n" + "="*60)
    logger.info("TESTING CAMOUFOX ADAPTER")
    logger.info("="*60)

    try:
        # Create Camoufox adapter
        settings = BrowserSettings(headless=False, stealth_mode=True)
        browser_session = create_browser_adapter("camoufox", settings)

        logger.info("✅ Camoufox adapter created successfully")

        # Test basic browser functionality
        page = browser_session.page
        page.goto("https://www.google.com/search?q=nike")
        title = page.title()
        logger.info(f"✅ Navigated to example.com, title: {title}")

        # Test page interaction
        screenshot_path = TEMP_DIR / "camoufox_test.png"
        page.screenshot(path=str(screenshot_path))
        logger.info(f"✅ Screenshot saved as {screenshot_path}")

        # Close browser
        browser_session.close()
        logger.info("✅ Camoufox browser closed successfully")

    except Exception as e:
        logger.error(f"❌ Camoufox adapter test failed: {e}")


def test_adapter_comparison():
    """Compare all adapters side by side"""
    logger.info("\n" + "="*60)
    logger.info("COMPARING ALL ADAPTERS")
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

    # Test Camoufox
    logger.info("\n--- CAMOUFOX ---")
    try:
        start_time = time.time()
        settings = BrowserSettings(headless=True)
        browser_session = create_browser_adapter("camoufox", settings)

        page = browser_session.page
        page.goto(test_url)
        status = page.content()

        camoufox_time = time.time() - start_time
        browser_session.close()

        logger.info(f"✅ Camoufox completed in {camoufox_time:.2f}s")
        logger.info(f"   Status: {len(status)} characters received")

    except Exception as e:
        logger.error(f"❌ Camoufox failed: {e}")
        camoufox_time = None

    # Comparison
    times = []
    if browserbase_time:
        times.append(("BrowserBase", browserbase_time))
    if playwright_time:
        times.append(("Playwright", playwright_time))
    if camoufox_time:
        times.append(("Camoufox", camoufox_time))

    if len(times) >= 2:
        logger.info(f"\n📊 COMPARISON:")
        for name, time_taken in times:
            logger.info(f"{name}: {time_taken:.2f}s")

        # Find fastest
        fastest = min(times, key=lambda x: x[1])
        logger.info(f"🏆 Fastest: {fastest[0]} ({fastest[1]:.2f}s)")


def main():
    """Run browser adapter tests"""
    logger.info("🌐 AutoSurfer Browser Adapter Test Suite")
    logger.info("This tests Playwright, BrowserBase, and Camoufox adapters")

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

    # Check if Camoufox is available
    try:
        import camoufox
        logger.info("✅ Camoufox is available")
    except ImportError:
        logger.warn(
            "⚠️  Camoufox not installed. Install with: pip install camoufox")
        logger.warn("Camoufox tests will be skipped")
    except Exception as e:
        logger.warn(f"⚠️  Camoufox import error: {e}")
        logger.warn("Camoufox tests will be skipped")

    # Run tests - BrowserBase first, then Playwright, then Camoufox
    tests = [
        test_browserbase_adapter,
        test_playwright_adapter,
        test_adapter_comparison,
        test_camoufox_adapter,
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
