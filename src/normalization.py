import unicodedata
from datetime import datetime


def reiwa_to_ad(reiwa_date: str) -> str:
    """
    reiwa_date takes a format like "令和5年4月25日現在".
    """
    reiwa_start_date = datetime(2019, 5, 1)

    reiwa_year = int(reiwa_date[2 : reiwa_date.index("年")])
    year = reiwa_year + int(reiwa_start_date.year) - 1
    month = int(reiwa_date[reiwa_date.index("年") + 1 : reiwa_date.index("月")])
    day = int(reiwa_date[reiwa_date.index("月") + 1 : reiwa_date.index("日")])

    ad_date = str(datetime(year, month, day).date())

    return ad_date


def text_normalize(txt: str) -> str:
    normalize_txt = (
        unicodedata.normalize("NFKC", txt)
        .replace("\n", "")
        .replace("\t", "")
        .replace(" ", "")
    )
    return normalize_txt
