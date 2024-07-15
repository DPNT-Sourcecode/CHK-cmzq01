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


class LadderOffer(SingleProductOffer):
    def __init__(self, single_unit_price: int, ladder_discounts: list[LadderDiscount]):
        super().__init__(single_unit_price)
        self.single_unit_price = single_unit_price
        # TODO: check for duplicated "quantity" fields across ladder_discounts, and that
        self.ladder_discounts = (ladder_discounts + [LadderDiscount(1, single_unit_price)]).sort(reverse=True)

    def calculate_price(self, quantity: int) -> int:
        # variables to keep track going down the ladders
        y = quantity
        price = 0

        # Cycle down the ladders, adding the price at each level
        for ladder_discount in self.ladder_discounts:
            price += (y // ladder_discount.quantity) * ladder_discount.price
            y = y % ladder_discount.quantity

        # Return total price
        return price


