import yaml

with open("companies.yaml", "r") as f:
    data = yaml.safe_load(f)

for company in data["companies"]:
    print(company["name"])
