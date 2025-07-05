# autosurfer/agent/browser_agent.py
from autosurfer.logger import logger
from autosurfer.agent.brain.task_planner import next_action
from autosurfer.agent.browser.manager import BrowserManager, BrowserSettings
from autosurfer.agent.browser.action_executor import BrowserActionExecutor
from autosurfer.agent.browser.captcha_handler import CaptchaHandler
import time
from typing import List, Dict, Any


class AutoSurferAgent:
    def __init__(self, objective: str, headless: bool = False, max_retries: int = 3):
        self.objective = objective
        self.headless = headless
        self.max_retries = max_retries
        self.browser_settings = BrowserSettings(
            stealth_mode=True,
            headless=headless
        )
        self.browser_session = BrowserManager(
            settings=self.browser_settings
        )

    def run(self):
        logger.info(f"🎯 Objective: {self.objective}")
        memory = []
        executor = BrowserActionExecutor(
            page=self.browser_session.page,
            browser_session=self.browser_session.browser
        )

        # Initialize captcha handler
        captcha_handler = CaptchaHandler(self.browser_session.page)

        try:
            retry_count = 0
            consecutive_failures = 0

            while True:
                # Get current page state
                current_url = self.browser_session.page.url
                page_title = self.browser_session.page.title

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
                    memory=memory,
                    page_context=page_context
                )

                logger.info(f"[Agent Plan] {plan}")

                # Execute action with retry logic
                execution_success = False
                for attempt in range(self.max_retries):
                    try:
                        executor.execute(plan)
                        execution_success = True
                        consecutive_failures = 0
                        break
                    except Exception as e:
                        logger.warn(f"Attempt {attempt + 1} failed: {e}")

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
                                f"All retry attempts failed for action: {e}")

                # If captcha was detected, break out of the loop
                if not execution_success and not captcha_handler.handle_captcha_detection():
                    break

                # Add to memory
                execution_result = {
                    "plan": plan,
                    "success": execution_success,
                    "page_context": page_context,
                    "attempts": attempt + 1 if not execution_success else 1
                }
                memory.append(execution_result)

                # Check if task is complete
                if any(item.action.type == "done" for item in plan.actions):
                    logger.info("✅ Task completed by agent.")
                    break

                # Check for too many consecutive failures
                if consecutive_failures >= 3:
                    logger.error(
                        "Too many consecutive failures. Stopping agent.")
                    break

                # Check for infinite loops (same action repeated too many times)
                if len(memory) > 10:
                    recent_actions = [m["plan"] for m in memory[-5:]]
                    if len(set(str(action) for action in recent_actions)) <= 2:
                        logger.warn(
                            "Detected potential infinite loop. Stopping agent.")
                        break

                # Simple delay
                time.sleep(2)

        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            raise
        finally:
            logger.info("Agent execution finished!")
            self.browser_session.close()
