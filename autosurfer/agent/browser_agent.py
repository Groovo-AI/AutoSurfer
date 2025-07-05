# autosurfer/agent/browser_agent.py
from autosurfer.logger import logger
from autosurfer.agent.brain.task_planner import next_action
from autosurfer.agent.browser.manager import BrowserManager, BrowserSettings
from autosurfer.agent.browser.action_executor import BrowserActionExecutor
import time
from typing import List, Dict, Any


class AutoSurferAgent:
    def __init__(self, objective: str, headless: bool = False):
        self.objective = objective
        self.headless = headless
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

        try:
            while True:
                # Get current page state
                current_url = self.browser_session.page.url
                page_title = self.browser_session.page.title

                # Get UI elements
                ui_elements = executor.annotate_ui()

                # Add page context to memory
                page_context = {
                    "url": current_url,
                    "title": page_title,
                    "timestamp": time.time()
                }

                # Plan next action
                plan = next_action(
                    objective=self.objective,
                    ui_elements=ui_elements,
                    memory=memory,
                    page_context=page_context
                )

                logger.info(f"[Agent Plan] {plan}")

                # Execute action
                try:
                    executor.execute(plan)
                except Exception as e:
                    logger.error(f"Failed to execute action: {e}")
                    break

                # Add to memory
                execution_result = {
                    "plan": plan,
                    "success": True,
                    "page_context": page_context
                }
                memory.append(execution_result)

                # Check if task is complete
                if any(item.action.type == "done" for item in plan.actions):
                    logger.info("✅ Task completed by agent.")
                    break

                # Simple delay
                time.sleep(2)

        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            raise
        finally:
            logger.info("Agent execution finished!")
            self.browser_session.close()
