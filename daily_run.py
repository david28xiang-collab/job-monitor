"""Backward-compatible launcher for running from the repository root."""

from pathlib import Path
import sys


SOURCE_DIR = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SOURCE_DIR))

from job_monitor.daily_run import main  # noqa: E402


if __name__ == "__main__":
    main()
