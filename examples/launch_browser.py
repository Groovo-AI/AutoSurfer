#!/usr/bin/env python3
"""
Simple example to demonstrate AutoSurfer browser automation improvements.
"""

from autosurfer.agent.browser_agent import AutoSurferAgent
import os
import sys
from pathlib import Path

# Add the autosurfer package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Run a simple browser automation example"""

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable is required")
        print("Please set it with: export OPENAI_API_KEY='your-api-key'")
        return

    # Simple test objective
    objective = "Go to example.com and verify the page loads successfully"

    print("🚀 Starting AutoSurfer Browser Agent")
    print(f"Objective: {objective}")
    print("=" * 60)

    try:
        # Create and run the agent
        agent = AutoSurferAgent(
            objective=objective,
            headless=False,  # Set to True for headless mode
            max_retries=3
        )

        agent.run()

        print("✅ Browser automation completed successfully!")

    except KeyboardInterrupt:
        print("\n⏹️  Automation interrupted by user")
    except Exception as e:
        print(f"❌ Automation failed: {e}")


if __name__ == "__main__":
    main()
