import json, os
import requests

api_endpoint = "https://kokkai.ndl.go.jp/api/meeting_list"
payload = {"from": "2023-02-01", "until": "2023-02-28", "maximumRecords": "100", "recordPacking": "json"}

r = requests.get(url=api_endpoint, params=payload)
output = r.json()

os.makedirs("data", exist_ok=True)

with open("data/meeting_list_202302_ver2.json", "w") as f:
    json.dump(output, f)
