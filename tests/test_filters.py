import csv
import math

import pytest

from job_monitor.filters import is_target_location
from job_monitor.paths import DATA_DIR


DATASET = "cornerstone_research.csv"

DATA_FILE = DATA_DIR / DATASET


@pytest.mark.parametrize(
    ("location", "expected"),
    [
        ("US", True),
        ("US-MA-Boston", True),
        ("US-IL-Chicago | UK-London", True),
        ("US-DC-Washington, DC", True),
        ("CN-Shanghai", True),
        ("Hong Kong SAR", True),
        ("UK-London", False),
        ("Paris, France", False),
        (None, True),
        (math.nan, True),
    ],
)
def test_is_target_location(location, expected):
    assert is_target_location(location) is expected


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
