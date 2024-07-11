import re
import urllib
import csv
import requests
import os
from lxml import html

import normalization


TARGET_DIR = "/workspaces/PoliQuant/data/politician_list/councilors"


class ParserCouncilors:
    def __init__(self, session):
        self.session: int = session
        self.source_url: str = (
            f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/{session}/giin.htm"
        )
        self.members: list = list()
        self.update_date: str = None
        self.target_dir = TARGET_DIR

    def add_update_date(self) -> None:
        response = requests.get(self.source_url)

        # parse the html
        dom = html.fromstring(response.content)
        target = "/html/body/div/div/div[4]/div[2]/div[2]/p[3]"
        update_date = dom.xpath(target)[0].text

        self.update_date = normalization.reiwa_to_ad(update_date)

    def add_members(self) -> None:
        response = requests.get(self.source_url)

        # parse the html
        dom = html.fromstring(response.content)
        target = "/html/body/div/div/div[4]/div[2]/div[2]/table[2]//tr"  # if xpath includes tbody between table[2] and tr, it doesn't work.
        rows = dom.xpath(target)

        member_list = []
        for row in rows[1:]:  # ignore the header row.
            cells = row.xpath(".//td")

            # URL of profile
            profile = cells[0].xpath("./a/@href")[0]
            abs_url = urllib.parse.urljoin(self.source_url, profile)

            # His/her name
            name = cells[0].text_content()
            name = normalization.text_normalize(name)
            name = re.sub(r"\[.+\]", "", name)  # e.g. 石垣　のりこ[小川　のり子] ->

            # Furigana
            kana = cells[1].text_content()
            kana = normalization.text_normalize(kana)

            # Political party
            party = cells[2].text_content()
            party = normalization.text_normalize(party)

            # Electoral district
            district = cells[3].text_content()
            district = normalization.text_normalize(district)

            # Expiration date
            expiration = cells[4].text_content()
            expiration = normalization.text_normalize(expiration)
            expiration_ad = str(normalization.reiwa_to_ad(expiration))

            member_list.append(
                [
                    abs_url,
                    name,
                    kana,
                    party,
                    district,
                    expiration_ad,
                    str(self.session),
                ]
            )

        self.members.extend(member_list)

    def write_csv(self):
        os.makedirs(self.target_dir, exist_ok=True)
        with open(
            f"{self.target_dir}/councilors_{self.update_date}_{self.session}.csv",
            "w",
        ) as f:
            writer = csv.writer(f)
            writer.writerows(self.members)


if __name__ == "__main__":
    sessions = range(207, 214)  # session情報をどこかから取得してくる必要ある。
    for session in sessions:
        councilors = ParserCouncilors(session)
        councilors.add_update_date()
        councilors.add_members()
        councilors.write_csv()
