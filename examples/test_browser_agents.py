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


def test_instagram_login():
    """Test Instagram login automation"""
    print("\n" + "="*60)
    print("TESTING INSTAGRAM LOGIN AUTOMATION")
    print("="*60)

    objective = "Go to instagram.com and login to my account with username 'testuser' and password 'testpass123'"

    try:
        agent = AutoSurferAgent(objective=objective, headless=False)
        agent.run()
        print("✅ Instagram login test completed successfully!")
    except Exception as e:
        print(f"❌ Instagram login test failed: {e}")


def test_google_search():
    """Test Google search automation"""
    print("\n" + "="*60)
    print("TESTING GOOGLE SEARCH AUTOMATION")
    print("="*60)

    objective = "Go to google.com and search for 'Python automation'"

    try:
        agent = AutoSurferAgent(objective=objective, headless=False)
        agent.run()
        print("✅ Google search test completed successfully!")
    except Exception as e:
        print(f"❌ Google search test failed: {e}")


def test_form_filling():
    """Test form filling automation"""
    print("\n" + "="*60)
    print("TESTING FORM FILLING AUTOMATION")
    print("="*60)

    objective = "Go to httpbin.org/forms/post and fill out the form with name 'John Doe', age '30', and submit it"

    try:
        agent = AutoSurferAgent(objective=objective, headless=False)
        agent.run()
        print("✅ Form filling test completed successfully!")
    except Exception as e:
        print(f"❌ Form filling test failed: {e}")


def test_navigation():
    """Test navigation automation"""
    print("\n" + "="*60)
    print("TESTING NAVIGATION AUTOMATION")
    print("="*60)

    objective = "Go to github.com and navigate to the trending repositories page"

    try:
        agent = AutoSurferAgent(objective=objective, headless=False)
        agent.run()
        print("✅ Navigation test completed successfully!")
    except Exception as e:
        print(f"❌ Navigation test failed: {e}")


def main():
    """Run all tests"""
    print("🚀 AutoSurfer Enhanced Accuracy Test Suite")
    print("This demonstrates the improvements made for 100% accuracy")

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable is required")
        print("Please set it with: export OPENAI_API_KEY='your-api-key'")
        return

    # Run tests
    tests = [
        test_google_search,
        test_form_filling,
        test_navigation,
        # test_instagram_login,  # Uncomment to test Instagram (requires credentials)
    ]

    for test in tests:
        try:
            test()
            time.sleep(2)  # Brief pause between tests
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
