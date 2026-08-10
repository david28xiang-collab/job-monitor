import os
import yaml
import pandas as pd

from citadel import fetch_citadel_jobs
from greenhouse import fetch_greenhouse
from icims import fetch_icims
from workday import fetch_workday
from millennium import fetch_millennium_jobs


company_jobs = {}


# ==================================================
# Load company configuration
# ==================================================

with open("companies.yaml", "r") as f:
    config = yaml.safe_load(f)


# ==================================================
# Fetch jobs for each company
# ==================================================

for company in config["companies"]:

    company_type = company.get("type")
    company_name = company["name"]

    print(
        f"\nFetching {company_name} "
        f"({company_type})..."
    )


    try:

        # ------------------------------------------
        # Greenhouse
        # ------------------------------------------

        if company_type == "greenhouse":

            jobs = fetch_greenhouse(
                company["board"],
                company_name,
            )


        # ------------------------------------------
        # iCIMS
        # ------------------------------------------

        elif company_type == "icims":

            jobs = fetch_icims(
                company["url"],
                company_name,
            )


        # ------------------------------------------
        # Workday
        # ------------------------------------------

        elif company_type == "workday":

            jobs = fetch_workday(
                company["api_url"],
                company_name,
                company["career_path"],
            )


        # ------------------------------------------
        # Millennium / Eightfold
        # ------------------------------------------

        elif company_type == "millennium":

            jobs = fetch_millennium_jobs()
        # ------------------------------------------
        # Millennium / Eightfold
        # ------------------------------------------
        elif company_type == "citadel":

            jobs = fetch_citadel_jobs()


        # ------------------------------------------
        # Unknown scraper type
        # ------------------------------------------

        else:

            print(
                f"Skipping {company_name} "
                f"(unknown type: {company_type})"
            )

            continue


    except Exception as e:

        print(
            f"Failed to fetch {company_name}: {e}"
        )

        continue


    # ==================================================
    # Do not write empty results
    # ==================================================

    if not jobs:

        print(
            f"No jobs found for {company_name}"
        )

        continue


    company_jobs[company_name] = jobs


# ==================================================
# Save jobs
# ==================================================

os.makedirs(
    "data",
    exist_ok=True,
)


for company_name, jobs in company_jobs.items():

    df = pd.DataFrame(
        jobs
    )

    filename = (
        company_name
        .lower()
        .replace(" ", "_")
    )

    output_path = (
        f"data/{filename}.csv"
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Saved {len(df)} jobs "
        f"for {company_name}"
    )