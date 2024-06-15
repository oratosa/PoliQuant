import json
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path


class NdlApi:
    def __init__(self) -> None:
        self.api_endpoint_meeting_list = "https://kokkai.ndl.go.jp/api/meeting_list"

    def get_meeting_list(self, start_date: str, end_date: str, output_dir: str):
        """
        Retrieves meeting data from the API and saves it as JSON files.

        This function iterates over the specified years and months, retrieves meeting data
        from the API for each month, and saves the data as JSON files.
        """

        # API endpoint URL
        api_endpoint = self.api_endpoint_meeting_list

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        current_date = start_date

        while current_date <= end_date:

            month_start = current_date.replace(day=1)
            next_month = month_start.replace(day=28) + timedelta(days=4)  # 次の月に進む
            month_end = next_month - timedelta(days=next_month.day)

            # Start record position for pagination
            startrecord = 1

            done = False
            while not done:
                # Iterate requesting data from the API until nextRecordPosition become None
                payload = {
                    "from": str(month_start.date()),
                    "until": str(month_end.date()),
                    "startRecord": str(startrecord),
                    "maximumRecords": str(100),
                    "recordPacking": "json",
                }
                r = requests.get(url=api_endpoint, params=payload)
                result = r.json()

                # Create a directory for the data if it doesn't exist
                os.makedirs(output_dir, exist_ok=True)

                # Create a file path
                file_name = f"meeting_list_{month_start}_{startrecord}.json"
                path = f"{output_dir}/{file_name}"

                # Dump the data to a JSON file
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False)

                # Check if there is more data to retrieve
                if result["nextRecordPosition"] is None:
                    done = True
                else:
                    startrecord = result["nextRecordPosition"]

            current_date = month_end + timedelta(days=1)


if __name__ == "__main__":
    ndl_api = NdlApi()
    path = Path().resolve()  # Retrieve the path of working directory
    ndl_api.get_meeting_list(
        start_date="2024-04-10",
        end_date="2024-06-14",
        output_dir=f"{path}/data/meeting_list",
    )
