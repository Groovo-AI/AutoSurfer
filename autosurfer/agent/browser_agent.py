from autosurfer.logger import logger
from autosurfer.agent.brain.task_planner import next_action
from autosurfer.agent.browser.action_executor import BrowserActionExecutor


class AutoSurferAgent:
    """High-level orchestrator -- plans, then delegates real work to BrowserActionExecutor."""

    def __init__(self, objective: str, headless: bool = False):
        self.objective = objective
        self.headless = headless

    def run(self):
        logger.info(f"🎯 Objective: {self.objective}")

        plan = next_action(
            objective=self.objective,
            ui_elements=[],
            memory=None,
        )
        logger.info(f"[Agent Plan] {plan}")
        executor = BrowserActionExecutor(plan, headless=self.headless)
        try:
            executor.execute()
        finally:
            executor.close()
