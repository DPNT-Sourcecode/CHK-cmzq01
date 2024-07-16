import pytest

from solutions.CHK.checkout_solution import compute_price_of_single_item_type, checkout


class TestCheckout:

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
            ("BBEEEE", 160),
            ("EEEE", 160),
            ("BEEEE", 160),
            ("C" * 100, 2000),
            ("D" * 100, 1500),
            ("F", 10),
            ("FF", 20),
            ("FFF", 20),
            ("FFFF", 30),
            ("FFFFF", 40),
            ("FFFFFF", 40),
            ("F" * 99, 660),
            ("F" * 100, 670),
            ("F" * 101, 680),
            ("F" * 102, 680),
            ("F" * 103, 690),
            ("A" * 9 + "B" * 6 + "C" * 10 + "D" * 8 + "E" * 4 + "F" * 101, 1630),
            ("", 0),
            ("----", -1),
            ("abcd", -1),
            ("wxyz", -1),
        ],
    )
    def test_checkout(self, skus, expected_price):
        assert checkout(skus) == expected_price

