import json
import os
import datetime
import calendar
import requests


def get_first_and_last_date_of_month(year: int, month: int):
    # If year or month is not provided, use the current year and previous month
    if year is None or month is None:
        today = datetime.date.today()
        year, month = today.year, today.month - 1

    # Check if the year and month values are valid
    check_year_and_month(year, month)

    # Get the first and last date of the month
    first_date = datetime.date(year, month, 1)
    last_date = datetime.date(year, month, calendar.monthrange(year, month)[1])
    return first_date, last_date


def check_year_and_month(year: int, month: int):
    """
    Check if the year and month values are valid.

    Args:
        year (int): The year value.
        month (int): The month value.

    Raises:
        TypeError: If year or month is not an integer.
        ValueError: If year is not a 4-digit integer or month is not between 1 and 12.
    """
    if not isinstance(year, int) or not isinstance(month, int):
        raise TypeError("year and month must be integers.")
    if len(str(year)) != 4:
        raise ValueError("year must be a 4-digit integer.")
    if month < 1 or month > 12:
        raise ValueError("month must be an integer between 1 and 12.")


def main():
    """
    Retrieves meeting data from the API and saves it as JSON files.

    This function iterates over the specified years and months, retrieves meeting data
    from the API for each month, and saves the data as JSON files.

    API Endpoint: https://kokkai.ndl.go.jp/api/meeting_list
    """

    # API endpoint URL
    api_endpoint = "https://kokkai.ndl.go.jp/api/meeting_list"

    # Years and months to retrieve data for
    years = [2022, 2023]
    months = range(1, 13)

    for year in years:
        for month in months:
            # Get the first and last date of the month
            first_date, last_date = get_first_and_last_date_of_month(year, month)

            # Start record position for pagination
            startrecord = 1

            # If the last date is in the future, break the loop
            if last_date > datetime.date.today():
                break

            done = False
            while not done:
                # Request data from the API
                payload = {
                    "from": str(first_date),
                    "until": str(last_date),
                    "startRecord": str(startrecord),
                    "maximumRecords": str(100),
                    "recordPacking": "json",
                }
                r = requests.get(url=api_endpoint, params=payload)
                result = r.json()

                # Create a directory for the data if it doesn't exist
                os.makedirs("data", exist_ok=True)

                # Dump the data to a JSON file
                with open(
                    f"data/meeting_list_{first_date}_{startrecord}.json",
                    "w",
                    encoding="utf-8",
                ) as f:
                    json.dump(result, f, ensure_ascii=False)

                # Check if there is more data to retrieve
                if result["nextRecordPosition"] is None:
                    done = True
                else:
                    startrecord = result["nextRecordPosition"]


if __name__ == "__main__":
    main()
