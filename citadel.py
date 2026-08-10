from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


BASE_URL = "https://www.citadel.com"

CAREERS_URL = (
    "https://www.citadel.com/"
    "careers/open-opportunities/"
)


# ==================================================
# Fetch one Citadel careers page
# ==================================================

def fetch_citadel_page(page_number):

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

    response.raise_for_status()


    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )


    jobs = []

    seen_urls = set()


    # ==================================================
    # Find job links
    # ==================================================

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


        # Remove fragments if any
        full_url = full_url.split("#")[0]


        # Avoid duplicate links
        if full_url in seen_urls:
            continue

        seen_urls.add(
            full_url
        )


        # ==================================================
        # Extract text from job card
        # ==================================================

        parts = [
            text.strip()
            for text in link.stripped_strings
            if text.strip()
        ]


        # Remove button text
        parts = [
            text
            for text in parts
            if text.lower()
            not in {
                "apply now",
                "learn more",
            }
        ]


        if not parts:
            continue


        # ==================================================
        # Title
        # ==================================================

        title_element = link.find(
            ["h2", "h3", "h4"]
        )


        if title_element:

            title = (
                title_element
                .get_text(
                    " ",
                    strip=True,
                )
            )

        else:

            title = parts[0]


        # ==================================================
        # Location
        #
        # Job card generally looks like:
        #
        # Sector Data Scientist, Central Team
        # New York
        # Apply Now
        #
        # or
        #
        # Software Engineer
        # Greenwich, Houston, London, New York...
        # ==================================================

        location_parts = []


        title_found = False

        for part in parts:

            if part == title:

                title_found = True

                continue


            if title_found:

                location_parts.append(
                    part
                )


        location = ", ".join(
            location_parts
        )


        # ==================================================
        # Job ID
        #
        # Use URL slug:
        #
        # /careers/details/
        # sector-data-scientist-central-team/
        #
        # ->
        #
        # sector-data-scientist-central-team
        # ==================================================

        path = urlparse(
            full_url
        ).path


        job_id = (
            path
            .rstrip("/")
            .split("/")[-1]
        )


        jobs.append(
            {
                "company": "Citadel",
                "job_id": job_id,
                "title": title,
                "location": location,
                "url": full_url,
            }
        )


    return jobs


# ==================================================
# Fetch ALL Citadel jobs
# ==================================================

def fetch_citadel_jobs():

    all_jobs = []

    seen_job_ids = set()

    page_number = 1


    while True:

        print(
            f"Citadel: fetching page "
            f"{page_number}..."
        )


        jobs = fetch_citadel_page(
            page_number
        )


        print(
            f"Citadel: page {page_number} "
            f"returned {len(jobs)} jobs"
        )


        # ==================================================
        # No jobs = end of pagination
        # ==================================================

        if not jobs:
            break


        new_jobs = []


        for job in jobs:

            job_id = job["job_id"]


            if job_id in seen_job_ids:
                continue


            seen_job_ids.add(
                job_id
            )


            new_jobs.append(
                job
            )


        # ==================================================
        # Stop if page only contains duplicates
        # ==================================================

        if not new_jobs:

            print(
                "Citadel: no new jobs "
                "on this page. Stopping."
            )

            break


        all_jobs.extend(
            new_jobs
        )


        page_number += 1


        # Safety guard
        if page_number > 100:

            print(
                "Citadel: reached page "
                "safety limit."
            )

            break


    print(
        f"Citadel: fetched "
        f"{len(all_jobs)} unique jobs"
    )


    return all_jobs

