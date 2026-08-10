from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://www.citadel.com"

CAREERS_URL = (
    "https://www.citadel.com/"
    "careers/open-opportunities/"
)


def get_job_links(page_number):

    if page_number == 1:
        url = CAREERS_URL
    else:
        url = (
            f"{CAREERS_URL}"
            f"page/{page_number}/"
        )

    response = requests.get(
        url,
        impersonate="chrome",
        timeout=30,
    )

    print(
        f"Page {page_number}: "
        f"status={response.status_code}"
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    job_links = []

    for link in soup.find_all(
        "a",
        href=True,
    ):

        href = link["href"]

        if "/careers/details/" not in href:
            continue

        full_url = urljoin(
            BASE_URL,
            href,
        )

        if full_url not in job_links:
            job_links.append(
                full_url
            )

    print(
        f"Page {page_number}: "
        f"{len(job_links)} jobs"
    )

    for job_url in job_links:
        print(job_url)

    return job_links


if __name__ == "__main__":

    all_jobs = []

    for page in range(1, 10):

        links = get_job_links(
            page
        )

        if not links:
            break

        new_links = [
            link
            for link in links
            if link not in all_jobs
        ]

        if not new_links:
            break

        all_jobs.extend(
            new_links
        )

    print(
        f"\nTotal unique jobs: "
        f"{len(all_jobs)}"
    )