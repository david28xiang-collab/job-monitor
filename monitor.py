import requests

companies = {
    "Analysis Group":
        "https://analystcareers-analysisgroup.icims.com/jobs/search",

    "Brattle":
        "https://www.brattle.com/careers/",

    "Compass Lexecon":
        "https://www.compasslexecon.com/careers/",

    "NERA":
        "https://www.nera.com/careers.html",
}

for name, url in companies.items():

    try:
        r = requests.get(url, timeout=20)

        print()
        print(name)
        print("status:", r.status_code)
        print("length:", len(r.text))

    except Exception as e:
        print(name, e)
