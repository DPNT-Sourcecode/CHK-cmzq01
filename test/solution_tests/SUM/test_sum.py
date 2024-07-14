import pytest

from solutions.SUM.sum_solution import InputOutOfRangeError, compute


class TestSum:

    @pytest.mark.parametrize(
        "x, y, expected_sum",
        [
            (0, 0, 0),
            (100, 100, 200),
            (31, 56, 87),
        ]
    )
    def test_sum(self, x, y, expected_sum):
        assert compute(x, y) == expected_sum

    @pytest.mark.parametrize(
        "x, y, expected_exception_class",
        [
            (0.0, 0.0, TypeError),
            (15.6, 5, TypeError),
            (5, 15.6, TypeError),
            ("string_input", {"dict": "input"}, TypeError),
            (-1, 100, InputOutOfRangeError),
            (101, 100, InputOutOfRangeError),
            (100, 101, InputOutOfRangeError),
            (100, -1, InputOutOfRangeError),
        ]
    )
    def test_sum_exceptions(self, x, y, expected_exception_class):
        with pytest.raises(expected_exception_class):
            compute(x, y)
