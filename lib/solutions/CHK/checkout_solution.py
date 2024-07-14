# noinspection PyUnusedLocal
# skus = unicode string

def compute_price_of_single_item_type(quantity: int, single_price: int, offer: dict) -> int:
    """Input item quanity, normal single item price, tuple describing item offer. Returns total price including offers.

    :param quantity: number of items purchased
    :param single_price: normal price of a single item (ie. without offer)
    :param offer: offer in the form of a tuple (<quantity>, <total_price>)
    :return: total price after offers applied
    """
    return (quantity // offer[0]) * offer[1] + (quantity % offer[0]) * single_price


def checkout(skus):
    raise NotImplementedError()
