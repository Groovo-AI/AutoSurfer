#!/usr/bin/env python3
"""
Test script to demonstrate AutoSurfer improvements for better accuracy.
This script shows how the enhanced system handles common web automation tasks.
"""

from autosurfer.logger import logger
from autosurfer.agent.browser_agent import AutoSurferAgent
import os
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Use logger directly in this example script


def test_httpbin_form():
    """Test form filling automation on httpbin"""
    logger.info("\n" + "="*60)
    logger.info("TESTING HTTPBIN FORM FILLING AUTOMATION")
    logger.info("="*60)

    objective = "Go to httpbin.org/forms/post and fill out the form with name 'John Doe', age '30', and submit it"

    try:
        agent = AutoSurferAgent(objective=objective,
                                headless=False, max_retries=3)
        agent.run()
        logger.info("✅ HTTPBin form test completed successfully!")
    except Exception as e:
        logger.error(f"❌ HTTPBin form test failed: {e}")


def test_google_search():
    """Test Google search automation"""
    logger.info("\n" + "="*60)
    logger.info("TESTING GOOGLE SEARCH AUTOMATION")
    logger.info("="*60)

    objective = "Go to google.com and search for 'Python automation'"

    try:
        agent = AutoSurferAgent(objective=objective,
                                headless=False, max_retries=3)
        agent.run()
        logger.info("✅ Google search test completed successfully!")
    except Exception as e:
        logger.error(f"❌ Google search test failed: {e}")


def test_wikipedia_navigation():
    """Test Wikipedia navigation automation"""
    logger.info("\n" + "="*60)
    logger.info("TESTING WIKIPEDIA NAVIGATION AUTOMATION")
    logger.info("="*60)

    objective = "Go to wikipedia.org and search for 'Python programming language'"

    try:
        agent = AutoSurferAgent(objective=objective,
                                headless=False, max_retries=3)
        agent.run()
        logger.info("✅ Wikipedia navigation test completed successfully!")
    except Exception as e:
        logger.error(f"❌ Wikipedia navigation test failed: {e}")


def test_simple_navigation():
    """Test simple navigation automation"""
    logger.info("\n" + "="*60)
    logger.info("TESTING SIMPLE NAVIGATION AUTOMATION")
    logger.info("="*60)

    objective = "Go to example.com and verify the page loads"

    try:
        agent = AutoSurferAgent(objective=objective,
                                headless=False, max_retries=3)
        agent.run()
        logger.info("✅ Simple navigation test completed successfully!")
    except Exception as e:
        logger.error(f"❌ Simple navigation test failed: {e}")


def test_website_summarization():
    """Test website summarization with scrolling"""
    logger.info("\n" + "="*60)
    logger.info("TESTING WEBSITE SUMMARIZATION WITH SCROLLING")
    logger.info("="*60)

    objective = "Go to https://octifytechnologies.com/ and summarize their website by scrolling through the page"

    try:
        agent = AutoSurferAgent(objective=objective,
                                headless=False, max_retries=3)
        agent.run()
        logger.info("✅ Website summarization test completed successfully!")
    except Exception as e:
        logger.error(f"❌ Website summarization test failed: {e}")


def main():
    """Run all tests"""
    logger.info("🚀 AutoSurfer Enhanced Accuracy Test Suite")
    logger.info("This demonstrates the improvements made for better accuracy")

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("❌ OPENAI_API_KEY environment variable is required")
        logger.error(
            "Please set it with: export OPENAI_API_KEY='your-api-key'")
        return

    # Run tests
    tests = [
        # test_simple_navigation,
        # test_httpbin_form,
        # test_wikipedia_navigation,
        # test_google_search,
        test_website_summarization,
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
    logger.info("TEST SUITE COMPLETED")
    logger.info("="*60)


if __name__ == "__main__":
    main()
