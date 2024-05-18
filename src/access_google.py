from google.cloud import storage

client = storage.Client()
bucket = client.get_bucket("poliquant")
iam_policy = bucket.get_iam_policy()

print(iam_policy)
