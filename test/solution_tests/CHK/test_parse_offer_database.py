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
        ],
    )
    def test_parse_line(
            self, line, expected_sku, expected_offer
    ):
        sku, offer = parse_line(line)
        assert sku == expected_sku
        assert offer == expected_offer

