import unicodedata, re, urllib, csv
import requests
from bs4 import BeautifulSoup


class Councilors:
    def __init__(self):
        self.members = list()

    def add_members(self, url: str) -> None:
        # retrieve a html
        page = url
        response = requests.get(page)
        html = response.content

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
                        ]
                    )

        self.members.extend(member_list)


def main():
    councilors = Councilors()

    page = "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/200/giin.htm"

    councilors.add_members(page)

    with open("data/counsilors_master.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(councilors.members)


if __name__ == "__main__":
    main()
