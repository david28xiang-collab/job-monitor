import requests


PAGE_SIZE = 20
REQUEST_TIMEOUT = 30


def fetch_workday(api_url, company, career_path):
    base_url = api_url.split("/wday/")[0]
    jobs = []
    offset = 0
    total = None

    while total is None or offset < total:
        response = requests.post(
            api_url,
            json={
                "limit": PAGE_SIZE,
                "offset": offset,
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()

        postings = data.get("jobPostings", [])
        if total is None:
            total = data.get("total", len(postings))

        if not postings:
            break

        for posting in postings:
            jobs.append(
                {
                    "company": company,
                    "job_id": posting["bulletFields"][0],
                    "title": posting["title"],
                    "location": posting.get("locationsText"),
                    "url": (
                        f"{base_url}/en-US/{career_path}/details/"
                        f"{posting['externalPath'].split('/')[-1]}"
                    ),
                }
            )

        offset += len(postings)

    return jobs
