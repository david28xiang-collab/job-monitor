import csv
from pathlib import Path

from filter import is_target_location


DATASET = "cornerstone_research.csv"

DATA_FILE = Path(__file__).resolve().parent / "data" / DATASET


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