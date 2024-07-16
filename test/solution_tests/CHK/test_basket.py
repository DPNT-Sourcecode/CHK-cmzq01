import pytest

from solutions.CHK.basket import *


@pytest.fixture
def small_price_list_1():
    return {
        "A":
            LadderOffer(
                50,
                [
                    LadderDiscount(3, 130),
                    LadderDiscount(5, 200),
                ],
            ),
        "B":
            LadderOffer(
                30,
                [
                    LadderDiscount(2, 45),
                ]
            ),
        "C": SingleProductOffer(20),
        "D": SingleProductOffer(15),
        "E": CrossProductOffer(40, "E", 2, "B"),
        "F": BgfOffer(10, 2),
        "G": CrossProductOffer(10, "G", 3, "C"),
    }


class TestBasket:

    @pytest.mark.parametrize(
        "skus, expected_basket_contents",
        [
            (
                    "A" * 16 + "B" * 1 + "C" * 18 + "D" * 12 + "E" * 20 + "F" * 14 + "G" * 7,
                    {
                        "A": BasketItem(16, 16, 0),
                        "B": BasketItem(1, 0, 0),
                        "C": BasketItem(18, 16, 0),
                        "D": BasketItem(12, 12, 0),
                        "E": BasketItem(20, 20, 0),
                        "F": BasketItem(14, 14, 0),
                        "G": BasketItem(7, 7, 0),

                    }),
        ],
    )
    def test_basket_apply_all_cross_product_offers(
            self, skus, expected_basket_contents, small_price_list_1
    ):
        basket = Basket(skus, small_price_list_1)
        assert basket.basket_contents == expected_basket_contents



