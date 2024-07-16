"""Module containing class representing basket of items at checkout."""

from collections import Counter
from CHK.offers import *

# This should be from global config or external database, but for time's sake is kept here for now.
OFFER_DATABASE = {
    "A":
        LadderOffer(
            50,
            [
                LadderDiscount(3, 130),
                LadderDiscount(5, 200),
            ],
        ),
    "B":
        LadderOffer(
            30,
            [
                LadderDiscount(2, 45),
            ],
        ),
    "C": SingleProductOffer(20),
    "D": SingleProductOffer(15),
    "E": CrossProductOffer(40, "E", 2, "B"),
    "F": BgfOffer(10, 2),
}


class BasketItem:
    def __init__(self, quantity_raw: int, quantity_corrected=None, price=None):
        if not (isinstance(quantity_raw, int)):
            raise TypeError

        self.quantity_raw = quantity_raw
        # For unit testing
        self.quantity_corrected = quantity_raw if quantity_corrected is None else quantity_corrected
        self.price = price

    def __hash__(self):
        """Hash magic method.

        :return: hash of instance
        """
        return hash(str(self.quantity_raw) + str(self.quantity_corrected) + str(self.price))

class Basket:
    def __init__(self, skus: str, offer_database: dict):
        # skus must be a string.
        if not isinstance(skus, str):
            raise TypeError("skus must be a string")

        if not isinstance(offer_database, dict):
            raise TypeError("offer_database must be a dict")

        # If the set of characters in the skus string is not a subset of the item_prices keys, return -1
        if not set(skus) <= offer_database.keys():
            raise IndexError

        # Get counts of SKUs - of the form {"A": count_a, "B": count_b, etc ....}
        sku_counter = Counter(skus)

        # Basket contents of the form {"A": BasketItem(count_a), "B": BasketItem(count_b), etc ....}
        self.basket_contents = {k: BasketItem(v) for k, v in sku_counter.items()}

        self.offer_database = offer_database

        # Basket uses cross-product offers associated to certain SKUs to correct the basket item counts
        self.apply_all_cross_product_offers()

        # Basket updates the price of each basket item
        (self.calculate_all_prices())

        # Basket sets the final price
        self.final_price = sum(
            [basket_item.price for _, basket_item in self.basket_contents.items()]
        )

    def apply_all_cross_product_offers(self):
        for sku, basket_item in self.basket_contents.items():
            offer = self.offer_database[sku]
            if isinstance(offer, CrossProductOffer):
                self.apply_cross_product_offer(offer)

    def apply_cross_product_offer(self, offer: CrossProductOffer):
        target_sku = offer.target_sku
        target_quantity = self.basket_contents[target_sku].quantity_corrected
        subject_sku = offer.subject_sku
        subject_quantity = self.basket_contents[subject_sku].quantity_raw
        subject_quantity_buy = offer.subject_quantity_buy
        self.basket_contents[target_sku].quantity_corrected = max(
            0, target_quantity - (subject_quantity // subject_quantity_buy)
        )

    def calculate_all_prices(self):
        for sku, basket_item in self.basket_contents.items():
            offer = self.offer_database[sku]
            basket_item.price = offer.calculate_price(basket_item.quantity_corrected)

