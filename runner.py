from watchfiles import run_process
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    root_dir = Path(__file__).parent.resolve()
    autosurf_pkg = root_dir / "autosurfer"

    run_process(
        str(autosurf_pkg),
        target="python -m autosurfer.main",
    )
