import requests

def fetch_greenhouse(board, company):

    url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"

    data = requests.get(url).json()

    jobs = []

    for job in data["jobs"]:

        jobs.append({
            "company": company,
            "job_id": str(job["id"]),
            "title": job["title"],
            "location": job.get("location", {}).get("name"),
            "url": job["absolute_url"]
        })

    return jobs

    