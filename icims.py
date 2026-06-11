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

        if "/jobs/login" in href:
            continue

        if href in seen:
            continue

        seen.add(href)

        title = a.get_text(strip=True)

        if title.startswith("Title"):
            title = title[5:].strip()

        jobs.append({
            "company": company,
            "job_id": href.split("/jobs/")[1].split("/")[0],
            "title": title,
            "url": href.split("?")[0]
        })

    return jobs

