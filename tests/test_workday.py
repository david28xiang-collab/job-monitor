"""Tests for the Workday scraper, including configured live endpoints."""

from pathlib import Path

import pytest
import requests
import yaml

from job_monitor.scrapers.workday import fetch_workday


CONFIG_FILE = Path(__file__).resolve().parents[1] / "config" / "companies.yaml"


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def workday_companies():
    with CONFIG_FILE.open(encoding="utf-8") as file:
        companies = yaml.safe_load(file)["companies"]

    return [company for company in companies if company["type"] == "workday"]


def test_fetch_workday_paginates_and_extracts_locations(monkeypatch):
    postings = [
        {
            "title": f"Role {index}",
            "externalPath": f"/job/City/Role-{index}_JR{index}",
            "locationsText": f"City {index}",
            "bulletFields": [f"JR{index}"],
        }
        for index in range(25)
    ]
    requested_offsets = []

    def fake_post(url, json, timeout):
        requested_offsets.append(json["offset"])
        start = json["offset"]
        end = start + json["limit"]
        return FakeResponse(
            {
                "total": len(postings),
                "jobPostings": postings[start:end],
            }
        )

    monkeypatch.setattr(
        "job_monitor.scrapers.workday.requests.post",
        fake_post,
    )

    jobs = fetch_workday(
        "https://example.com/wday/cxs/company/careers/jobs",
        "Example Company",
        "careers",
    )

    assert requested_offsets == [0, 20]
    assert len(jobs) == 25
    assert jobs[0]["location"] == "City 0"
    assert jobs[-1]["location"] == "City 24"


@pytest.mark.parametrize(
    "company",
    workday_companies(),
    ids=lambda company: company["name"],
)
def test_configured_workday_endpoint_returns_all_jobs_with_locations(company):
    """Compare scraper output with each configured Workday API's live total."""
    response = requests.post(
        company["api_url"],
        json={"limit": 20, "offset": 0},
        timeout=30,
    )
    response.raise_for_status()
    expected_total = response.json()["total"]

    jobs = fetch_workday(
        company["api_url"],
        company["name"],
        company["career_path"],
    )

    assert len(jobs) == expected_total
    assert all(job.get("location") for job in jobs)
