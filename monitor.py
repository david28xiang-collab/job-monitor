import requests

html = requests.get(
    "https://www.crai.com/cra-careers/jobs/"
).text

print(html[:5000])
