# noinspection PyUnusedLocal
# skus = unicode string

def compute_price_of_single_item_type(quantity: int, single_price: int, offer: tuple[int, int] = None) -> int:
    """Input item quanity, normal single item price, tuple describing item offer. Returns total price including offers.

    :param quantity: number of items purchased
    :param single_price: normal price of a single item (ie. without offer)
    :param offer: offer in the form of a tuple (<quantity>, <total_price>). Pass None if there is no offer.
    :return: total price after offers applied
    """
    if offer is None:
        return quantity * single_price
    if not len(offer) == 2:
        raise IndexError("offer must be of the form (<quantity>, <total_price>)")
    elif not (isinstance(offer[0], int) and isinstance(offer[1], int)):
        raise TypeError("offer must be a tuple with types (int, int)")
    else:
        return (quantity // offer[0]) * offer[1] + (quantity % offer[0]) * single_price


def checkout(skus):
    raise NotImplementedError()

