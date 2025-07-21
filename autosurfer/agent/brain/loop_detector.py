from typing import List, Any
import logging


class LoopDetector:
    """Very small loop-detection helper.

    – Look at the last `window` entries (default 6).  
    – Build a fingerprint “url|title|action|desc” for each.  
    – If ≤ `distinct_threshold` (default 2) different fingerprints *and*
      no “done” action → we’re stuck.
    """

    def __init__(self, window: int = 6, distinct_threshold: int = 2):
        self.window = window
        self.distinct_threshold = distinct_threshold

    def is_stuck(self, entries: List[Any]) -> bool:
        if len(entries) < self.window:
            return False

        recent = entries[-self.window:]

        # any ‘done’ means progress → not stuck
        if any(getattr(e, "action_type", "") == "done" for e in recent):
            return False

        # Composite fingerprint: url, title, action, desc, dom_hash, ui_state_hash, scroll_position, retry_count
        fingerprints = [
            f"{getattr(e,'page_url','')}|{getattr(e,'page_title','')}|"
            f"{getattr(e,'action_type','')}|{getattr(e,'description','')}|"
            f"{getattr(e,'dom_hash',None)}|{getattr(e,'ui_state_hash',None)}|"
            f"{getattr(e,'scroll_position',None)}|{getattr(e,'retry_count',None)}"
            for e in recent
        ]
        unique_fingerprints = set(fingerprints)
        if len(unique_fingerprints) == 1:
            logging.warning(
                f"[LoopDetector] Agent flagged as stuck: repeated fingerprint '{fingerprints[0]}' for last {self.window} actions."
            )
            for idx, entry in enumerate(recent, 1):
                logging.warning(f"[LoopDetector] Action {idx}: {entry}")
            return True
        return False
