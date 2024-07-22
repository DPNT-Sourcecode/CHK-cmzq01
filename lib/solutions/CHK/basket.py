"""Module containing class representing basket of items at checkout."""

import os
from collections import Counter
from CHK.offers import CrossProductOffer
from CHK.parse_offer_database import parse_offer_database_file


# Load the database of offers
database_filename = f"{os.path.dirname(__file__)}/offer_database.txt"
OFFER_DATABASE = parse_offer_database_file(database_filename)


class BasketItem:
    """Simple class representing one type of item."""

    def __init__(self, quantity_raw: int, quantity_corrected=None, price=None):
        """Initialize self.

        :param quantity_raw: raw quantity of item.
        :param quantity_corrected: Only use input during testing. If not input, will be set to raw quantity.
        :param price: Only use input during testing. If not input, will be set to None and calculated later by basket.
        """
        if not (isinstance(quantity_raw, int)):
            raise TypeError

        self.quantity_raw = quantity_raw
        # For unit testing
        self.quantity_corrected = (
            quantity_raw if quantity_corrected is None else quantity_corrected
        )
        self.price = price


class Basket:
    """Class representing a basket of items."""

    def __init__(self, skus: str, offer_database: dict = OFFER_DATABASE):
        """Initialize self.

        :param skus: string of SKUs.
        :param offer_database: dict containing prices/offers on products.
        """
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

        # Need list of all SKUs to add zero counts to some of basket_contents
        all_skus = offer_database.keys()

        # Basket contents of the form {"A": BasketItem(count_a), "B": BasketItem(count_b), etc ....}
        self.basket_contents = {
            k: BasketItem(sku_counter[k]) if k in sku_counter else BasketItem(0)
            for k in all_skus
        }

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
        """Apply all cross-product offers on the basket.

        :return: void
        """
        for sku, basket_item in self.basket_contents.items():
            offer = self.offer_database[sku]
            if isinstance(offer, CrossProductOffer):
                self.apply_cross_product_offer(sku, offer)

    def apply_cross_product_offer(self, sku: str, offer: CrossProductOffer):
        """Apply single cross-product offer on the basket.

        :param offer: offer to apply
        :param sku: subject SKU (buying this SKU can save on the target SKU of the offer)
        :return: void
        """
        target_sku = offer.target_sku
        target_quantity = self.basket_contents[target_sku].quantity_corrected
        subject_sku = sku
        subject_quantity = self.basket_contents[subject_sku].quantity_raw
        subject_quantity_buy = offer.subject_quantity_buy
        self.basket_contents[target_sku].quantity_corrected = max(
            0, target_quantity - (subject_quantity // subject_quantity_buy)
        )

    def calculate_all_prices(self):
        """Calculate all prices for the individual items in the basket contents.

        :return: void
        """
        for sku, basket_item in self.basket_contents.items():
            offer = self.offer_database[sku]
            basket_item.price = offer.calculate_price(basket_item.quantity_corrected)
