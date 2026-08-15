import csv
import math
from pathlib import Path
import sys


SOURCE_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_DIR))

from job_monitor.filters import is_target_location, is_target_role
from job_monitor.paths import DATA_DIR


DATASET = "cornerstone_research.csv"

DATA_FILE = DATA_DIR / DATASET
ROLE_DATASET = "millennium.csv"
ROLE_DATA_FILE = DATA_DIR / ROLE_DATASET


def test_is_target_location():
    cases = [
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
    ]

    for location, expected in cases:
        assert is_target_location(location) is expected


def test_is_target_role():
    cases = [
        ("Quantitative Researcher - PhD Intern", False),
        ("Summer Analyst", False),
        ("Administrative Assistant", False),
        ("Executive Assistant (14-month FTC)", False),
        ("Recruitment and Office Coordinator", False),
        ("International Economics Analyst", True),
        ("Research Analyst", True),
        (None, True),
    ]

    for title, expected in cases:
        assert is_target_role(title) is expected


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


def show_millennium_role_flags():
    """Print True/False for every title in data/current/millennium.csv."""
    with ROLE_DATA_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        jobs = list(csv.DictReader(file))

    assert jobs, f"{ROLE_DATASET} contains no jobs"

    for job in jobs:
        title = job.get("title", "")
        print(f"{is_target_role(title)!s:<5} | {title}")


if __name__ == "__main__":
    show_millennium_role_flags()
