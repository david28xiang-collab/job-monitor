import requests
from bs4 import BeautifulSoup


def fetch_icims(search_url, company):

    html = requests.get(
        search_url + "?in_iframe=1"
    ).text

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    jobs = []

    seen = set()

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if "/jobs/" not in href:
            continue

        try:
            job_id = (
                href.split("/jobs/")[1]
                .split("/")[0]
            )

            if len(job_id) == 0:
                continue

            if not job_id[0].isdigit():
                continue

        except Exception:
            continue

        if href in seen:
            continue

        seen.add(href)

        jobs.append({
            "company": company,
            "job_id": job_id,
            "title": a.get_text(strip=True).replace("Title", ""),
            "url": href.split("?")[0]
        })

    return jobs