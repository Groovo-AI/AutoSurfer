# autosurf/agent/executor/core.py
import time
from typing import List, Dict, Any, Sequence
import random
import pyautogui
import string
from autosurfer.logger import logger


class OsActionExecutor:
    """
    Execute a list of UI-automation steps produced by Autosurf.

    Each list item must look like:
    {
        "thought": "...",
        "action": {
            "type":  "press" | "type" | "click" | "move" | "drag" | "scroll" | "wait" | "done",
            ...params...
        }
    }
    """

    # --------------------------------------------------------------- #
    # Construction
    # --------------------------------------------------------------- #
    def __init__(self, actions: Sequence[Dict[str, Any]], delay_between: float = 0.8):
        self.actions: List[Dict[str, Any]] = list(actions)
        self.delay: float = delay_between

        # Fail fast if PyAutoGUI cannot read the screen (common on macOS until
        # the user grants screen-recording + accessibility rights).
        try:
            pyautogui.size()
        except Exception as exc:
            raise RuntimeError(
                "PyAutoGUI cannot access the screen. On macOS, enable "
                "System Settings → Privacy & Security → Screen Recording & Accessibility."
            ) from exc

        # PyAutoGUI safety: move mouse to a corner to abort
        pyautogui.FAILSAFE = True

    # --------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------- #
    def execute(self) -> None:
        """
        Run the action list from top to bottom.
        Stops immediately on a 'done' action.
        """
        for step in self.actions:
            thought: str = step.get("thought", "")
            action: Dict[str, Any] = step.get("action", {}) or {}

            logger.info(f"[Agent Thought] {thought}")
            logger.info(f"[Agent Action] {action}")

            action_type: str = action.get("type", "")
            handler = self._get_handler(action_type)

            if handler is None:
                logger.info(f"[Warning] Unknown action type: {action_type!r}")
            else:
                handler(action)

            # 'wait' and 'done' include their own timing / exit behaviour
            if action_type not in {"wait", "done"}:
                time.sleep(self.delay)

            # stop after done (handler already logger.infoed summary)
            if action_type == "done":
                break

    # --------------------------------------------------------------- #
    # Handler lookup
    # --------------------------------------------------------------- #
    def _get_handler(self, action_type: str):
        """Return the bound handler method or None."""
        return getattr(self, f"_handle_{action_type}", None)

    # --------------------------------------------------------------- #
    # Individual handlers
    # --------------------------------------------------------------- #
    def _handle_press(self, action: Dict[str, Any]) -> None:
        # keys may come as ["ctrl","s"] or {"key":"enter"}
        keys = action.get("keys") or (
            [action["key"]] if action.get("key") else [])
        if not keys:
            logger.info("[Error] press action missing 'keys'")
            return

        hold_ms = action.get("hold_ms", 0)
        if hold_ms:
            logger.info(f"→ Holding {keys} for {hold_ms} ms")
            for k in keys:
                pyautogui.keyDown(k)
            time.sleep(hold_ms / 1000)
            for k in reversed(keys):
                pyautogui.keyUp(k)
        else:
            logger.info(f"→ Pressing hotkey {keys}")
            pyautogui.hotkey(*keys)

    def _handle_type(self, action: Dict[str, Any]) -> None:
        """
        Type text like a real user:
        • variable delay per character
        • longer pause after whitespace / punctuation
        • optional 'typo' simulation
        """
        text: str = action.get("text", "")
        if not text:
            logger.info("[Error] type action missing 'text'")
            return

        # Allow per-action overrides; else default human-ish cadence
        min_delay: float = float(action.get("min_delay", 0.05))  # seconds
        max_delay: float = float(action.get("max_delay", 0.18))
        typo_rate: float = float(action.get(
            "typo_rate", 0.0))   # 0-1 (e.g. 0.02)

        logger.info(f"→ Typing (human-style): {text!r}")

        def random_delay(char: str) -> float:
            """
            Fast for normal letters, slower after whitespace / punctuation.
            """
            base = random.uniform(min_delay, max_delay)
            if char in {" ", "\t"}:
                return base + 0.15        # think after a word
            if char in {".", "?", "!"}:
                return base + 0.25        # think after sentence
            if char in {",", ";", ":"}:
                return base + 0.10
            return base

        # Helper to press a single character (pyautogui.write handles case)
        def press_char(c: str):
            pyautogui.write(c)

        for idx, char in enumerate(text):
            # Occasionally introduce a typo and correct it
            if typo_rate and random.random() < typo_rate and char.isalpha():
                wrong_char = random.choice(string.ascii_lowercase)
                press_char(wrong_char)
                time.sleep(random_delay(wrong_char))
                pyautogui.press("backspace")
                time.sleep(random_delay("\b"))

            press_char(char)
            time.sleep(random_delay(char))

    def _handle_click(self, action: Dict[str, Any]) -> None:
        button = action.get("button", "left")
        clicks = int(action.get("count", 1))
        mods = action.get("modifiers", [])
        coords = action.get("coords")
        # Not used here—but kept for future image-locate flow
        target = action.get("target")

        coord_str = f"at {coords}" if coords else "(current position)"
        logger.info(
            f"→ {button.title()}-click {clicks}× {coord_str} with modifiers {mods or 'none'}")

        # Hold modifier keys first
        for m in mods:
            pyautogui.keyDown(m)

        if coords:
            x, y = coords
            pyautogui.click(x=x, y=y, clicks=clicks, button=button)
        else:
            pyautogui.click(clicks=clicks, button=button)

        # Release modifiers
        for m in reversed(mods):
            pyautogui.keyUp(m)

    def _handle_move(self, action: Dict[str, Any]) -> None:
        coords = action.get("coords")
        if coords is None:
            logger.info("[Error] move action missing 'coords'")
            return
        duration = action.get("duration_ms", 0) / 1000
        x, y = coords
        logger.info(f"→ Moving mouse to {x},{y} over {duration:.3f}s")
        pyautogui.moveTo(x, y, duration=duration)

    def _handle_drag(self, action: Dict[str, Any]) -> None:
        end = action.get("end")
        if end is None:
            logger.info("[Error] drag action missing 'end'")
            return
        start = action.get("start")
        button = action.get("button", "left")
        duration = action.get("duration_ms", 0) / 1000

        # Move to start if supplied
        if start is not None:
            pyautogui.moveTo(start[0], start[1], duration=0)

        logger.info(f"→ Dragging to {end} with {button} over {duration:.3f}s")
        pyautogui.dragTo(end[0], end[1], duration=duration, button=button)

    def _handle_scroll(self, action: Dict[str, Any]) -> None:
        dx = int(action.get("dx", 0))
        dy = int(action.get("dy", 0))
        duration = action.get("duration_ms", 0) / 1000

        logger.info(f"→ Scrolling dx={dx} dy={dy} over {duration:.3f}s")
        if dx:
            # Horizontal scroll (might not work on all platforms)
            pyautogui.hscroll(dx)
        if dy:
            pyautogui.scroll(dy)
        if duration:
            time.sleep(duration)

    def _handle_wait(self, action: Dict[str, Any]) -> None:
        seconds = float(action.get("seconds", 0))
        logger.info(f"→ Waiting {seconds} s")
        time.sleep(seconds)

    def _handle_done(self, action: Dict[str, Any]) -> None:
        summary = action.get("summary", "<no summary provided>")
        logger.info(f"[DONE] {summary}")
