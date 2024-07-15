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
    def __init__(self, single_unit_price: int, buy_quantity: int, get_quantity: int):
        super().__init__(single_unit_price)
        self.buy_quantity = buy_quantity
        self.get_quantity = get_quantity

    def calculate_price(self, quantity: int) -> int:
        return (quantity - quantity // (self.buy_quantity + self.get_quantity)) * self.single_unit_price


