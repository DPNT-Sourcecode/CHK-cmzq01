# noinspection PyShadowingBuiltins,PyUnusedLocal

class InputOutOfRangeError(Exception):
    """A simple exception class indicating integers inputs are out of range.
    """
    def __init__(self):
        pass


def compute(x: int, y: int) -> int:
    """Simple function to return the sum of two input integers.

    :param x: First integer
    :param y: Second integer
    :return: Sum of x and y
    """

    # x and y must be integers, or raise TypeError.
    if x is not int or y is not int:
        raise TypeError("Inputs x and y must both be integers.")

    # x and y must be between 0 and 100 inclusive, or raise InputOutOfRangeError.
    elif not (0 <= x <= 100 and 0 <= y <= 100):
        raise InputOutOfRangeError()

    # Return sum.
    return x + y
