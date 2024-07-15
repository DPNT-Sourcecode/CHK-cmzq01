import pytest

from solutions.CHK.offers import *


class TestOffers:

    @pytest.mark.parametrize(
        "quantity, single_unit_price, expected_price",
        [
            (10, 5, 50),
            (10, 10, 100),
            (0, 5, 0),
            (0, 10, 0),
        ],
    )
    def test_calculate_price_single_product_offer(
            self, quantity, single_unit_price, expected_price
    ):
        offer = SingleProductOffer(single_unit_price)
        assert offer.calculate_price(quantity) == expected_price