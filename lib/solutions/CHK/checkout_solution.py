"""checkout_solution challenge."""

from collections import Counter

# noinspection PyUnusedLocal
# skus = unicode string


def compute_price_of_single_item_type(
    quantity: int, single_item_price: int, offer: tuple[int, int] = None
) -> int:
    """Input item quanity, normal single item price, tuple describing item offer. Returns total price including offers.

    This function is now unused, because the structure of offers available is more complicated.

    :param quantity: number of items purchased
    :param single_item_price: normal price of a single item (ie. without offer)
    :param offer: offer in the form of a tuple (<quantity>, <total_price>). Pass None if there is no offer.
    :return: total price after offers applied
    """
    if not (isinstance(quantity, int) and isinstance(single_item_price, int)):
        raise TypeError("quantity and single_item_price must be integers")
    if offer is None:
        return quantity * single_item_price
    elif not len(offer) == 2:
        raise IndexError("offer must be of the form (<quantity>, <total_price>)")
    elif not (
        isinstance(offer, tuple)
        and isinstance(offer[0], int)
        and isinstance(offer[1], int)
    ):
        raise TypeError("offer must be a tuple with types (int, int)")
    else:
        return (quantity // offer[0]) * offer[1] + (
            quantity % offer[0]
        ) * single_item_price


def checkout(skus: str) -> int:
    """Input SKU string. Returns total price including the offers available.

    :param skus: string of the SKUs for items in the basket. SKUs not present in item_prices are ignored.
    :return: total price of items in basket.
    """
    # set of items available
    item_set = {"A", "B", "C", "D", "E"}

    # skus must be a string.
    if not isinstance(skus, str):
        raise TypeError("skus must be a string")

    # If the set of characters in the skus string is not a subset of the item_prices keys, return -1
    if not set(skus) <= item_set:
        return -1

    # count occurences of each character in skus
    sku_counter = Counter(skus)

    # increment total price with each item type
    total_price = 0

    # SKU "A"
    a = sku_counter["A"]
    total_price += (a // 5) * 200 + ((y := a % 5) // 3) * 130 + (y % 3) * 50

    # SKU "B" depends on "E" so left until "E" is completed

    # SKU "C"
    c = sku_counter["C"]
    total_price += c * 20

    # SKU "D"
    d = sku_counter["D"]
    total_price += d * 15

    # SKU "E"
    e = sku_counter["E"]
    b = sku_counter["B"]
    total_price += e * 40
    b = max(0, b - (e // 2))

    # SKU "B"
    total_price += (b // 2) * 45 + (b % 2) * 30

    # Return total price
    return total_price

