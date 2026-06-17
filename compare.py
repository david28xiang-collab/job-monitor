from datetime import datetime
import os
import shutil
import pandas as pd
from discord_notify import send_discord

today = datetime.now().strftime("%Y-%m-%d")

found_new_jobs = False

for file in os.listdir("data"):

    if not file.endswith(".csv"):
        continue

    current_path = f"data/{file}"
    baseline_path = f"baseline/{file}"

    if not os.path.exists(baseline_path):

        print(f"Creating baseline for {file}")

        shutil.copy(
            current_path,
            baseline_path
        )

        continue

    current = pd.read_csv(current_path)
    baseline = pd.read_csv(baseline_path)

    current_ids = set(current["job_id"].astype(str))
    baseline_ids = set(baseline["job_id"].astype(str))

    new_ids = current_ids - baseline_ids

    if len(new_ids) > 0:

        found_new_jobs = True

        new_jobs = current[
            current["job_id"].astype(str).isin(new_ids)
        ]

        company = new_jobs.iloc[0]["company"]

        message = (
            "-----------------------------------------------\n"
            f"📅 {today}\n\n"
            f"🐭 **鼠奇奇给你找到了新工作**\n"
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

    send_discord(
        "--------------------------------------------------\n"
        f"📅 {today}\n\n"
        "🐭 鼠奇奇今天检查完毕\n\n"
        "没有发现新工作。"
    )

# Update baseline

for file in os.listdir("data"):

    if file.endswith(".csv"):

        shutil.copy(
            f"data/{file}",
            f"baseline/{file}"
        )
        