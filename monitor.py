import requests

url = "https://analystcareers-analysisgroup.icims.com/jobs/search"

response = requests.get(url)

print("Status:", response.status_code)
print(response.text[:1000])
