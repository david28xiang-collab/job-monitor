from job_monitor.scrapers.icims import fetch_icims


ICIMS_HTML = """
<ul class="iCIMS_JobsTable">
  <li class="iCIMS_JobCardItem">
    <div class="row">
      <div class="col-xs-6 header left">
        <span class="sr-only field-label">Job Locations</span>
        <span>US-MA-Boston | US-IL-Chicago</span>
      </div>
      <div class="col-xs-12 title">
        <a href="/jobs/3004/analyst/job?in_iframe=1">
          <span class="sr-only field-label">Title</span>
          <h3>Analyst</h3>
        </a>
      </div>
    </div>
  </li>
</ul>
"""


class FakeResponse:
    text = ICIMS_HTML

    def raise_for_status(self):
        return None


def test_fetch_icims_extracts_location(monkeypatch):
    def fake_get(url, params, timeout):
        assert params == {"in_iframe": "1"}
        assert timeout == 30
        return FakeResponse()

    monkeypatch.setattr(
        "job_monitor.scrapers.icims.requests.get",
        fake_get,
    )

    jobs = fetch_icims(
        "https://example.icims.com/jobs/search",
        "Example Company",
    )

    assert jobs == [
        {
            "company": "Example Company",
            "job_id": "3004",
            "title": "Analyst",
            "location": "US-MA-Boston | US-IL-Chicago",
            "url": "https://example.icims.com/jobs/3004/analyst/job",
        }
    ]
