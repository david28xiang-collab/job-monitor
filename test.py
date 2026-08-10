import requests


API_URL = "https://career.mlp.com/api/apply/v2/jobs"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/150.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


params = {
    "domain": "mlp.com",
    "start": 50,
    "num": 10,
    "sort_by": "relevance",
}


response = requests.get(
    API_URL,
    params=params,
    headers=HEADERS,
    timeout=30,
)

print("Status:", response.status_code)
print("URL:", response.url)
print("Content-Type:", response.headers.get("content-type"))

response.raise_for_status()

data = response.json()

print("\nTop-level type:", type(data))

if isinstance(data, dict):
    print("Keys:", data.keys())

print("\nRaw response preview:")
print(data)