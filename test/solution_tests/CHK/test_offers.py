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
        "quantity, single_unit_price, buy_quantity, expected_price",
        [
            (1, 10, 2, 10),
            (2, 10, 2, 20),
            (3, 10, 2, 20),
            (10, 100, 8, 900),
        ],
    )
    def test_calculate_price_bgf_offer(
            self, quantity, single_unit_price, buy_quantity, expected_price
    ):
        offer = BgfOffer(single_unit_price, buy_quantity)
        assert offer.calculate_price(quantity) == expected_price

    @pytest.mark.parametrize(
        "quantity, single_unit_price, buy_quantity, expected_exception_class",
        [
            (10.5, 5, 3, TypeError),
            (10, 5.5, 3, TypeError),
            (10, 5, 3.5, TypeError),
        ],
    )
    def test_calculate_price_bgf_offer_exceptions(
            self, quantity, single_unit_price, buy_quantity, expected_exception_class
    ):
        with pytest.raises(expected_exception_class):
            offer = BgfOffer(single_unit_price, buy_quantity)
            offer.calculate_price(quantity)

    @pytest.mark.parametrize(
        "quantity, single_unit_price, ladder_discounts, expected_price",
        [
            (
                    1,
                    50,
                    [
                        LadderDiscount(3, 130),
                        LadderDiscount(5, 200),
                    ],
                    50
            ),
            (
                    8, 50, [
                        LadderDiscount(3, 130),
                        LadderDiscount(5, 200),
                    ],
                    330
            ),
            (
                    9, 50, [
                        LadderDiscount(3, 130),
                        LadderDiscount(5, 200),
                    ],
                    380
            ),
            (
                    10, 50, [
                        LadderDiscount(3, 130),
                        LadderDiscount(5, 200),
                    ],
                    400
            ),
        ],
    )
    def test_calculate_price_ladder_offer(
            self, quantity, single_unit_price, ladder_discounts, expected_price
    ):
        offer = LadderOffer(single_unit_price, ladder_discounts)
        assert offer.calculate_price(quantity) == expected_price

    # @pytest.mark.parametrize(
    #     "quantity, single_unit_price, ladder_discounts, expected_exception_class",
    #     [
    #         (
    #             1,
    #             50,
    #             [
    #                 LadderDiscount(3, 130),
    #                 LadderDiscount(3, 200),
    #             ],
    #             DuplicateLadderDiscountException
    #         ),
    #         (
    #             1,
    #             50,
    #             [
    #                 LadderDiscount(3, 130),
    #                 LadderDiscount(1, 200),
    #             ],
    #             IndexError
    #         ),
    #         (
    #             1,
    #             50,
    #             [
    #                 LadderDiscount(3, 130),
    #                 LadderDiscount(0, 200),
    #             ],
    #             IndexError
    #         ),
    #     ]
    # )
    # def test_calculate_price_ladder_offer_exceptions(
    #         self, quantity, single_unit_price, ladder_discounts, expected_exception_class
    # ):
    #     with pytest.raises(expected_exception_class):
    #         offer = LadderOffer(single_unit_price, ladder_discounts)
    #         offer.calculate_price(quantity)

