import pytest

from solutions.SUM import sum_solution


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
        assert sum_solution.compute(x, y) == expected_sum

    @pytest.mark.parametrize(
        "x, y, expected_exception_class",
        [
            (0.0, 0.0, TypeError),
            (15.6, 5, TypeError),
            (5, 15.6, TypeError),
            (-1, 100, sum_solution.InputOutOfRangeError),
            (101, 100, sum_solution.InputOutOfRangeError),
            (100, 101, sum_solution.InputOutOfRangeError),
            (100, -1, sum_solution.InputOutOfRangeError),
        ]
    )
    def test_sum_exceptions(self, x, y, expected_exception_class):
        with pytest.raises(expected_exception_class):
            sum_solution.compute(x, y)