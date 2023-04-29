import json
import os
import datetime
import calendar
import requests


def get_first_and_last_date_of_month(year: int, month: int):
    if year is None or month is None:
        today = datetime.date.today()
        year, month = today.year, today.month - 1

    check_year_and_month(year, month)

    first_date = datetime.date(year, month, 1)
    last_date = datetime.date(year, month, calendar.monthrange(year, month)[1])
    return first_date, last_date


def check_year_and_month(year: int, month: int):
    if not isinstance(year, int) or not isinstance(month, int):
        raise TypeError("year and month must be integers.")
    if len(str(year)) != 4:
        raise ValueError("year must be a 4-digit integer.")
    if month < 1 or month > 12:
        raise ValueError("month must be an integer between 1 and 12.")


def main():
    api_endpoint = "https://kokkai.ndl.go.jp/api/meeting_list"
    years = [2022, 2023]
    months = range(1, 13)

    for year in years:
        for month in months:
            first_date, last_date = get_first_and_last_date_of_month(year, month)
            startrecord = 1

            if last_date > datetime.date.today():
                break

            done = False
            while done is False:
                # request a data
                payload = {
                    "from": str(first_date),
                    "until": str(last_date),
                    "startRecord": str(startrecord),
                    "maximumRecords": str(100),
                    "recordPacking": "json",
                }
                r = requests.get(url=api_endpoint, params=payload)
                result = r.json()

                # dump a file
                os.makedirs("data", exist_ok=True)
                with open(
                    f"data/meeting_list_{first_date}_{startrecord}.json",
                    "w",
                    encoding="utf-8",
                ) as f:
                    json.dump(result, f, ensure_ascii=False)

                # check if there is a rest of the data
                if result["nextRecordPosition"] is None:
                    done = True
                else:
                    startrecord = result["nextRecordPosition"]


if __name__ == "__main__":
    main()
