from pathlib import Path
from datetime import datetime


class Logger:
    COLORS = {
        "INFO": "\033[94m",     # Blue
        "DEBUG": "\033[96m",    # Cyan
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",    # Red
        "RESET": "\033[0m"
    }

    def __init__(self, log_to_file=True):
        self.log_to_file = log_to_file
        if log_to_file:
            root_dir = Path(__file__).resolve().parent.parent
            self.log_dir = root_dir / ".temp" / "logs"
            self.log_dir.mkdir(parents=True, exist_ok=True)
            self.log_file = self.log_dir / "app.log"

    def _write(self, level, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        colored_level = f"{self.COLORS.get(level, '')}{level}{self.COLORS['RESET']}"
        message = " ".join(str(arg) for arg in args)
        log_line = f"[{timestamp}] [{level}] {message}"

        # Print to console with color
        print(f"[{timestamp}] [{colored_level}] {message}")

        # Write to file if enabled
        if self.log_to_file:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")

    def info(self, *args):
        self._write("INFO", *args)

    def debug(self, *args):
        self._write("DEBUG", *args)

    def warn(self, *args):
        self._write("WARNING", *args)

    def error(self, *args):
        self._write("ERROR", *args)


logger = Logger()
