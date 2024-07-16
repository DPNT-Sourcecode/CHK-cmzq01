import pytest

from solutions.CHK.parse_offer_database import parse_line
from solutions.CHK.offers import *



class TestParseOfferDatabase:

    @pytest.mark.parametrize(
        "line, expected_sku, expected_offer",
        [
            (
                    "| B    | 30    | 2B for 45              |",
                    "B",
                    LadderOffer(
                        30,
                        [
                            LadderDiscount(2, 45)
                        ]
                    )
            ),
        ],
    )
    def test_parse_line(
            self, line, expected_sku, expected_offer
    ):
        sku, offer = parse_line(line)
        assert sku == expected_sku
        assert offer.__hash__ == expected_offer.__hash__
