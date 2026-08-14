from job_monitor.compare import main as compare_jobs
from job_monitor.monitor import main as fetch_jobs


def main():
    print("Running monitor...")
    fetch_jobs()

    print("Running compare...")
    compare_jobs()


if __name__ == "__main__":
    main()
