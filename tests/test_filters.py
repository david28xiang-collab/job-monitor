import csv
from job_monitor.filters import is_target_location
from job_monitor.paths import DATA_DIR


DATASET = "cornerstone_research.csv"

DATA_FILE = DATA_DIR / DATASET


def test_location_flag():
    with DATA_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        jobs = list(csv.DictReader(file))

    assert jobs, f"{DATASET} contains no jobs"

    for job in jobs:
        location = job.get("location", "")
        flag = is_target_location(location)

        print(
            f"{flag!s:<5} | "
            f"{location:<55} | "
            f"{job['title']}"
        )


if __name__ == "__main__":
    test_location_flag()
