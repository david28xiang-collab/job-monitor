from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


REQUEST_TIMEOUT = 30


def extract_location(card):
    location_container = card.select_one(".header.left")
    if location_container is None:
        return None

    location_parts = [
        span.get_text(" ", strip=True)
        for span in location_container.select("span:not(.field-label)")
        if span.get_text(" ", strip=True)
    ]

    return " | ".join(location_parts) or None


def fetch_icims(search_url, company):
    response = requests.get(
        search_url,
        params={"in_iframe": "1"},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    seen_job_ids = set()

    for card in soup.select(".iCIMS_JobCardItem"):
        link = card.select_one(".title a[href]")
        if link is None:
            continue

        href = link["href"]
        if "/jobs/" not in href:
            continue

        try:
            job_id = href.split("/jobs/", 1)[1].split("/", 1)[0]
        except IndexError:
            continue

        if not job_id.isdigit() or job_id in seen_job_ids:
            continue

        seen_job_ids.add(job_id)
        title_element = link.find(["h1", "h2", "h3", "h4"])
        title = (
            title_element.get_text(" ", strip=True)
            if title_element
            else link.get_text(" ", strip=True).replace("Title", "", 1)
        )

        jobs.append(
            {
                "company": company,
                "job_id": job_id,
                "title": title,
                "location": extract_location(card),
                "url": urljoin(search_url, href).split("?", 1)[0],
            }
        )

    return jobs
