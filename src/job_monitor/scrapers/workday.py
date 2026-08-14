import requests


def fetch_workday(api_url, company, career_path):

    response = requests.post(
        api_url,
        json={
            "limit": 20,
            "offset": 0
        }
    )

    data = response.json()

    base_url = api_url.split("/wday/")[0]

    jobs = []

    for job in data["jobPostings"]:

        jobs.append({
            "company": company,
            "job_id": job["bulletFields"][0],
            "title": job["title"],
            "url": (
                f"{base_url}/en-US/{career_path}/details/"
                f"{job['externalPath'].split('/')[-1]}"
            )
        })

    return jobs