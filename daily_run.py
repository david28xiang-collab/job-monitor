import subprocess

print("Running monitor...")
subprocess.run(
["python", "monitor.py"],
check=True
)

print("Running compare...")
subprocess.run(
["python", "compare.py"],
check=True
)

print("Done.")
