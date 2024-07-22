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
def small_offer_database():
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
        "C": SingleSubjectSkuOffer(20),
        "D": SingleSubjectSkuOffer(15),
        "E": CrossProductOffer(40, "E", 2, "B"),
        "F": BgfOffer(10, 2),
        "G": CrossProductOffer(10, "G", 3, "C"),
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
                    "A": BasketItem(16, 16, 650),
                    "B": BasketItem(1, 0, 0),
                    "C": BasketItem(18, 16, 320),
                    "D": BasketItem(12, 12, 180),
                    "E": BasketItem(20, 20, 800),
                    "F": BasketItem(14, 14, 100),
                    "G": BasketItem(7, 7, 70),
                },
                2120,
            ),
        ],
    )
    def test_basket_contents_and_final_price(
        self, skus, expected_basket_contents, expected_final_price, small_offer_database
    ):
        # TODO: split this into cross-product application / price calculation using patch/mock
        basket = Basket(skus, small_offer_database)
        assert basket.basket_contents.__hash__ == expected_basket_contents.__hash__
        assert basket.final_price == expected_final_price






