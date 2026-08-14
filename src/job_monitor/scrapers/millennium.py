import requests


API_URL = "https://career.mlp.com/api/apply/v2/jobs"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/150.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_millennium_page(start=0, num=10):
    """
    Fetch one page of Millennium jobs.
    """

    params = {
        "domain": "mlp.com",
        "start": start,
        "num": num,
        "sort_by": "relevance",
    }

    response = requests.get(
        API_URL,
        params=params,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def fetch_millennium_jobs():
    """
    Fetch all currently open Millennium jobs.

    Returns:
        list[dict]
    """

    all_jobs = []

    start = 0
    page_size = 10
    total_jobs = None

    while True:

        # ------------------------------------------
        # Fetch one page
        # ------------------------------------------

        data = fetch_millennium_page(
            start=start,
            num=page_size,
        )

        positions = data.get(
            "positions",
            [],
        )

        # ------------------------------------------
        # Get total number of jobs
        # ------------------------------------------

        if total_jobs is None:

            total_jobs = data.get(
                "count",
                0,
            )

            print(
                f"Millennium reports "
                f"{total_jobs} open jobs"
            )

        # ------------------------------------------
        # Stop if API returns nothing
        # ------------------------------------------

        if not positions:

            print(
                f"Millennium returned no jobs "
                f"at start={start}"
            )

            break

        print(
            f"Millennium: fetched "
            f"{start} - "
            f"{start + len(positions) - 1}"
        )

        # ------------------------------------------
        # Normalize jobs
        # ------------------------------------------

        for job in positions:

            eightfold_id = job.get("id")
            ats_job_id = job.get("ats_job_id")

            # Use ATS requisition ID when available
            job_id = (
                ats_job_id
                if ats_job_id
                else eightfold_id
            )

            all_jobs.append(
                {
                    "company": "Millennium",

                    "job_id": str(job_id),

                    "title": job.get(
                        "name"
                    ),

                    "location": job.get(
                        "location"
                    ),

                    "department": job.get(
                        "department"
                    ),

                    "business_unit": job.get(
                        "business_unit"
                    ),

                    "work_option": job.get(
                        "work_location_option"
                    ),

                    "url": (
                        "https://career.mlp.com/"
                        f"careers/job/{eightfold_id}"
                    ),

                    "pid": str(
                        eightfold_id
                    ),
                }
            )

        # ------------------------------------------
        # Move to next page
        # ------------------------------------------

        start += len(positions)

        # ------------------------------------------
        # Stop once we fetched everything
        # ------------------------------------------

        if (
            total_jobs is not None
            and start >= total_jobs
        ):

            break

    # ----------------------------------------------
    # Remove duplicates
    # ----------------------------------------------

    unique_jobs = {}

    for job in all_jobs:

        job_id = job["job_id"]

        unique_jobs[job_id] = job

    jobs = list(
        unique_jobs.values()
    )

    print(
        f"Millennium: fetched "
        f"{len(jobs)} unique jobs"
    )

    return jobs


# ==================================================
# Test millennium.py directly
# ==================================================

if __name__ == "__main__":

    jobs = fetch_millennium_jobs()

    print(
        f"\nTotal Millennium jobs: "
        f"{len(jobs)}\n"
    )

    for job in jobs[:20]:

        print(
            job["job_id"],
            "|",
            job["title"],
            "|",
            job["location"],
        )