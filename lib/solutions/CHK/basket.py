from collections import Counter

# This should be from global config or external database, but for time's sake is kept here for now.
PRICE_LIST = {

}


class BasketItem:
    def __init__(self, quantity_raw: int):
        if not (isinstance(quantity_raw, int)):
            raise TypeError

        self.quantity_raw = quantity_raw
        self.quantity_corrected = None
        self.price = None


class Basket:
    def __init__(self, skus: str, price_list: dict):
        # skus must be a string.
        if not isinstance(skus, str):
            raise TypeError("skus must be a string")

        # If the set of characters in the skus string is not a subset of the item_prices keys, return -1
        if not set(skus) <= price_list.keys():
            raise IndexError

        # Get counts of SKUs - of the form {"A": count_a, "B": count_b, etc ....}
        sku_counter = Counter(skus)

        # Basket contents of the form {"A": BasketItem(count_a), "B": BasketItem(count_b), etc ....}
        self.basket_contents = {k: BasketItem(v) for k, v in sku_counter}

        # Basket uses cross-product offers associated to certain SKUs to correct the basket item counts
        self.apply_cross_product_offers()

        # Basket updates the price of each basket item
        self.calculate_all_prices()

        # Basket sets the final price
        self.final_price = sum([basket_item.price for basket_item in self.basket_contents])

    def apply_cross_product_offers(self):
        pass

    def calculate_all_prices(self):
        pass

    def get_final_price(self):
        pass

