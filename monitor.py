import requests
import re

html = requests.get(
    "https://analystcareers-analysisgroup.icims.com/jobs/search"
).text

matches = re.findall(r'/jobs/\d+/[^"]+', html)

for m in matches:
    print(m)

print("count:", len(matches))
