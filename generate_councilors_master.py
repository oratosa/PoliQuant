import unicodedata, re, urllib, csv
import requests
from lxml import html
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


class CouncilorsNameList:
    def __init__(self, session):
        self.session: int = session
        self.source_url: str = (
            f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/{session}/giin.htm"
        )
        self.members: list = list()
        self.update_date: str = None

    def add_update_date(self) -> None:
        response = requests.get(self.source_url)

        # parse the html
        dom = html.fromstring(response.content)
        target_xpath = "/html/body/div/div/div[4]/div[2]/div[2]/p[3]"
        update_date = dom.xpath(target_xpath)[0].text

        self.update_date = reiwa_to_ad(update_date)

    def add_members(self) -> None:
        response = requests.get(self.source_url)

        # parse the html
        dom = html.fromstring(response.content)
        target = "/html/body/div/div/div[4]/div[2]/div[2]/table[2]//tr"  # /table[2]/tbody//tr とすると抽出できない
        rows = dom.xpath(target)

        member_list = []
        for row in rows[1:]:  # ignore the header row.
            cells = row.xpath(".//td")

            # URL of profile
            profile = cells[0].xpath("./a/@href")[0]
            abs_url = urllib.parse.urljoin(self.source_url, profile)

            # His/her name
            name = cells[0].text_content()
            name = (
                unicodedata.normalize("NFKC", name).replace("\n", "").replace(" ", "")
            )
            name = re.sub(r"\[.+\]", "", name)

            # Furigana
            kana = cells[1].text_content()
            kana = (
                unicodedata.normalize("NFKC", kana).replace("\n", "").replace(" ", "")
            )

            # Political party
            party = cells[2].text_content()

            # Electoral district
            district = cells[3].text_content()

            # Expiration date
            expiration = cells[4].text_content()
            expiration_ad = str(reiwa_to_ad(expiration))
            member_list.append(
                [
                    abs_url,
                    name,
                    kana,
                    party,
                    district,
                    expiration_ad,
                    self.session,
                ]
            )

        self.members.extend(member_list)


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
        councilors = CouncilorsNameList(session)
        councilors.add_update_date()
        councilors.add_members()

        with open(f"data/counsilors_master_{councilors.update_date}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(councilors.members)
