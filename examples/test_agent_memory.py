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

# Use logger.info directly instead of print


def test_memory_disabled():
    """Test agent without memory enabled"""
    logger.info("\n" + "="*60)
    logger.info("🧠 TESTING AGENT WITHOUT MEMORY")
    logger.info("="*60)

    objective = "Go to https://example.com and click on the 'More information...' link"

    logger.info(f"Objective: {objective}")
    logger.info("Memory: DISABLED")
    logger.info("Expected: Basic functionality, no memory tracking")

    try:
        agent = AutoSurferAgent(
            objective=objective,
            headless=False,  # Run in visible mode for testing
            enable_memory=False
        )

        logger.info("\nStarting agent without memory...")
        start_time = time.time()
        agent.run()
        end_time = time.time()

        logger.info(
            f"\n✅ Agent completed in {end_time - start_time:.2f} seconds")
        logger.info("Memory was disabled, so no memory tracking occurred")

    except Exception as e:
        logger.error(f"Agent failed: {e}")


def test_memory_enabled():
    """Test agent with memory enabled"""
    logger.info("\n" + "="*60)
    logger.info("🧠 TESTING AGENT WITH MEMORY ENABLED")
    logger.info("="*60)

    objective = "Go to https://example.com and click on the 'More information...' link"

    logger.info(f"Objective: {objective}")
    logger.info("Memory: ENABLED")
    logger.info("Expected: Enhanced functionality with memory tracking")

    try:
        agent = AutoSurferAgent(
            objective=objective,
            headless=False,  # Run in visible mode for testing
            enable_memory=True
        )

        logger.info("\nStarting agent with memory...")
        start_time = time.time()
        agent.run()
        end_time = time.time()

        logger.info(
            f"\n✅ Agent completed in {end_time - start_time:.2f} seconds")

        # Display memory information
        if agent.memory:
            logger.info("\n📊 MEMORY SUMMARY:")
            logger.info(f"Total actions: {len(agent.memory.entries)}")
            logger.info(
                f"Accomplishments: {len(agent.memory.accomplishments)}")
            logger.info(f"Failures: {len(agent.memory.failures)}")
            logger.info(f"Current progress: {agent.memory.current_progress}")

            if agent.memory.entries:
                logger.info("\n📝 RECENT ACTIONS:")
                for i, entry in enumerate(agent.memory.entries[-3:], 1):
                    status = "✅" if entry.success else "❌"
                    logger.info(
                        f"  {i}. {status} {entry.action_type}: {entry.description}")
                    if not entry.success and entry.error_message:
                        logger.info(f"     Error: {entry.error_message}")

    except Exception as e:
        logger.error(f"Agent failed: {e}")


def test_memory_comparison():
    """Compare memory enabled vs disabled on the same task"""
    logger.info("\n" + "="*60)
    logger.info("🔄 MEMORY COMPARISON TEST")
    logger.info("="*60)

    objective = "Go to https://httpbin.org/status/200 and verify the page loads"

    logger.info(f"Objective: {objective}")
    logger.info("This test will run the same task with and without memory")

    # Test without memory
    logger.info("\n--- WITHOUT MEMORY ---")
    try:
        agent_no_memory = AutoSurferAgent(
            objective=objective,
            headless=False,
            enable_memory=False
        )
        start_time = time.time()
        agent_no_memory.run()
        no_memory_time = time.time() - start_time
        logger.info(f"✅ Completed in {no_memory_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Failed: {e}")
        no_memory_time = None

    # Test with memory
    logger.info("\n--- WITH MEMORY ---")
    try:
        agent_with_memory = AutoSurferAgent(
            objective=objective,
            headless=False,
            enable_memory=True
        )
        start_time = time.time()
        agent_with_memory.run()
        with_memory_time = time.time() - start_time
        logger.info(f"✅ Completed in {with_memory_time:.2f} seconds")

        if agent_with_memory.memory:
            logger.info(
                f"📊 Memory tracked {len(agent_with_memory.memory.entries)} actions")

    except Exception as e:
        logger.error(f"Failed: {e}")
        with_memory_time = None

    # Comparison
    if no_memory_time and with_memory_time:
        logger.info(f"\n📈 COMPARISON:")
        logger.info(f"Without memory: {no_memory_time:.2f}s")
        logger.info(f"With memory: {with_memory_time:.2f}s")
        difference = with_memory_time - no_memory_time
        logger.info(
            f"Difference: {difference:+.2f}s ({difference/no_memory_time*100:+.1f}%)")


def main():
    """Main test function"""
    logger.info("🧠 AutoSurfer Agent Memory Test Suite")
    logger.info(
        "This script demonstrates the memory functionality of the AutoSurfer agent.")

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
            logger.info(f"Unknown test type: {test_type}")
            logger.info("Available tests: disabled, enabled, comparison")
    else:
        # Run all tests
        test_memory_disabled()
        test_memory_enabled()
        test_memory_comparison()

    logger.info("\n" + "="*60)
    logger.info("🎉 Memory test suite completed!")
    logger.info("="*60)


if __name__ == "__main__":
    main()
