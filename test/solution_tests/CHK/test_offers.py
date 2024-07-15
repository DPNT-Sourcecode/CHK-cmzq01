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

    @pytest.mark.parametrize(
        "quantity, single_unit_price, expected_exception_class",
        [
            (10.5, 5, TypeError),
            (10, 5.5, TypeError),
        ],
    )
    def test_calculate_price_single_product_offer_exceptions(
            self, quantity, single_unit_price, expected_exception_class
    ):
        with pytest.raises(expected_exception_class):
            offer = SingleProductOffer(single_unit_price)
            offer.calculate_price(quantity)

    @pytest.mark.parametrize(
        "quantity, single_unit_price, buy_quantity, get_quantity, expected_price",
        [
            (1, 10, 2, 1, 10),
            (2, 10, 2, 1, 20),
            (3, 10, 2, 1, 20),
        ],
    )
    def test_calculate_price_bgf_offer(
            self, quantity, single_unit_price, buy_quantity, get_quantity, expected_price
    ):
        offer = BgfOffer(single_unit_price, buy_quantity, get_quantity)
        assert offer.calculate_price(quantity) == expected_price


