import pandas as pd
import yaml

from job_monitor.paths import CONFIG_FILE, DATA_DIR
from job_monitor.scrapers.citadel import fetch_citadel_jobs
from job_monitor.scrapers.greenhouse import fetch_greenhouse
from job_monitor.scrapers.icims import fetch_icims
from job_monitor.scrapers.millennium import fetch_millennium_jobs
from job_monitor.scrapers.workday import fetch_workday


def main():
    company_jobs = {}

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    for company in config["companies"]:
        company_type = company.get("type")
        company_name = company["name"]
        print(f"\nFetching {company_name} ({company_type})...")

        try:
            if company_type == "greenhouse":
                jobs = fetch_greenhouse(
                    company["board"],
                    company_name,
                )
            elif company_type == "icims":
                jobs = fetch_icims(
                    company["url"],
                    company_name,
                )
            elif company_type == "workday":
                jobs = fetch_workday(
                    company["api_url"],
                    company_name,
                    company["career_path"],
                )
            elif company_type == "millennium":
                jobs = fetch_millennium_jobs()
            elif company_type == "citadel":
                jobs = fetch_citadel_jobs()
            else:
                print(
                    f"Skipping {company_name} "
                    f"(unknown type: {company_type})"
                )
                continue
        except Exception as error:
            print(f"Failed to fetch {company_name}: {error}")
            continue

        if not jobs:
            print(f"No jobs found for {company_name}")
            continue

        company_jobs[company_name] = jobs

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for company_name, jobs in company_jobs.items():
        dataframe = pd.DataFrame(jobs)
        filename = company_name.lower().replace(" ", "_")
        output_path = DATA_DIR / f"{filename}.csv"

        dataframe.to_csv(output_path, index=False)
        print(f"Saved {len(dataframe)} jobs for {company_name}")


if __name__ == "__main__":
    main()
