class SingleProductOffer:
    def __init__(self, single_unit_price: int):
        if not isinstance(single_unit_price, int):
            raise TypeError
        self.single_unit_price = single_unit_price

    def calculate_price(self, quantity: int) -> int:
        if not isinstance(quantity, int):
            raise TypeError
        return self.single_unit_price * quantity


class BgfOffer(SingleProductOffer):
    def __init__(self, single_unit_price: int, buy_quantity: int):
        super().__init__(single_unit_price)
        if not isinstance(buy_quantity, int):
            raise TypeError
        self.buy_quantity = buy_quantity

    def calculate_price(self, quantity: int) -> int:
        if not isinstance(quantity, int):
            raise TypeError
        return (quantity - quantity // (self.buy_quantity + 1)) * self.single_unit_price


class LadderDiscount:
    def __init__(self, quantity: int, total_price: int):
        if not(isinstance(quantity, int) and isinstance(total_price, int)):
            raise TypeError
        self.quantity = quantity
        self.total_price = total_price

    def __eq__(self, other):
        return self.quantity == other.quantity

    def __gt__(self, other):
        return self.quantity > other.quantity

    def __lt__(self, other):
        return self.quantity < other.quantity


class DuplicateLadderDiscountException(Exception):
    pass


class InvalidLadderDiscountQuantityException(Exception):
    pass


class LadderOffer(SingleProductOffer):
    def __init__(self, single_unit_price: int, ladder_discounts: list[LadderDiscount]):
        super().__init__(single_unit_price)
        self.single_unit_price = single_unit_price

        # Check for duplicate discounts in the ladder, which don't make sense.
        if len(ladder_discounts) != len(set(ladder_discounts)):
            raise DuplicateLadderDiscountException

        # TODO: some other validation checking on ladder_discounts.
        if any(ladder_discount.quantity <= 1 for ladder_discount in ladder_discounts):
            raise(InvalidLadderDiscountQuantityException)
        # Add the final ladder discount for the single unit price.
        self.ladder_discounts = (ladder_discounts + [LadderDiscount(1, single_unit_price)])
        self.ladder_discounts.sort(reverse=True)

    def calculate_price(self, quantity: int) -> int:
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



