import pytest
from deepdiff import DeepDiff

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
            "G": CrossProductOffer(10, 3, "C"),
        },
        "group_offers": {}
    }


@pytest.fixture
def small_offer_database_2():
    return {
        "single_sku_offers": {
            "A": MultiSubjectSkuOffer(10, {"A", "B", "C", "D"}, 3, 45),
            "B": MultiSubjectSkuOffer(15, {"A", "B", "C", "D"}, 3, 45),
            "C": MultiSubjectSkuOffer(20, {"A", "B", "C", "D"}, 3, 45),
            "D": MultiSubjectSkuOffer(25, {"A", "B", "C", "D"}, 3, 45),
            "E": BasicOffer(30),
        },
        "group_offers": {frozenset({"A", "B", "C", "D"}): {"quantity": 3, "price": 45}}
    }


class TestBasket:

    @pytest.mark.parametrize(
        "skus, expected_basket_contents",
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
                        "single_items": {
                            "A": BasketItem(16, 16, None),
                            "B": BasketItem(1, 0, None),
                            "C": BasketItem(18, 16, None),
                            "D": BasketItem(12, 12, None),
                            "E": BasketItem(20, 20, None),
                            "F": BasketItem(14, 14, None),
                            "G": BasketItem(7, 7, None),
                        },
                        "group_prices": {}
                    },
            ),
        ],
    )
    def test_basket_apply_all_cross_product_offers(self, skus, expected_basket_contents, small_offer_database_1):
        basket = Basket(skus, small_offer_database_1)
        basket.apply_all_cross_product_offers()
        assert DeepDiff(basket.basket_contents, expected_basket_contents) == {}

    @pytest.mark.parametrize(
        "skus, expected_basket_contents",
        [
            (
                    "AAAABBCCCCCCDEEEEE",
                    {
                        "single_items": {
                            "A": BasketItem(4, 1, None),
                            "B": BasketItem(2, 0, None),
                            "C": BasketItem(6, 0, None),
                            "D": BasketItem(1, 0, None),
                            "E": BasketItem(5, 5, None),
                        },
                        "group_prices": {
                            frozenset({"A", "B", "C", "D"}): 180,
                        }
                    }
            ),
        ],
    )
    def test_basket_apply_all_group_offers(
            self, skus, expected_basket_contents, small_offer_database_2
    ):
        basket = Basket(skus, small_offer_database_2)
        basket.apply_all_cross_product_offers()
        # assert basket.basket_contents == expected_basket_contents
