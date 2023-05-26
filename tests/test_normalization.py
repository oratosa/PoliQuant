import pytest

from src.normalization import reiwa_to_ad, text_normalize


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        ("令和5年4月25日現在", "2023-04-25"),
        ("令和05年04月25日現在", "2023-04-25"),
        ("令和10年7月25日", "2028-07-25"),
    ],
)
def test_reiwa_to_ad(target, expected):
    assert reiwa_to_ad(target) == expected


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        ("足立　　敏之", "足立敏之"),
        ("あだち　としゆき", "あだちとしゆき"),
        ("石垣　のりこ[小川　のり子]", "石垣のりこ[小川のり子]"),
        ("自民", "自民"),
        ("鳥取・島根", "鳥取・島根"),
        ("青柳　陽一郎君", "青柳陽一郎君"),
        ("あおやぎ 　よういちろう 	", "あおやぎよういちろう"),
        (" 	（比）南関東 ", "(比)南関東"),
        ("4　　 　", "4"),
        ("4（参1）", "4(参1)"),
    ],
)
def test_text_normalize(target, expected):
    assert text_normalize(target) == expected
