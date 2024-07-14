"""sum_solution challenge."""

# noinspection PyShadowingBuiltins,PyUnusedLocal


class InputOutOfRangeError(Exception):
    """A simple exception class indicating integer inputs are out of range."""

    pass


def compute(x: int, y: int) -> int:
    """Input two integers x and y. Return their sum.

    :param x: First integer
    :param y: Second integer
    :return: Sum of x and y
    """
    # x and y must be integers, or raise TypeError.
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("Inputs x and y must both be integers.")

    # x and y must be between 0 and 100 inclusive, or raise InputOutOfRangeError.
    elif not (0 <= x <= 100 and 0 <= y <= 100):
        raise InputOutOfRangeError()

    # Return sum.
    return x + y
