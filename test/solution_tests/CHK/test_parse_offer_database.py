import pytest

from solutions.CHK.parse_offer_database import parse_line
from solutions.CHK.offers import *



class TestParseOfferDatabase:

    @pytest.mark.parametrize(
        "line, expected_sku, expected_offer",
        [
            (
                    "| C    | 20    |                        |",
                    "C",
                    SingleProductOffer(20),
            ),
            (
                    "| U    | 40    | 3U get one U free      |",
                    "U",
                    BgfOffer(40, 3),
            ),
            (
                    "| B    | 30    | 2B for 45              |",
                    "B",
                    LadderOffer(
                        30,
                        [
                            LadderDiscount(2, 45)
                        ]),
            ),
            (
                    "| R    | 50    | 3R get one Q free      |",
                    "R",
                    CrossProductOffer(50, "R", 3, "Q"),
            ),
        ],
    )
    def test_parse_line(
            self, line, expected_sku, expected_offer
    ):
        sku, offer = parse_line(line)
        assert sku == expected_sku
        assert offer == expected_offer

