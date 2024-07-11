import os
import json
from google.cloud import storage
from google.oauth2 import service_account

service_account_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

credentials = service_account.Credentials.from_service_account_info(
    service_account_info
)

client = storage.Client(credentials=credentials)
print(client)

bucket = client.get_bucket("poliquant")
print(bucket.exists())
iam_policy = bucket.get_iam_policy()

print(iam_policy)
