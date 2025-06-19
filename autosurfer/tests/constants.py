tasks = [
    # ───────────────────  Launch Chrome  ───────────────────
    {
        "thought": "Slide mouse to a screen corner before starting",
        "action": {"type": "move", "coords": [5, 5], "duration_ms": 300}
    },
    {
        "thought": "Brief natural pause",
        "action": {"type": "wait", "seconds": 0.2}
    },
    {
        "thought": "Open Spotlight (⌘ Space)",
        "action": {"type": "press", "keys": ["command", "space"]}
    },
    {
        "thought": "Allow Spotlight field to appear",
        "action": {"type": "wait", "seconds": 0.25}
    },
    {
        "thought": "Type the app name",
        "action": {"type": "type", "text": "Google Chrome"}
    },
    {
        "thought": "Hit ⏎ to launch Chrome",
        "action": {"type": "press", "key": "enter"}
    },
    {
        "thought": "Wait for Chrome window",
        "action": {"type": "wait", "seconds": 3.5}
    },

    # ───────────────────  Navigate to Google Drive  ───────────────────
    {
        "thought": "Open new tab (⌘ T)",
        "action": {"type": "press", "keys": ["command", "t"]}
    },
    {
        "thought": "Natural glance pause",
        "action": {"type": "wait", "seconds": 0.15}
    },
    {
        "thought": "Type Drive URL",
        "action": {"type": "type", "text": "https://drive.google.com/"}
    },
    {
        "thought": "Go to Drive (⏎)",
        "action": {"type": "press", "key": "enter"}
    },
    {
        "thought": "Let Drive load fully",
        "action": {"type": "wait", "seconds": 4}
    },

    # ───────────────────  Open the Upload dialog  ───────────────────
    {
        "thought": "Glide to '+ New' button",
        "action": {"type": "move", "coords": [120, 160], "duration_ms": 350}
    },
    {
        "thought": "Click '+ New'",
        "action": {"type": "click", "button": "left", "count": 1, "coords": [120, 160]}
    },
    {
        "thought": "Wait for dropdown",
        "action": {"type": "wait", "seconds": 0.2}
    },
    {
        "thought": "Move to 'File upload'",
        "action": {"type": "move", "coords": [140, 260], "duration_ms": 200}
    },
    {
        "thought": "Double-click 'File upload'",
        "action": {"type": "click", "button": "left", "count": 2, "coords": [140, 260]}
    },

    # ───────────────────  Choose the PDF  ───────────────────
    {
        "thought": "Wait for system file picker",
        "action": {"type": "wait", "seconds": 1.5}
    },
    {
        "thought": "Hold ⇧ briefly for multi-select realism",
        "action": {"type": "press", "keys": ["shift"], "hold_ms": 500}
    },
    {
        "thought": "Move to PDF file icon",
        "action": {"type": "move", "coords": [200, 500], "duration_ms": 250}
    },
    {
        "thought": "Drag file to browser drop-zone",
        "action": {
            "type": "drag",
            "start": [200, 500],
            "end": [800, 250],
            "button": "left",
            "duration_ms": 600
        }
    },

    # ───────────────────  Monitor upload  ───────────────────
    {
        "thought": "Scroll down slightly to view progress",
        "action": {"type": "scroll", "dx": 0, "dy": -300, "duration_ms": 200}
    },
    {
        "thought": "Scroll sideways to peek at columns (looks human)",
        "action": {"type": "scroll", "dx": 120, "dy": 100, "duration_ms": 200}
    },
    {
        "thought": "Right-click empty space to close any menu",
        "action": {"type": "click", "button": "right", "count": 1, "coords": [400, 500]}
    },

    # ───────────────────  Finish  ───────────────────
    {
        "thought": "Wait until upload completes",
        "action": {"type": "wait", "seconds": 5}
    },
    {
        "thought": "Done – PDF uploaded successfully",
        "action": {
            "type": "done",
            "summary": "PDF uploaded to Google Drive and visible in My Drive."
        }
    }
]
