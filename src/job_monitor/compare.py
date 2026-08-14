from datetime import datetime
import shutil

import pandas as pd

from job_monitor.filters import is_target_location
from job_monitor.notifications import send_discord
from job_monitor.paths import BASELINE_DIR, DATA_DIR


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    found_new_jobs = False
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)

    for current_path in sorted(DATA_DIR.glob("*.csv")):
        filename = current_path.name
        baseline_path = BASELINE_DIR / filename
        print(f"Checking {filename}")

        if not baseline_path.exists():
            print(f"Creating baseline for {filename}")
            shutil.copy(current_path, baseline_path)
            continue

        if current_path.stat().st_size == 0:
            print(f"Skipping empty current file: {current_path}")
            continue

        if baseline_path.stat().st_size == 0:
            print(f"Skipping empty baseline file: {baseline_path}")
            continue

        try:
            current = pd.read_csv(current_path)
            baseline = pd.read_csv(baseline_path)
        except pd.errors.EmptyDataError:
            print(f"Skipping invalid CSV: {filename}")
            continue

        current_ids = set(current["job_id"].astype(str))
        baseline_ids = set(baseline["job_id"].astype(str))
        new_ids = current_ids - baseline_ids

        if not new_ids:
            continue

        new_jobs = current[
            current["job_id"].astype(str).isin(new_ids)
        ]

        if "location" in new_jobs.columns:
            new_jobs = new_jobs[
                new_jobs["location"].apply(is_target_location)
            ]

        if new_jobs.empty:
            print(
                f"No new US, Hong Kong, or China jobs in {filename}"
            )
            continue

        found_new_jobs = True
        company = new_jobs.iloc[0]["company"]
        message = (
            "-----------------------------------------------\n"
            f"📅 {today}\n\n"
            "🐧 **上班小企鹅给你找到了新工作**\n"
            f"🏢 {company}\n\n"
        )

        for _, row in new_jobs.iterrows():
            message += f"{row['title']}\n{row['url']}\n\n"

        send_discord(message)
        print()
        print("=" * 50)
        print(message)
        print("=" * 50)

    if not found_new_jobs:
        message = (
            "-----------------------------------------------\n"
            f"📅 {today}\n\n"
            "🐧 上班小企鹅今天检查完毕\n\n"
            "没有发现新工作。"
        )
        send_discord(message)
        print(message)

    for current_path in DATA_DIR.glob("*.csv"):
        if current_path.stat().st_size == 0:
            continue

        baseline_path = BASELINE_DIR / current_path.name
        shutil.copy(current_path, baseline_path)


if __name__ == "__main__":
    main()
