"""
Module containing classes representing single/cross product offers.
"""


class SingleProductOffer:
    """Base class for a single product offer. Not SKU-aware. Holds key information about the offer,
    and can be used to calculate the price of a quantity of items within this offer.
    """
    def __init__(self, single_unit_price: int):
        """Initialize self.

        :param single_unit_price: price for a single item
        """
        if not isinstance(single_unit_price, int):
            raise TypeError
        self.single_unit_price = single_unit_price

    def calculate_price(self, quantity: int) -> int:
        """Input quantity. Returns price.

        :param quantity: number of items
        :return: price of items
        """
        if not isinstance(quantity, int):
            raise TypeError
        return self.single_unit_price * quantity


class BgfOffer(SingleProductOffer):
    """Buy X get 1 free offer class.
    """
    def __init__(self, single_unit_price: int, buy_quantity: int):
        """Initialize self.

        :param single_unit_price: price for a single item
        :param buy_quantity: number required to get 1 free
        """
        super().__init__(single_unit_price)
        if not isinstance(buy_quantity, int):
            raise TypeError
        self.buy_quantity = buy_quantity

    def calculate_price(self, quantity: int) -> int:
        """Input quantity. Returns price.

        :param quantity: number of items
        :return: price of items
        """
        if not isinstance(quantity, int):
            raise TypeError
        return (quantity - quantity // (self.buy_quantity + 1)) * self.single_unit_price


class DuplicateLadderDiscountException(Exception):
    """Custom exception raised when duplicate LadderDiscount quantity values are seen in a LadderOffer.
    """
    pass


class InvalidLadderDiscountQuantityException(Exception):
    """Custom exception raised when LadderDiscount quantity is 0 or 1.
    """
    pass


class LadderDiscount:
    """Class representing a "Ladder Discount". For example "buy 3 for 80".
    """
    def __init__(self, quantity: int, total_price: int):
        """Initialize self.

        :param quantity: number of items to qualify for discount
        :param total_price: total price of the items
        """
        if not(isinstance(quantity, int) and isinstance(total_price, int)):
            raise TypeError
        if quantity <= 1:
            raise(InvalidLadderDiscountQuantityException)
        self.quantity = quantity
        self.total_price = total_price

    def __eq__(self, other):
        return self.quantity == other.quantity

    def __gt__(self, other):
        return self.quantity > other.quantity

    def __lt__(self, other):
        return self.quantity < other.quantity

    def __hash__(self):
        return hash(self.quantity)


class LadderOffer(SingleProductOffer):
    """Class representing a "Ladder Offer", composed of multiple "Ladder Discounts".
    """
    def __init__(self, single_unit_price: int, ladder_discounts: list[LadderDiscount]):
        """Input single_unit_price and list of ladder discounts. ladder_discounts will be sorted by quantity in reverse,
        and have basic "remainder" ladder appended before setting as attribute.

        :param single_unit_price: price of a single unit (the final basic "remainder" ladder considered)
        :param ladder_discounts: list of LadderDiscounts (no ladder may contain 0 or 1 as quantity)
        """
        super().__init__(single_unit_price)
        self.single_unit_price = single_unit_price

        # Check for duplicate discounts in the ladder, which don't make sense.
        if len(ladder_discounts) != len(set(ladder_discounts)):
            raise DuplicateLadderDiscountException

        # TODO: possibly some other validation checking on ladder_discounts.
        if any(ladder_discount.quantity <= 1 for ladder_discount in ladder_discounts):
            raise InvalidLadderDiscountQuantityException
        # Add the final ladder discount for the single unit price.
        self.ladder_discounts = (ladder_discounts + [LadderDiscount(1, single_unit_price)])
        self.ladder_discounts.sort(reverse=True)

    def calculate_price(self, quantity: int) -> int:
        """Input quantity. Returns price.

        :param quantity: number of items
        :return: price of items
        """
        if not isinstance(quantity, int):
            raise TypeError

        # variables to keep track of, going down the ladders.
        y = quantity
        price = 0

        # Cycle down the ladders, adding the price at each level
        for ladder_discount in self.ladder_discounts:
            price += (y // ladder_discount.quantity) * ladder_discount.total_price
            y = y % ladder_discount.quantity

        # Return total price
        return price


class CrossProductOffer:
    """Class representing a cross-product offer that is SKU-aware. To be used by Baskets to correct the count of each
    item type before computing the final price, so other single product offers can be applied.
    """
    def __init__(
            self,
            subject_sku: str,
            subject_quantity_buy: int,
            target_sku: str,
            target_quantity_free: int
    ):
        """Initialize self.

        :param subject_sku: type of SKU to buy to get this offer
        :param subject_quantity_buy: quantity of items to buy to get this offer
        :param target_sku: type of SKU given free as part of this offer
        :param target_quantity_free: quantity of items given free as part of this offer
        """
        if not (
                isinstance(subject_sku, str)
                and isinstance(subject_quantity_buy, int)
                and isinstance(target_sku, str)
                and isinstance(target_quantity_free, int)
        ):
            raise TypeError
        self.subject_sku = subject_sku
        self.subject_quantity_buy = subject_quantity_buy
        self.target_sku = target_sku
        self.target_quantity_free = target_quantity_free


