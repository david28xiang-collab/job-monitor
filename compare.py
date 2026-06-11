import os
import shutil
import pandas as pd

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

        print()
        print("=" * 50)
        print(f"NEW JOBS FOUND IN {file}")
        print("=" * 50)

        print(
            current[
                current["job_id"].astype(str).isin(new_ids)
            ][["title", "url"]]
        )

# Update baseline after comparison

for file in os.listdir("data"):

    if file.endswith(".csv"):

        shutil.copy(
            f"data/{file}",
            f"baseline/{file}"
        )