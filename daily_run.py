import subprocess
import sys


print("Running monitor...")

subprocess.run(
    [sys.executable, "monitor.py"],
    check=True
)


print("Running compare...")

subprocess.run(
    [sys.executable, "compare.py"],
    check=True
)