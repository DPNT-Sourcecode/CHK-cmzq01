import pytest

from solutions.CHK.checkout_solution import compute_price_of_single_item_type, checkout


class TestCheckout:

    @pytest.mark.parametrize(
        "quantity, single_item_price, offer, expected_price",
        [
            (10, 50, (3, 130), 440),
            (6, 30, (2, 45), 135),
            (13, 20, None, 260),
            (4, 15, None, 60),
        ],
    )
    def test_compute_price_of_single_item_type(self, quantity, single_item_price, offer, expected_price):
        assert compute_price_of_single_item_type(quantity, single_item_price, offer) == expected_price

    @pytest.mark.parametrize(
        "quantity, single_item_price, offer, expected_exception_class",
        [
            ("ten", 50, None, TypeError),
            (10, 50.0, None, TypeError),
            (10, 50, (), IndexError),
            (10, 50, [3, 130], TypeError),
            (10, 50, (3, "wrong"), TypeError),
            (10, 50, (3.0, 130), TypeError),
            (10, 50, (3, 130, "wrong"), IndexError),
        ],
    )
    def test_compute_price_of_single_item_type_exceptions(self, quantity, single_item_price, offer, expected_exception_class):
        with pytest.raises(expected_exception_class):
            compute_price_of_single_item_type(quantity, single_item_price, offer)

    @pytest.mark.parametrize(
        "skus, expected_price",
        [
            ("AAAA", 180),
            ("AFAGAHAI", 180),
            ("AABCAADABDCCCADB", 460),
        ]
    )
    def test_checkout(self, skus, expected_price):
        assert checkout(skus) == expected_price