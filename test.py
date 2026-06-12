import requests

url = (
    "https://fticonsulting.wd108.myworkdayjobs.com"
    "/wday/cxs/fticonsulting"
    "/CompassLexeconCareers/jobs"
)

r = requests.post(
    url,
    json={
        "limit": 20,
        "offset": 0
    }
)

print(r.status_code)
print(r.text[:1000])