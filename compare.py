from datetime import datetime
import os
import shutil
import pandas as pd
from discord_notify import send_discord
from filter import is_target_location

today = datetime.now().strftime("%Y-%m-%d")

found_new_jobs = False

for file in os.listdir("data"):

    if not file.endswith(".csv"):
        continue

    current_path = f"data/{file}"
    baseline_path = f"baseline/{file}"

    print(f"Checking {file}")

    # First time seeing this company
    if not os.path.exists(baseline_path):

        print(f"Creating baseline for {file}")

        shutil.copy(
            current_path,
            baseline_path
        )

        continue

    # Skip empty current CSV
    if os.path.getsize(current_path) == 0:

        print(f"Skipping empty current file: {current_path}")
        continue

    # Skip empty baseline CSV
    if os.path.getsize(baseline_path) == 0:

        print(f"Skipping empty baseline file: {baseline_path}")
        continue

    try:
        current = pd.read_csv(current_path)
        baseline = pd.read_csv(baseline_path)
    except pd.errors.EmptyDataError:
        print(f"Skipping invalid CSV: {file}")
        continue

    current_ids = set(current["job_id"].astype(str))
    baseline_ids = set(baseline["job_id"].astype(str))

    new_ids = current_ids - baseline_ids

    if len(new_ids) > 0:
        new_jobs = current[
            current["job_id"].astype(str).isin(new_ids)
        ]

        if "location" in new_jobs.columns:
            new_jobs = new_jobs[
                new_jobs["location"].apply(is_target_location)
            ]

        if new_jobs.empty:
            print(
                f"No new US, Hong Kong, or China jobs in {file}"
            )
            continue

        found_new_jobs = True

        company = new_jobs.iloc[0]["company"]

        message = (
            "-----------------------------------------------\n"
            f"📅 {today}\n\n"
            f"🐧 **上班小企鹅给你找到了新工作**\n"
            f"🏢 {company}\n\n"
        )

        for _, row in new_jobs.iterrows():

            message += (
                f"{row['title']}\n"
                f"{row['url']}\n\n"
            )

        send_discord(message)

        print()
        print("=" * 50)
        print(message)
        print("=" * 50)

# No new jobs anywhere

if not found_new_jobs:

    message = (
        "-----------------------------------------------\n"
        f"📅 {today}\n\n"
        f"🐧 上班小企鹅今天检查完毕\n\n"
        "没有发现新工作。"
    )

    send_discord(message)

    print(message)

# Update baseline

os.makedirs("baseline", exist_ok=True)

for file in os.listdir("data"):

    if not file.endswith(".csv"):
        continue

    current_path = f"data/{file}"
    baseline_path = f"baseline/{file}"

    # Don't overwrite with an empty file
    if os.path.getsize(current_path) == 0:
        continue

    shutil.copy(
        current_path,
        baseline_path
    )