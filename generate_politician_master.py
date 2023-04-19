import unicodedata, re, urllib, csv
import requests
from bs4 import BeautifulSoup


class Politicians:
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


def main():
    politicians = Politicians()

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
        politicians.add_members(page)

    with open("data/politicians_master.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(politicians.members)


if __name__ == "__main__":
    main()
