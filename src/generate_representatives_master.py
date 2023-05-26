import re, urllib, csv
import requests
from lxml import html

import normalization


class RepresentativesNameList:
    def __init__(self, number):
        self.alphabetical_order = number
        self.source_url: str = f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{number}giin.htm"
        self.members: list = list()
        self.update_date: str = None

    def add_update_date(self) -> None:
        response = requests.get(self.source_url)

        # parse the html
        dom = html.fromstring(response.content)
        target = "/html/body/div[2]/div[2]/table[1]//tr/td"
        update_date = dom.xpath(target)[0].text

        self.update_date = normalization.reiwa_to_ad(update_date)

    def add_members(self) -> None:
        response = requests.get(self.source_url)

        # parse the html
        dom = html.fromstring(response.content)
        target = "/html/body/div[2]/div[2]/table[2]//tr/td/table//tr"  # if xpath includes tbody between table[2] and tr, it doesn't work.
        rows = dom.xpath(target)

        member_list = []
        for row in rows[1:]:  # ignore the header row.
            cells = row.xpath(".//td//tt")

            # Website for profile
            if cells[0].xpath("./a/@href"):
                profile = cells[0].xpath("./a/@href")[0]
            else:
                profile = "../../../../itdb_giinprof.nsf/html/profile/999.html"  # Tentative address is assigned when it doesn't have official one.

            abs_url = urllib.parse.urljoin(
                self.source_url,
                profile,
            )

            # His/her Name
            name = cells[0].text_content()
            name = normalization.text_normalize(name)
            name = name[:-1]  # remove "君"

            # Furigana
            kana = cells[1].text_content()
            kana = normalization.text_normalize(kana)

            # Political party
            party = cells[2].text_content()
            party = normalization.text_normalize(party)

            # Electoral district
            district = cells[3].text_content()
            district = normalization.text_normalize(district)

            # Elected times
            kaisu = cells[4].text_content()
            kaisu = normalization.text_normalize(kaisu)
            kaisu = re.sub(r"\(.+\)", "", kaisu)  # e.g. "4(参1)" -> "4"

            member_list.append(
                [abs_url, name, kana, party, district, kaisu, self.update_date]
            )

        self.members.extend(member_list)


if __name__ == "__main__":
    page_numbers = range(1, 11)
    for number in page_numbers:
        representatives = RepresentativesNameList(number)
        representatives.add_update_date()
        representatives.add_members()

        with open(
            f"data/representatives_master_{representatives.update_date}_{number}.csv",
            "w",
        ) as f:
            writer = csv.writer(f)
            writer.writerows(representatives.members)
