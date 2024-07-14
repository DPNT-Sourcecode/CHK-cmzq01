# noinspection PyShadowingBuiltins,PyUnusedLocal
def compute(x: int, y: int) -> int:
    """Simple function to return the sum of two input integers.

    :param x: First integer
    :param y: Second integer
    :return: Sum of x and y
    """
    if x is not int or y is not int:
        raise TypeError("Inputs x and y must both be integers.")
    return x + y


