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
    def test_compute_price_of_single_item_type(
        self, quantity, single_item_price, offer, expected_price
    ):
        assert (
            compute_price_of_single_item_type(quantity, single_item_price, offer)
            == expected_price
        )

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
    def test_compute_price_of_single_item_type_exceptions(
        self, quantity, single_item_price, offer, expected_exception_class
    ):
        with pytest.raises(expected_exception_class):
            compute_price_of_single_item_type(quantity, single_item_price, offer)

    @pytest.mark.parametrize(
        "skus, expected_price",
        [
            ("A", 50),
            ("AAAAAAAA", 330),
            ("AAAAAAAAA", 380),
            ("AAAAAAAAAA", 400),
            ("BBBBBBB", 165),
            ("BBBBBBEE", 120 + 80),
            ("BBBBBBEEE", 120 + 120),
            ("BBBBBBEEEE", 90 + 160),
            ("BEE", 80),
            ("BBEEEE", 80),
            ("EEEE", 80),
            ("BEEEE", 80),
            ("C" * 100, 2000),
            ("D" * 100, 1500),
            ("A" * 9 + "B" * 6 + "C" * 10 + "D" * 8 + "E" * 4, 380 + 90 + 160 + 2000 + 1470),
            ("", 0),
            ("AFAGAHAI", -1),
            ("FGHI", -1),
            ("WXYZ", -1),
            ("----", -1),
            ("abcd", -1),
            ("wxyz", -1),
        ],
    )
    def test_checkout(self, skus, expected_price):
        assert checkout(skus) == expected_price

