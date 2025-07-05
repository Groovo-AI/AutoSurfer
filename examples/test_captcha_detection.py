#!/usr/bin/env python3
"""
Test script to demonstrate simplified AutoSurfer captcha detection.
This script shows how the system detects captchas and exits gracefully.
"""

from autosurfer.logger import logger
from autosurfer.agent.browser_agent import AutoSurferAgent
from autosurfer.agent.browser.captcha_handler import CaptchaHandler
from autosurfer.agent.browser.adapters import BrowserSettings, create_browser_adapter
import os
import sys
import time
from pathlib import Path

# Add root path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Use logger.info / logger.error instead of print


def test_captcha_detection():
    """Test captcha detection capabilities"""
    logger.info("\n" + "="*60)
    logger.info("TESTING SIMPLE CAPTCHA DETECTION")
    logger.info("="*60)

    # Create browser session
    settings = BrowserSettings(stealth_mode=True, headless=False)
    browser_session = create_browser_adapter("playwright", settings)

    try:
        # Navigate to a site that might have captcha
        browser_session.page.goto(
            "https://www.google.com/recaptcha/api2/demo", wait_until="networkidle")
        time.sleep(2)

        # Initialize captcha handler
        captcha_handler = CaptchaHandler(browser_session.page)

        # Test detection
        result = captcha_handler.handle_captcha_detection()

        if result:
            logger.info("✅ No captcha detected - task can continue")
        else:
            logger.info("🔒 Captcha detected - task would be terminated")

    except Exception as e:
        logger.error(f"❌ Captcha detection test failed: {e}")
    finally:
        browser_session.close()


def test_agent_with_captcha_detection():
    """Test the agent with captcha detection"""
    logger.info("\n" + "="*60)
    logger.info("TESTING AGENT WITH CAPTCHA DETECTION")
    logger.info("="*60)

    objective = "Go to google.com and search for 'test' - exit if captcha appears"

    try:
        settings = BrowserSettings(headless=False)
        browser_session = create_browser_adapter("playwright", settings)
        agent = AutoSurferAgent(objective=objective,
                                browser_session=browser_session, max_retries=3)
        agent.run()
        logger.info("✅ Agent with captcha detection completed!")
    except Exception as e:
        logger.error(f"❌ Agent test failed: {e}")


def test_captcha_detection_methods():
    """Test individual captcha detection methods"""
    logger.info("\n" + "="*60)
    logger.info("TESTING CAPTCHA DETECTION METHODS")
    logger.info("="*60)

    # Create browser session
    settings = BrowserSettings(stealth_mode=True, headless=False)
    browser_session = create_browser_adapter("playwright", settings)

    try:
        # Navigate to a test page
        browser_session.page.goto(
            "https://www.google.com/recaptcha/api2/demo", wait_until="networkidle")
        time.sleep(2)

        # Initialize captcha handler
        captcha_handler = CaptchaHandler(browser_session.page)

        # Test detection
        captcha_info = captcha_handler.detect_captcha()

        if captcha_info:
            logger.info(f"🔒 Captcha detected: {captcha_info.type}")
            logger.info(f"   Confidence: {captcha_info.confidence}")
            logger.info(f"   Selectors: {captcha_info.selectors}")
        else:
            logger.info("✅ No captcha detected")

        logger.info("✅ Captcha detection methods test completed!")

    except Exception as e:
        logger.error(f"❌ Captcha detection methods test failed: {e}")
    finally:
        browser_session.close()


def main():
    """Run simplified captcha detection tests"""
    logger.info("🔒 AutoSurfer Simple Captcha Detection Test Suite")
    logger.info("This demonstrates the simplified captcha detection approach")

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("❌ OPENAI_API_KEY environment variable is required")
        logger.error(
            "Please set it with: export OPENAI_API_KEY='your-api-key'")
        return

    # Run tests
    tests = [
        test_captcha_detection,
        test_captcha_detection_methods,
        # test_agent_with_captcha_detection,  # Uncomment to test full agent
    ]

    for test in tests:
        try:
            test()
            time.sleep(3)  # Brief pause between tests
        except KeyboardInterrupt:
            logger.info("\n⏹️  Test interrupted by user")
            break
        except Exception as e:
            logger.error(f"❌ Test failed with error: {e}")

    logger.info("\n" + "="*60)
    logger.info("SIMPLE CAPTCHA DETECTION TEST SUITE COMPLETED")
    logger.info("="*60)
    logger.info("\n📝 Simple Captcha Detection Features:")
    logger.info("✅ Lightweight captcha detection")
    logger.info("✅ No complex solving logic")
    logger.info("✅ Graceful task termination")
    logger.info("✅ Clean error messages")
    logger.info("✅ Future-ready for screen streaming")
    logger.info("✅ Minimal dependencies")


if __name__ == "__main__":
    main()
