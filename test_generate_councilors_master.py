import pytest

from generate_councilors_master import CouncilorsNameList, reiwa_to_ad


class TestCouncilorsNameList:
    def test_init(self):
        councilors = CouncilorsNameList(211)
        assert councilors.session == 211
        assert (
            councilors.source_url
            == "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/211/giin.htm"
        )
        assert councilors.members == []
        assert councilors.update_date == None

    def test_add_update_date(self):
        councilors = CouncilorsNameList(211)
        councilors.add_update_date()
        assert councilors.update_date == "2023-05-22"

    def test_add_members(self):
        councilors = CouncilorsNameList(211)
        councilors.add_members()
        assert not councilors.members[0] == [
            "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/profile/7016001.htm",
            "足立敏之",
            "あだちとしゆき",
            "自民",
            "比例",
            "令和10年7月25日",
            211,
        ]
        assert councilors.members[0] == [
            "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/profile/7016001.htm",
            "足立敏之",
            "あだちとしゆき",
            "自民",
            "比例",
            "2028-07-25",
            211,
        ]
        assert len(councilors.members) == 248


@pytest.mark.parametrize(
    ("reiwa_date", "ad_date"),
    [
        ("令和5年4月25日現在", "2023-04-25"),
        ("令和10年7月25日", "2028-07-25"),
        ("令和05年04月25日現在", "2023-04-25"),
    ],
)
def test_reiwa_to_ad(reiwa_date, ad_date):
    assert reiwa_to_ad(reiwa_date) == ad_date
