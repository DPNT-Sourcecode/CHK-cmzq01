import os

import pytest

from CHK.parse_offer_database import parse_line, parse_offer_database_file
from CHK.offers import *


@pytest.fixture
def expected_offer_database_dict():
    return {
        "single_sku_offers": {
            "A": LadderOffer(
            50,
            [
                LadderDiscount(3, 130),
                LadderDiscount(5, 200),
            ],
            ),
            "B": LadderOffer(
                30,
                [
                    LadderDiscount(2, 45),
                ],
            ),
            "C": BasicOffer(20),
            "D": BasicOffer(15),
            "E": CrossProductOffer(40, 2, "B"),
            "F": BgfOffer(10, 2),
            "G": MultiSubjectSkuOffer(18, {"A", "C", "D", "E"}, 4, 27),
        },
        "group_offers": {
            {"A", "C", "D", "E"}: MultiSubjectSkuOffer(18, {"A", "C", "D", "E"}, 4, 27),
        }
    }


class TestParseOfferDatabase:

    @pytest.mark.parametrize(
        "line, expected_sku, expected_offer",
        [
            (
                "| C    | 20    |                        |",
                "C",
                BasicOffer(20),
            ),
            (
                "| U    | 40    | 3U get one U free      |",
                "U",
                BgfOffer(40, 3),
            ),
            (
                "| B    | 30    | 2B for 45              |",
                "B",
                LadderOffer(30, [LadderDiscount(2, 45)]),
            ),
            (
                "| R    | 50    | 3R get one Q free      |",
                "R",
                CrossProductOffer(50, 3, "Q"),
            ),
            (
                "| G    | 18    | buy any 4 of (A,C,D,E) for 27  |",
                "G",
                MultiSubjectSkuOffer(18, {"A", "C", "D", "E"}, 4, 27),
            ),
        ],
    )
    def test_parse_line(self, line, expected_sku, expected_offer):
        sku, offer = parse_line(line)
        assert sku == expected_sku
        assert offer == expected_offer

    def test_parse_offer_database_file(self, expected_offer_database_dict):
        test_database_filename = f"{os.getcwd()}/test_offer_database.txt"
        actual_offer_database_dict = parse_offer_database_file(test_database_filename)
        assert actual_offer_database_dict == expected_offer_database_dict

