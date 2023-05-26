from src.generate_representatives_master import RepresentativesNameList


class TestRepresentativesNameList:
    def test_init(self):
        representatives = RepresentativesNameList(1)
        assert (
            representatives.source_url
            == "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/1giin.htm"
        )
        assert representatives.members == []
        assert representatives.update_date == None

    def test_add_update_date(self):
        representatives = RepresentativesNameList(1)
        representatives.add_update_date()
        assert representatives.update_date == "2023-05-20"

    def test_add_members(self):
        representatives = RepresentativesNameList(1)
        representatives.add_update_date()
        representatives.add_members()
        assert representatives.members[0] == [
            "https://www.shugiin.go.jp/internet/itdb_giinprof.nsf/html/profile/011.html",
            "逢沢一郎",
            "あいさわいちろう",
            "自民",
            "岡山1",
            "12",
            "2023-05-20",
        ]
        assert representatives.members[-1] == [
            "https://www.shugiin.go.jp/internet/itdb_giinprof.nsf/html/profile/098.html",
            "尾身朝子",
            "おみあさこ",
            "自民",
            "(比)北関東",
            "3",
            "2023-05-20",
        ]
