# autosurfer/agent/browser_agent.py
from autosurfer.logger import logger
from autosurfer.agent.brain.task_planner import next_action
from autosurfer.agent.browser.action_executor import BrowserActionExecutor


class AutoSurferAgent:
    def __init__(self, objective: str, headless: bool = False):
        self.objective = objective
        self.headless = headless

    def run(self):
        logger.info(f"🎯 Objective: {self.objective}")
        memory = []
        executor = BrowserActionExecutor(headless=self.headless)
        try:
            while True:
                ui_elements = executor.annotate_ui()
                plan = next_action(objective=self.objective,
                                   ui_elements=ui_elements, memory=memory)
                logger.info(f"[Agent Plan] {plan}")
                executor.execute(plan)
                memory.append(plan)
                if any(item.action.type == "done" for item in plan.actions):
                    logger.info("✅ Task completed by agent.")
                    break
        finally:
            executor.close()
