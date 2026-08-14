from pathlib import Path
import sys

# Support `python src/job_monitor/daily_run.py` in addition to package execution.
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from job_monitor.compare import main as compare_jobs
from job_monitor.monitor import main as fetch_jobs


def main():
    print("Running monitor...")
    fetch_jobs()

    print("Running compare...")
    compare_jobs()


if __name__ == "__main__":
    main()
