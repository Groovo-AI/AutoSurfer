#!/usr/bin/env python3
"""
Simple example to demonstrate AutoSurfer browser automation improvements.
"""

from autosurfer.agent.browser_agent import AutoSurferAgent
import os
import sys
from pathlib import Path
from autosurfer.logger import logger

# Add the autosurfer package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

# All outputs now use logger directly


def main():
    """Run a simple browser automation example"""

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.info("❌ OPENAI_API_KEY environment variable is required")
        logger.info("Please set it with: export OPENAI_API_KEY='your-api-key'")
        return

    # Simple test objective
    objective = "Go to example.com and verify the page loads successfully"

    logger.info("🚀 Starting AutoSurfer Browser Agent")
    logger.info(f"Objective: {objective}")
    logger.info("=" * 60)

    try:
        # Create and run the agent
        agent = AutoSurferAgent(
            objective=objective,
            headless=False,  # Set to True for headless mode
            max_retries=3
        )

        agent.run()

        logger.info("✅ Browser automation completed successfully!")

    except KeyboardInterrupt:
        logger.info("\n⏹️  Automation interrupted by user")
    except Exception as e:
        logger.error(f"❌ Automation failed: {e}")


if __name__ == "__main__":
    main()
