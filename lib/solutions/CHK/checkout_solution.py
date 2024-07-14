"""checkout_solution challenge."""

from collections import Counter

# noinspection PyUnusedLocal
# skus = unicode string


def compute_price_of_single_item_type(
    quantity: int, single_item_price: int, offer: tuple[int, int] = None
) -> int:
    """Input item quanity, normal single item price, tuple describing item offer. Returns total price including offers.

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


def checkout(
    skus: str,
    item_prices: dict = {
        "A": (50, (3, 130)),
        "B": (30, (2, 45)),
        "C": (20, None),
        "D": (15, None),
    },
) -> int:
    """Input SKU string (and optionally item_prices as a dict). Returns total price.

    :param skus: string of the SKUs for items in the basket. SKUs not present in item_prices are ignored.
    :param item_prices: dict with entries of the form {<sku>:(<single_price>, (<offer_quantity>, <offer_total_price>))}.
    For now, requirements do not require this to be a variable, but it is expected to be useful later. A database could
    be useful for this information also.
    :return: total price of items in basket.
    """
    # skus must be a string.
    if not isinstance(skus, str):
        raise TypeError("skus must be a string")

    # count occurences of each character in skus
    sku_counter = Counter(skus)
    total_price = 0
    for item, prices in item_prices.items():
        quantity = sku_counter[item]
        single_price = prices[0]
        offer = prices[1]
        total_price += compute_price_of_single_item_type(quantity, single_price, offer)
    return total_price

