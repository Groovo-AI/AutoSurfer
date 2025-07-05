# autosurfer/agent/browser_agent.py
from autosurfer.logger import logger
from autosurfer.agent.brain.task_planner import next_action
from autosurfer.agent.brain.memory import AgentMemory, MemoryEntry
from autosurfer.agent.browser.manager import BrowserManager, BrowserSettings
from autosurfer.agent.browser.action_executor import BrowserActionExecutor
from autosurfer.agent.browser.captcha_handler import CaptchaHandler
import time
from typing import List, Dict, Any
import re


class AutoSurferAgent:
    def __init__(self, objective: str, headless: bool = False, max_retries: int = 3, enable_memory: bool = False):
        self.objective = objective
        self.headless = headless
        self.max_retries = max_retries
        self.enable_memory = enable_memory
        self.browser_settings = BrowserSettings(
            stealth_mode=True,
            headless=headless
        )
        self.browser_session = BrowserManager(
            settings=self.browser_settings
        )
        self.memory = AgentMemory(
            objective=objective) if enable_memory else None

        # Simple heuristic: extract target click text for done detection
        self._click_target = None
        click_match = re.search(
            r"click\b.*?[\"']([^\"']+?)[\"']", objective, re.IGNORECASE)
        if click_match:
            self._click_target = click_match.group(1).lower()
            logger.debug(f"Click target detected: {self._click_target}")

    def run(self):
        logger.info(f"🎯 Objective: {self.objective}")
        executor = BrowserActionExecutor(
            page=self.browser_session.page,
            browser_session=self.browser_session.browser
        )

        # Initialize captcha handler
        captcha_handler = CaptchaHandler(self.browser_session.page)

        try:
            retry_count = 0
            consecutive_failures = 0
            action_count = 0  # Simple counter for non-memory mode

            while True:
                # Get current page state
                current_url = self.browser_session.page.url
                page_title = self.browser_session.page.title()
                logger.info(f"📍 Current URL: {current_url}")
                logger.info(f"📄 Page Title: {page_title}")

                # Check for captcha before proceeding
                if not captcha_handler.handle_captcha_detection():
                    logger.error("❌ Task terminated due to captcha detection")
                    break

                # Get UI elements
                ui_elements = executor.annotate_ui()

                # Add page context to memory
                page_context = {
                    "url": current_url,
                    "title": page_title,
                    "timestamp": time.time(),
                    "retry_count": retry_count,
                    "consecutive_failures": consecutive_failures
                }

                # Plan next action
                plan = next_action(
                    objective=self.objective,
                    ui_elements=ui_elements,
                    memory=self.memory,
                    page_context=page_context
                )

                # Execute action with retry logic
                execution_success = False
                error_message = None
                for attempt in range(self.max_retries):
                    try:
                        executor.execute(plan)
                        execution_success = True
                        consecutive_failures = 0
                        logger.info(
                            f"✅ Action executed successfully on attempt {attempt + 1}")

                        # If the plan started with a navigation, log new URL/title
                        if any(it.action.type == "goto" for it in plan.actions):
                            new_url = self.browser_session.page.url
                            new_title = self.browser_session.page.title()
                            logger.info(f"📍 URL after navigation: {new_url}")
                            logger.info(
                                f"📄 Title after navigation: {new_title}")

                        break
                    except Exception as e:
                        error_message = str(e)
                        logger.warn(f"❌ Attempt {attempt + 1} failed: {e}")

                        # Check if failure might be due to captcha
                        if not captcha_handler.handle_captcha_detection():
                            logger.error(
                                "❌ Task terminated due to captcha detection after action failure")
                            break

                        if attempt < self.max_retries - 1:
                            time.sleep(1)  # Brief pause before retry
                        else:
                            consecutive_failures += 1
                            logger.error(
                                f"❌ All retry attempts failed for action: {e}")

                # If captcha was detected, break out of the loop
                if not execution_success and not captcha_handler.handle_captcha_detection():
                    break

                # Create memory entry
                action_description = self._get_action_description(plan)
                memory_entry = MemoryEntry(
                    timestamp=time.time(),
                    action_type=self._get_primary_action_type(plan),
                    description=action_description,
                    success=execution_success,
                    page_url=current_url,
                    page_title=str(page_title),
                    attempts=attempt + 1 if not execution_success else 1,
                    error_message=error_message,
                    ui_elements_count=len(ui_elements)
                )

                # Add to memory if enabled
                if self.memory:
                    self.memory.add_entry(memory_entry)

                    # Build concise memory snapshot
                    snapshot = self.memory.get_progress_context()
                    extra = []
                    if self.memory.accomplishments:
                        extra.append(
                            f"Accomplishments: {len(self.memory.accomplishments)}")
                    if self.memory.failures:
                        extra.append(f"Failures: {len(self.memory.failures)}")
                    if extra:
                        snapshot += "\n" + " | ".join(extra)

                    logger.info(f"[MEM] {snapshot}")
                else:
                    action_count += 1

                # Heuristic: if we clicked the target link successfully, mark task done
                if self._click_target:
                    for item in plan.actions:
                        if item.action.type == "click" and self._click_target in str(item.action.selector).lower():
                            logger.info(
                                "✅ Detected target link clicked. Task completed.")
                            return  # Exit run method

                # Check if task is complete
                if hasattr(plan, 'actions') and any(item.action.type == "done" for item in plan.actions):
                    logger.info("✅ Task completed by agent.")
                    break

                # Check for too many consecutive failures
                if consecutive_failures >= 3:
                    logger.error(
                        "Too many consecutive failures. Stopping agent.")
                    break

                # Check if agent is stuck using memory system
                if self.memory and self.memory.is_stuck():
                    logger.warn(
                        "Agent appears to be stuck in a loop. Stopping agent.")
                    break

                # Simple loop detection without memory
                if not self.memory and action_count > 10:
                    logger.warn(
                        "Agent has performed many actions. Stopping to prevent infinite loop.")
                    break

                # Simple delay
                time.sleep(2)

        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            raise
        finally:
            logger.info("Agent execution finished!")
            self.browser_session.close()

    def _get_action_description(self, plan) -> str:
        """Extract a human-readable description of the planned actions"""
        descriptions = []
        if not hasattr(plan, 'actions'):
            return "Unknown action"

        for item in plan.actions:
            if item.action.type == "goto":
                descriptions.append(f"Navigate to {item.action.url}")
            elif item.action.type == "click":
                descriptions.append(f"Click {item.action.selector}")
            elif item.action.type == "fill":
                descriptions.append(
                    f"Fill {item.action.selector} with {item.action.value}")
            elif item.action.type == "done":
                descriptions.append(f"Complete task: {item.action.summary}")
            else:
                descriptions.append(f"{item.action.type}: {item.thought}")

        return "; ".join(descriptions)

    def _get_primary_action_type(self, plan) -> str:
        """Get the primary action type from the plan"""
        if not hasattr(plan, 'actions') or not plan.actions:
            return "unknown"

        # Prioritize done action
        for item in plan.actions:
            if item.action.type == "done":
                return "done"

        # Return the first action type
        return plan.actions[0].action.type
