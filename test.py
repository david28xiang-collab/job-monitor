import requests
from bs4 import BeautifulSoup

html = requests.get(
    "https://ug-chire.icims.com/jobs/search?in_iframe=1"
).text

print("Length:", len(html))

soup = BeautifulSoup(html, "html.parser")

for a in soup.find_all("a", href=True):

    href = a["href"]

    if "/jobs/" in href:
        print(href)