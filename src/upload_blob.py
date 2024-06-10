import os
from google.cloud import storage

# Set up the Google Cloud Storage client
client = storage.Client()

# Define the local folder path and the destination bucket name
local_folder_path = "data"
destination_bucket_name = "poliquant"

# Iterate over the files in the local folder
for file_name in os.listdir(local_folder_path):
    # Construct the local file path
    local_file_path = os.path.join(local_folder_path, file_name)

    # Construct the destination blob name
    destination_blob_name = f"{file_name}"

    # Upload the file to the destination bucket
    bucket = client.get_bucket(destination_bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)