from autosurfer.logger import logger
from autosurfer.agent.brain.task_planner import next_action
from autosurfer.agent.brain.memory import AgentMemory, MemoryEntry
from autosurfer.agent.browser.adapters import BrowserAdapter, BrowserSettings, create_browser_adapter
from autosurfer.config import Config
from autosurfer.agent.browser.action_executor import BrowserActionExecutor
from autosurfer.agent.browser.captcha_handler import CaptchaHandler
import time
from typing import List, Dict, Any, Optional
import re
import hashlib


class AutoSurferAgent:
    def __init__(self, objective: str, browser_session: BrowserAdapter, max_retries: int = 3, enable_memory: bool = False):
        self.objective = objective
        self.browser_session = browser_session
        self.max_retries = max_retries
        self.enable_memory = enable_memory

        self.memory = AgentMemory(
            objective=objective) if enable_memory else None

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
                final_url = current_url  # Default to current URL
                final_title = page_title  # Default to current title

                for attempt in range(self.max_retries):
                    # Capture current state for this attempt
                    attempt_url = self.browser_session.page.url
                    attempt_title = self.browser_session.page.title()

                    try:
                        executor.execute(plan)
                        execution_success = True
                        consecutive_failures = 0
                        logger.info(
                            f"✅ Action executed successfully on attempt {attempt + 1}")

                        # Capture final URL and title after successful action
                        final_url = self.browser_session.page.url
                        final_title = self.browser_session.page.title()

                        # If the plan started with a navigation, log new URL/title
                        if any(it.action.type == "goto" for it in plan.actions):
                            logger.info(f"📍 URL after navigation: {final_url}")
                            logger.info(
                                f"📄 Title after navigation: {final_title}")

                        # Log successful attempt immediately
                        self._log_memory_entry(
                            plan=plan,
                            success=True,
                            page_url=final_url,
                            page_title=final_title,
                            attempt_number=attempt + 1,
                            error_message=None,
                            ui_elements=ui_elements,
                            executor=executor
                        )
                        break

                    except Exception as e:
                        error_message = str(e)
                        logger.warn(f"❌ Attempt {attempt + 1} failed: {e}")

                        # Log failed attempt immediately
                        self._log_memory_entry(
                            plan=plan,
                            success=False,
                            page_url=attempt_url,
                            page_title=attempt_title,
                            attempt_number=attempt + 1,
                            error_message=error_message,
                            ui_elements=ui_elements,
                            executor=executor
                        )

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

                # If the action we just executed could spawn a captcha overlay, invalidate the captcha cache so the next loop re-checks.
                if execution_success and any(it.action.type in {"click", "fill", "press"} for it in plan.actions):
                    captcha_handler.invalidate_cache()

                # If captcha was detected, break out of the loop
                if not execution_success and not captcha_handler.handle_captcha_detection():
                    break

                # Update action count for non-memory mode
                if not self.memory:
                    action_count += 1

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

    def _log_memory_entry(self, plan, success, page_url, page_title, attempt_number, error_message, ui_elements, executor):
        """Log a memory entry in real-time and save memory immediately"""
        if not self.memory:
            return

        action_description = self._get_action_description(plan)

        # --- Capture signals for robust loop detection ---
        try:
            # DOM hash
            dom_html = executor.page.evaluate("() => document.body.innerHTML")
            dom_hash = hashlib.sha256(dom_html.encode(
                "utf-8")).hexdigest() if dom_html else None
            # UI state hash (hash the stringified list of UI elements)
            ui_state_str = str(ui_elements)
            ui_state_hash = hashlib.sha256(ui_state_str.encode(
                "utf-8")).hexdigest() if ui_state_str else None
            # Scroll position
            scroll_info = executor.get_scroll_info() if hasattr(
                executor, 'get_scroll_info') else None
            scroll_position = scroll_info["scrollY"] if scroll_info and "scrollY" in scroll_info else None
        except Exception as e:
            logger.debug(f"Failed to capture some signals: {e}")
            dom_hash = None
            ui_state_hash = None
            scroll_position = None

        # --- End capture signals ---

        memory_entry = MemoryEntry(
            timestamp=time.time(),
            action_type=self._get_primary_action_type(plan),
            description=action_description,
            success=success,
            page_url=page_url,
            page_title=str(page_title),
            attempts=attempt_number,
            error_message=error_message,
            ui_elements_count=len(ui_elements),
            dom_hash=dom_hash,
            ui_state_hash=ui_state_hash,
            scroll_position=scroll_position,
            retry_count=attempt_number
        )

        # Add to memory immediately
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

        # Save memory to file immediately after each attempt
        try:
            self.memory.save_to_file()
        except Exception as e:
            logger.debug(f"Failed to save memory to file: {e}")

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
