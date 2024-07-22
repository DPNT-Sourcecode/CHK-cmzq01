"""Module containing classes representing single/cross product offers."""

from typeguard import typechecked


@typechecked
class SingleSubjectSkuOffer:
    """Base class for a single product offer."""

    def __init__(self, single_unit_price: int):
        """Initialize self.

        :param single_unit_price: price for a single item
        """
        if not isinstance(single_unit_price, int):
            raise TypeError
        self.single_unit_price = single_unit_price

    @typechecked
    def calculate_price(self, quantity: int) -> int:
        """Input quantity. Returns price.

        :param quantity: number of items
        :return: price of items
        """
        return self.single_unit_price * quantity

    def __eq__(self, other):
        """Equality magic method.

        :param other: other instance
        :return: if self is equal to other
        """
        return self.single_unit_price == other.single_unit_price


class BgfOffer(SingleSubjectSkuOffer):
    """Buy X get 1 free offer class."""

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

    def __eq__(self, other):
        """Equality magic method.

        :param other: other instance
        :return: if self is equal to other
        """
        return (
            self.single_unit_price == other.single_unit_price
            and self.buy_quantity == other.buy_quantity
        )


class DuplicateLadderDiscountException(Exception):
    """Custom exception raised when duplicate LadderDiscount quantity values are seen in a LadderOffer."""

    pass


class InvalidLadderDiscountQuantityException(Exception):
    """Custom exception raised when LadderDiscount quantity is 0 or 1."""

    pass


class LadderDiscount:
    """Class representing a "Ladder Discount". For example "buy 3 for 80"."""

    def __init__(self, quantity: int, total_price: int):
        """Initialize self.

        :param quantity: number of items to qualify for discount
        :param total_price: total price of the items
        """
        if not (isinstance(quantity, int) and isinstance(total_price, int)):
            raise TypeError

        self.quantity = quantity
        self.total_price = total_price

    def __eq__(self, other):
        """Equals magic method.

        :param other: other instance
        :return: whether self is equal to other
        """
        return self.quantity == other.quantity and self.total_price == other.total_price

    def __gt__(self, other):
        """Greater than magic method.

        :param other: other instance
        :return: whether self is greater than other
        """
        return self.quantity > other.quantity

    def __lt__(self, other):
        """Less than magic method.

        :param other: other instance
        :return: whether self is less than other
        """
        return self.quantity < other.quantity

    def __hash__(self):
        """Hash magic method.

        :return: hash of instance
        """
        return hash(self.quantity)


class LadderOffer(SingleSubjectSkuOffer):
    """Class representing a "Ladder Offer", composed of multiple "Ladder Discounts"."""

    def __init__(self, single_unit_price: int, ladder_discounts: list[LadderDiscount]):
        """Initialize self.

        :param single_unit_price: price of a single unit (the final basic "remainder" ladder considered)
        :param ladder_discounts: list of LadderDiscounts (no ladder may contain 0 or 1 as quantity)
        """
        super().__init__(single_unit_price)

        # Check for duplicate discounts in the ladder, which don't make sense.
        ladder_discount_quantities = [
            ladder_discount.quantity for ladder_discount in ladder_discounts
        ]
        if len(ladder_discount_quantities) != len(set(ladder_discount_quantities)):
            raise DuplicateLadderDiscountException

        # TODO: possibly some other validation checking on ladder_discounts.
        if any(ladder_discount.quantity <= 1 for ladder_discount in ladder_discounts):
            raise InvalidLadderDiscountQuantityException
        # Add the final ladder discount for the single unit price.
        self.ladder_discounts = ladder_discounts + [
            LadderDiscount(1, single_unit_price)
        ]
        self.ladder_discounts.sort(reverse=True)

    def __eq__(self, other):
        """Equality magic method.

        :param other: other instance
        :return: if self is equal to other
        """
        return (
            self.single_unit_price == other.single_unit_price
            and self.ladder_discounts == other.ladder_discounts
        )

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


class CrossProductOffer(SingleSubjectSkuOffer):
    """Class representing a cross-product offer that is SKU-aware."""

    def __init__(
        self,
        single_unit_price: int,
        subject_quantity_buy: int,
        target_sku: str,
    ):
        """Initialize self.

        :param subject_sku: type of SKU to buy to get this offer
        :param subject_quantity_buy: quantity of items to buy to get this offer
        :param target_sku: type of SKU given one free as part of this offer
        """
        super().__init__(single_unit_price)
        if not (
            isinstance(single_unit_price, int)
            and isinstance(subject_quantity_buy, int)
            and isinstance(target_sku, str)
        ):
            raise TypeError
        self.single_unit_price = single_unit_price
        self.subject_quantity_buy = subject_quantity_buy
        self.target_sku = target_sku

    def __eq__(self, other):
        """Equality magic method.

        :param other: other instance
        :return: if self is equal to other
        """
        return (
            self.single_unit_price == other.single_unit_price
            and self.subject_quantity_buy == other.subject_quantity_buy
            and self.target_sku == other.target_sku
        )




