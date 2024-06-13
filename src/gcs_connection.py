import os
import json
from google.cloud import storage
from google.oauth2 import service_account


class GCSConnection:
    def __init__(self) -> None:
        self.client = self.setup_gcs_client()

    def setup_gcs_client(self):
        """Set up the Google Cloud Storage client"""
        service_account_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info
        )
        client = storage.Client(credentials=credentials)
        return client

    def upload_local_files_to_blob(
        self, local_folder_path, destination_bucket_name, prefix_of_blob_name
    ):
        """
        Upload the files in a local folder to the designated position in GCS.
        Keyword arguments:
            local_folder_path: "/workspaces/PoliQuant/data/meeting_list"
            destination_bucket_name: "poliquant"
            prefix_of_blob_name: "data/input/meeting_list"
        Notes:
            As the above example, prefix_of_blob_name doesn't include the bucket name.
        """

        # Define the local folder path and the destination bucket name
        local_folder_path = local_folder_path
        bucket_name = destination_bucket_name

        # Iterate over the files in the local folder
        for file_name in os.listdir(local_folder_path):
            # Construct the local file path
            local_file_path = os.path.join(local_folder_path, file_name)

            # Construct the destination blob name
            destination_blob_name = f"{prefix_of_blob_name}/{file_name}"

            # Upload the file to the destination bucket
            bucket = self.client.get_bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(local_file_path)
