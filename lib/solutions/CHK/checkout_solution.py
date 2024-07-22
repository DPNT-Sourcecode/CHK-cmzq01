"""checkout_solution challenge."""

from CHK.basket import Basket

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
    try:
        basket = Basket(skus)
        basket.apply_all_cross_product_offers()
        basket.calculate_all_prices()
        return basket.final_price
    except:
        return -1

