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




