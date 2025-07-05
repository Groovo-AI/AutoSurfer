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

# Add the autosurfer package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_httpbin_form():
    """Test form filling automation on httpbin"""
    print("\n" + "="*60)
    print("TESTING HTTPBIN FORM FILLING AUTOMATION")
    print("="*60)

    objective = "Go to httpbin.org/forms/post and fill out the form with name 'John Doe', age '30', and submit it"

    try:
        agent = AutoSurferAgent(objective=objective,
                                headless=False, max_retries=3)
        agent.run()
        print("✅ HTTPBin form test completed successfully!")
    except Exception as e:
        print(f"❌ HTTPBin form test failed: {e}")


def test_google_search():
    """Test Google search automation"""
    print("\n" + "="*60)
    print("TESTING GOOGLE SEARCH AUTOMATION")
    print("="*60)

    objective = "Go to google.com and search for 'Python automation'"

    try:
        agent = AutoSurferAgent(objective=objective,
                                headless=False, max_retries=3)
        agent.run()
        print("✅ Google search test completed successfully!")
    except Exception as e:
        print(f"❌ Google search test failed: {e}")


def test_wikipedia_navigation():
    """Test Wikipedia navigation automation"""
    print("\n" + "="*60)
    print("TESTING WIKIPEDIA NAVIGATION AUTOMATION")
    print("="*60)

    objective = "Go to wikipedia.org and search for 'Python programming language'"

    try:
        agent = AutoSurferAgent(objective=objective,
                                headless=False, max_retries=3)
        agent.run()
        print("✅ Wikipedia navigation test completed successfully!")
    except Exception as e:
        print(f"❌ Wikipedia navigation test failed: {e}")


def test_simple_navigation():
    """Test simple navigation automation"""
    print("\n" + "="*60)
    print("TESTING SIMPLE NAVIGATION AUTOMATION")
    print("="*60)

    objective = "Go to example.com and verify the page loads"

    try:
        agent = AutoSurferAgent(objective=objective,
                                headless=False, max_retries=3)
        agent.run()
        print("✅ Simple navigation test completed successfully!")
    except Exception as e:
        print(f"❌ Simple navigation test failed: {e}")


def main():
    """Run all tests"""
    print("🚀 AutoSurfer Enhanced Accuracy Test Suite")
    print("This demonstrates the improvements made for better accuracy")

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable is required")
        print("Please set it with: export OPENAI_API_KEY='your-api-key'")
        return

    # Run tests
    tests = [
        test_simple_navigation,
        test_httpbin_form,
        test_wikipedia_navigation,
        test_google_search,
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
    print("TEST SUITE COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()
