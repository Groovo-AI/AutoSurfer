#!/usr/bin/env python3
"""
Test script to demonstrate simplified AutoSurfer captcha detection.
This script shows how the system detects captchas and exits gracefully.
"""

from autosurfer.logger import logger
from autosurfer.agent.browser_agent import AutoSurferAgent
from autosurfer.agent.browser.captcha_handler import CaptchaHandler
import os
import sys
import time
from pathlib import Path

# Add the autosurfer package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_captcha_detection():
    """Test captcha detection capabilities"""
    print("\n" + "="*60)
    print("TESTING SIMPLE CAPTCHA DETECTION")
    print("="*60)

    from autosurfer.agent.browser.manager import BrowserManager, BrowserSettings

    # Create browser session
    settings = BrowserSettings(stealth_mode=True, headless=False)
    browser_manager = BrowserManager(settings=settings)

    try:
        # Navigate to a site that might have captcha
        browser_manager.page.goto(
            "https://www.google.com/recaptcha/api2/demo", wait_until="networkidle")
        time.sleep(2)

        # Initialize captcha handler
        captcha_handler = CaptchaHandler(browser_manager.page)

        # Test detection
        result = captcha_handler.handle_captcha_detection()

        if result:
            print("✅ No captcha detected - task can continue")
        else:
            print("🔒 Captcha detected - task would be terminated")

    except Exception as e:
        print(f"❌ Captcha detection test failed: {e}")
    finally:
        browser_manager.close()


def test_agent_with_captcha_detection():
    """Test the agent with captcha detection"""
    print("\n" + "="*60)
    print("TESTING AGENT WITH CAPTCHA DETECTION")
    print("="*60)

    objective = "Go to google.com and search for 'test' - exit if captcha appears"

    try:
        agent = AutoSurferAgent(objective=objective,
                                headless=False, max_retries=3)
        agent.run()
        print("✅ Agent with captcha detection completed!")
    except Exception as e:
        print(f"❌ Agent test failed: {e}")


def test_captcha_detection_methods():
    """Test individual captcha detection methods"""
    print("\n" + "="*60)
    print("TESTING CAPTCHA DETECTION METHODS")
    print("="*60)

    from autosurfer.agent.browser.manager import BrowserManager, BrowserSettings

    # Create browser session
    settings = BrowserSettings(stealth_mode=True, headless=False)
    browser_manager = BrowserManager(settings=settings)

    try:
        # Navigate to a test page
        browser_manager.page.goto(
            "https://www.google.com/recaptcha/api2/demo", wait_until="networkidle")
        time.sleep(2)

        # Initialize captcha handler
        captcha_handler = CaptchaHandler(browser_manager.page)

        # Test detection
        captcha_info = captcha_handler.detect_captcha()

        if captcha_info:
            print(f"🔒 Captcha detected: {captcha_info.type}")
            print(f"   Confidence: {captcha_info.confidence}")
            print(f"   Selectors: {captcha_info.selectors}")
        else:
            print("✅ No captcha detected")

        print("✅ Captcha detection methods test completed!")

    except Exception as e:
        print(f"❌ Captcha detection methods test failed: {e}")
    finally:
        browser_manager.close()


def main():
    """Run simplified captcha detection tests"""
    print("🔒 AutoSurfer Simple Captcha Detection Test Suite")
    print("This demonstrates the simplified captcha detection approach")

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable is required")
        print("Please set it with: export OPENAI_API_KEY='your-api-key'")
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
            print("\n⏹️  Test interrupted by user")
            break
        except Exception as e:
            print(f"❌ Test failed with error: {e}")

    print("\n" + "="*60)
    print("SIMPLE CAPTCHA DETECTION TEST SUITE COMPLETED")
    print("="*60)
    print("\n📝 Simple Captcha Detection Features:")
    print("✅ Lightweight captcha detection")
    print("✅ No complex solving logic")
    print("✅ Graceful task termination")
    print("✅ Clean error messages")
    print("✅ Future-ready for screen streaming")
    print("✅ Minimal dependencies")


if __name__ == "__main__":
    main()
