import os
import yaml
import pandas as pd

from greenhouse import fetch_greenhouse
from icims import fetch_icims

company_jobs = {}
all_jobs = []

with open("companies.yaml", "r") as f:
    config = yaml.safe_load(f)

for company in config["companies"]:

    company_type = company.get("type")

    if company_type == "greenhouse":

        jobs = fetch_greenhouse(
            company["board"],
            company["name"]
        )

    elif company_type == "icims":

        jobs = fetch_icims(
            company["url"],
            company["name"]
        )

    else:

        print(
            f"Skipping {company['name']} "
            f"(unknown type: {company_type})"
        )

        continue

    company_jobs[company["name"]] = jobs
    all_jobs.extend(jobs)

os.makedirs("data", exist_ok=True)

for company_name, jobs in company_jobs.items():

    df = pd.DataFrame(jobs)

    filename = (
        company_name.lower()
        .replace(" ", "_")
    )

    df.to_csv(
        f"data/{filename}.csv",
        index=False
    )

    print(
        f"Saved {len(df)} jobs for {company_name}"
    )


