import pytest

from CHK.offers import *
from CHK.basket import *

# useful: python commands to generate random SKUs
# from string import ascii_uppercase
# "".join([f"\"{char}\" * {randint(0,20)}{' + ' if i != len(ascii_uppercase) - 1 else ''}" \
#   for (i, char) in enumerate(ascii_uppercase)])
# chars = ["A", "B", "C"]
# "".join([f"\"{char}\" * {randint(0,20)}{' + ' if i != len(chars) - 1 else ''}" for (i, char) in enumerate(chars)])


@pytest.fixture
def small_offer_database_1():
    return {
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
        "G": CrossProductOffer(10, 3, "C"),
    }


class TestBasket:

    @pytest.mark.parametrize(
        "skus, expected_basket_contents, expected_final_price",
        [
            (
                "A" * 16
                + "B" * 1
                + "C" * 18
                + "D" * 12
                + "E" * 20
                + "F" * 14
                + "G" * 7,
                {
                    "A": BasketItem(16, 16, None),
                    "B": BasketItem(1, 0, None),
                    "C": BasketItem(18, 16, None),
                    "D": BasketItem(12, 12, None),
                    "E": BasketItem(20, 20, None),
                    "F": BasketItem(14, 14, None),
                    "G": BasketItem(7, 7, None),
                },
                2120,
            ),
        ],
    )
    def test_basket_apply_all_cross_product_offers(
        self, skus, expected_basket_contents, expected_final_price, small_offer_database_1
    ):
        basket = Basket(skus, small_offer_database_1)
        basket.apply_all_cross_product_offers()
        assert basket.basket_contents.__hash__ == expected_basket_contents.__hash__



