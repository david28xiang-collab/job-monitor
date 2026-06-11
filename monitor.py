import requests
import re

url = "https://analystcareers-analysisgroup.icims.com/jobs/search"

html = requests.get(url).text

matches = re.findall(r"/jobs/\d+", html)

print(matches[:50])
print("count:", len(matches))
