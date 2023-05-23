import unicodedata, re, urllib, csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date


def reiwa_to_ad(reiwa_date: str) -> date:
    """
    reiwa_date takes a format like "令和5年4月25日現在".
    """
    reiwa_start_date = datetime(2019, 5, 1)

    reiwa_year = int(reiwa_date[2 : reiwa_date.index("年")])
    year = reiwa_year + int(reiwa_start_date.year) - 1
    month = int(reiwa_date[reiwa_date.index("年") + 1 : reiwa_date.index("月")])
    day = int(reiwa_date[reiwa_date.index("月") + 1 : reiwa_date.index("日")])

    ad_date = datetime(year, month, day).date()

    return ad_date


class Representatives:
    def __init__(self):
        self.members = list()

    def add_members(self, url: str) -> None:
        # retrieve a html
        page = url
        response = requests.get(page)
        html = response.content

        # parse the html
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        member_table = tables[1]

        member_list = []
        for row in member_table.find_all("tr"):
            cells = row.find_all("tt")

            if len(cells) > 0:
                a = cells[0].find("a", href=True)

                # "a" tag includes a politician's profile website. If a is None, it's not a politician's data and you can skip.
                if a is None:
                    continue
                else:
                    # Website for profile
                    profile = a["href"]
                    abs_url = urllib.parse.urljoin(
                        page,
                        profile,
                    )

                    # His/her Name
                    name = cells[0].get_text().strip()
                    name = (
                        unicodedata.normalize("NFKC", name)
                        .replace("\n", "")
                        .replace(" ", "")
                    )
                    name = name[:-1]  # remove "君"

                    # Furigana
                    kana = cells[1].get_text().strip()
                    kana = (
                        unicodedata.normalize("NFKC", kana)
                        .replace("\n", "")
                        .replace(" ", "")
                    )

                    # Political party
                    party = cells[2].get_text().strip()

                    # Electoral district
                    district = cells[3].get_text().strip()

                    # Elected times
                    kaisu = cells[4].get_text().strip()
                    kaisu = re.sub(r"\（.+\）", "", kaisu)  # e.g. "4（参1）" -> "4"

                    member_list.append(
                        [
                            abs_url,
                            name,
                            kana,
                            party,
                            district,
                            kaisu,
                        ]
                    )

        self.members.extend(member_list)


class Councilors:
    def __init__(self, session):
        self.session: int = session
        self.source_url: str = (
            f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/{session}/giin.htm"
        )
        self.members: list = list()
        self.update_date: date = None

    def add_update_date(self, html: str) -> None:
        # parse the html
        soup = BeautifulSoup(html, "html.parser")
        update_date_txt = soup.find("p", _class="ta_r").get_text().strip()
        self.update_date = reiwa_to_ad(update_date_txt)

    def add_members(self, html: str) -> None:
        # parse the html
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", summary="議員一覧（50音順）")

        member_list = []
        for row in table.find_all("tr"):
            cells = row.find_all("td")

            if len(cells) > 0:
                a = cells[0].find("a", href=True)

                # "a" tag includes a politician's profile website. If a is None, it's not a politician's data and you can skip.
                if a is None:
                    continue
                else:
                    # Website for profile
                    profile = a["href"]
                    abs_url = urllib.parse.urljoin(
                        self.source_url,
                        profile,
                    )

                    # His/her Name
                    name = cells[0].get_text().strip()
                    name = (
                        unicodedata.normalize("NFKC", name)
                        .replace("\n", "")
                        .replace(" ", "")
                    )
                    name = re.sub(r"\[.+\]", "", name)

                    # Furigana
                    kana = cells[1].get_text().strip()
                    kana = (
                        unicodedata.normalize("NFKC", kana)
                        .replace("\n", "")
                        .replace(" ", "")
                    )

                    # Political party
                    party = cells[2].get_text().strip()

                    # Electoral district
                    district = cells[3].get_text().strip()

                    # Expiration date
                    expiration = cells[4].get_text().strip()

                    member_list.append(
                        [
                            abs_url,
                            name,
                            kana,
                            party,
                            district,
                            expiration,
                            self.session,
                        ]
                    )

        self.members.extend(member_list)


def write_representatives():
    # Representatives
    representatives = Representatives()

    page_a = (
        "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/1giin.htm"
    )
    page_ka = (
        "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/2giin.htm"
    )
    page_sa = (
        "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/3giin.htm"
    )
    page_ta = (
        "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/4giin.htm"
    )
    page_na = (
        "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/5giin.htm"
    )
    page_ha = (
        "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/6giin.htm"
    )
    page_ma = (
        "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/7giin.htm"
    )
    page_ya = (
        "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/8giin.htm"
    )
    page_ra = (
        "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/9giin.htm"
    )
    page_wa = (
        "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/10giin.htm"
    )

    pages = [
        page_a,
        page_ka,
        page_sa,
        page_ta,
        page_na,
        page_ha,
        page_ma,
        page_ya,
        page_ra,
        page_wa,
    ]

    for page in pages:
        representatives.add_members(page)

    with open("data/representatives_master.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(representatives.members)


def write_councilors(session):
    councilors = Councilors(session)

    html = retrieve_html(councilors.source_url)
    councilors.add_update_date(html)

    councilors.add_members(html)

    with open(
        "data/counsilors_master_{}.csv".format(str(councilors.update_date)), "w"
    ) as f:
        writer = csv.writer(f)
        writer.writerows(councilors.members)


if __name__ == "__main__":
    sessions = range(207, 212)
    for session in sessions:
        write_councilors(session)
