from solutions.SUM import sum_solution
import pytest


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
        "x, y, expected_exception",
        [
            (0.0, 0.0, TypeError),
        ]
    )
    def test_sum_exceptions(self, x, y, expected_exception):
        with pytest.raises(TypeError):
            sum_solution.compute(x, y)

