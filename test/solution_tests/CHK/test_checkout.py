import pytest

from solutions.CHK.checkout_solution import compute_price_of_single_item_type, checkout


class TestCheckout:

    @pytest.mark.parametrize(
        "quantity, single_price, offer, expected_price",
        [
            (10, 50, (3, 130), 440),
            (6, 30, (2, 45), 135),
        ],
    )
    def test_compute_price_of_single_item_type(self, quantity, single_price, offer, expected_price):
        assert compute_price_of_single_item_type(quantity, single_price, offer) == expected_price
