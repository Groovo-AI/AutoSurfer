#!/usr/bin/env python3
"""
Test script to demonstrate AutoSurfer agent memory functionality.

This script shows the difference between running the agent with memory enabled vs disabled.
"""

from autosurfer.logger import logger
from autosurfer.agent.browser_agent import AutoSurferAgent
import time
import sys
import os

# Add the parent directory to the path so we can import autosurfer
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_memory_disabled():
    """Test agent without memory enabled"""
    print("\n" + "="*60)
    print("🧠 TESTING AGENT WITHOUT MEMORY")
    print("="*60)

    objective = "Go to https://example.com and click on the 'More information...' link"

    print(f"Objective: {objective}")
    print("Memory: DISABLED")
    print("Expected: Basic functionality, no memory tracking")

    try:
        agent = AutoSurferAgent(
            objective=objective,
            headless=False,  # Run in visible mode for testing
            enable_memory=False
        )

        print("\nStarting agent without memory...")
        start_time = time.time()
        agent.run()
        end_time = time.time()

        print(f"\n✅ Agent completed in {end_time - start_time:.2f} seconds")
        print("Memory was disabled, so no memory tracking occurred")

    except Exception as e:
        print(f"❌ Agent failed: {e}")


def test_memory_enabled():
    """Test agent with memory enabled"""
    print("\n" + "="*60)
    print("🧠 TESTING AGENT WITH MEMORY ENABLED")
    print("="*60)

    objective = "Go to https://example.com and click on the 'More information...' link"

    print(f"Objective: {objective}")
    print("Memory: ENABLED")
    print("Expected: Enhanced functionality with memory tracking")

    try:
        agent = AutoSurferAgent(
            objective=objective,
            headless=False,  # Run in visible mode for testing
            enable_memory=True
        )

        print("\nStarting agent with memory...")
        start_time = time.time()
        agent.run()
        end_time = time.time()

        print(f"\n✅ Agent completed in {end_time - start_time:.2f} seconds")

        # Display memory information
        if agent.memory:
            print("\n📊 MEMORY SUMMARY:")
            print(f"Total actions: {len(agent.memory.entries)}")
            print(f"Accomplishments: {len(agent.memory.accomplishments)}")
            print(f"Failures: {len(agent.memory.failures)}")
            print(f"Current progress: {agent.memory.current_progress}")

            if agent.memory.entries:
                print("\n📝 RECENT ACTIONS:")
                for i, entry in enumerate(agent.memory.entries[-3:], 1):
                    status = "✅" if entry.success else "❌"
                    print(
                        f"  {i}. {status} {entry.action_type}: {entry.description}")
                    if not entry.success and entry.error_message:
                        print(f"     Error: {entry.error_message}")

    except Exception as e:
        print(f"❌ Agent failed: {e}")


def test_memory_comparison():
    """Compare memory enabled vs disabled on the same task"""
    print("\n" + "="*60)
    print("🔄 MEMORY COMPARISON TEST")
    print("="*60)

    objective = "Go to https://httpbin.org/status/200 and verify the page loads"

    print(f"Objective: {objective}")
    print("This test will run the same task with and without memory")

    # Test without memory
    print("\n--- WITHOUT MEMORY ---")
    try:
        agent_no_memory = AutoSurferAgent(
            objective=objective,
            headless=False,
            enable_memory=False
        )
        start_time = time.time()
        agent_no_memory.run()
        no_memory_time = time.time() - start_time
        print(f"✅ Completed in {no_memory_time:.2f} seconds")
    except Exception as e:
        print(f"❌ Failed: {e}")
        no_memory_time = None

    # Test with memory
    print("\n--- WITH MEMORY ---")
    try:
        agent_with_memory = AutoSurferAgent(
            objective=objective,
            headless=False,
            enable_memory=True
        )
        start_time = time.time()
        agent_with_memory.run()
        with_memory_time = time.time() - start_time
        print(f"✅ Completed in {with_memory_time:.2f} seconds")

        if agent_with_memory.memory:
            print(
                f"📊 Memory tracked {len(agent_with_memory.memory.entries)} actions")

    except Exception as e:
        print(f"❌ Failed: {e}")
        with_memory_time = None

    # Comparison
    if no_memory_time and with_memory_time:
        print(f"\n📈 COMPARISON:")
        print(f"Without memory: {no_memory_time:.2f}s")
        print(f"With memory: {with_memory_time:.2f}s")
        difference = with_memory_time - no_memory_time
        print(
            f"Difference: {difference:+.2f}s ({difference/no_memory_time*100:+.1f}%)")


def main():
    """Main test function"""
    print("🧠 AutoSurfer Agent Memory Test Suite")
    print("This script demonstrates the memory functionality of the AutoSurfer agent.")

    # Check if we should run all tests or just one
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        if test_type == "disabled":
            test_memory_disabled()
        elif test_type == "enabled":
            test_memory_enabled()
        elif test_type == "comparison":
            test_memory_comparison()
        else:
            print(f"Unknown test type: {test_type}")
            print("Available tests: disabled, enabled, comparison")
    else:
        # Run all tests
        test_memory_disabled()
        test_memory_enabled()
        test_memory_comparison()

    print("\n" + "="*60)
    print("🎉 Memory test suite completed!")
    print("="*60)


if __name__ == "__main__":
    main()
