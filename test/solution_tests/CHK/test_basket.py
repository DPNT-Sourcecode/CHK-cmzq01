import pytest

from solutions.CHK.basket import *


@pytest.fixture
def small_price_list():
    return {
        "A": {
            LadderOffer(
                50,
                [
                    LadderDiscount(3, 130),
                    LadderDiscount(5, 200),
                ],
            )
        }
    }


# class TestBasket:
#
#     @pytest.mark.parametrize(
#         "quantity, single_unit_price, expected_price",
#         [
#             (10, OFFER_DATABASE,
#         ],
#     )
#     def test_basket_init(
#             self, quantity, single_unit_price, expected_price
#     ):
#         offer = SingleProductOffer(single_unit_price)
#         assert offer.calculate_price(quantity) == expected_price
