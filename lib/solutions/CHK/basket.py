"""Module containing class representing basket of items at checkout."""

import os
from collections import Counter
from CHK.offers import CrossProductOffer
from CHK.parse_offer_database import parse_offer_database_file
from typeguard import typechecked

# Load the database of offers
database_filename = f"{os.path.dirname(__file__)}/offer_database.txt"
OFFER_DATABASE = parse_offer_database_file(database_filename)


@typechecked
class BasketItem:
    """Simple class representing one type of item."""

    def __init__(self, quantity_raw: int, quantity_corrected=None, price=None):
        """Initialize self.

        :param quantity_raw: raw quantity of item.
        :param quantity_corrected: Only use input during testing. If not input, will be set to raw quantity.
        :param price: Only use input during testing. If not input, will be set to None and calculated later by basket.
        """
        self.quantity_raw = quantity_raw
        # For unit testing
        self.quantity_corrected = (
            quantity_raw if quantity_corrected is None else quantity_corrected
        )
        self.price = price

    def __eq__(self, other):
        return (self.quantity_raw == other.quantity_raw
                and self.quantity_corrected == other.quantity_corrected
                and self.price == other.price
                )


@typechecked
class Basket:
    """Class representing a basket of items."""

    def __init__(self, skus: str, offer_database: dict = OFFER_DATABASE):
        """Initialize self.

        :param skus: string of SKUs.
        :param offer_database: dict containing prices/offers on products.
        """
        # If the set of characters in the skus string is not a subset of the item_prices keys, return -1
        if not set(skus) <= offer_database["single_sku_offers"].keys():
            raise IndexError

        # Get counts of SKUs - of the form {"A": count_a, "B": count_b, etc ....}
        sku_counter = Counter(skus)

        # Need list of all SKUs to add zero counts to some of basket_contents
        all_skus = offer_database["single_sku_offers"].keys()

        basket_contents = {"single_items": {}, "group_prices": {}}

        # Basket contents of the form {"A": BasketItem(count_a), "B": BasketItem(count_b), etc ....}
        basket_contents["single_items"] = {
            k: BasketItem(sku_counter[k])
            for k in all_skus
        }

        self.basket_contents = basket_contents

        self.offer_database = offer_database

    def apply_all_cross_product_offers(self):
        """Apply all cross-product offers on the basket.

        :return: void
        """
        for sku, basket_item in self.basket_contents["single_items"].items():
            offer = self.offer_database["single_sku_offers"][sku]
            if isinstance(offer, CrossProductOffer):
                self.apply_cross_product_offer(sku, offer)

    def apply_cross_product_offer(self, sku: str, offer: CrossProductOffer):
        """Apply single cross-product offer on the basket.

        :param offer: offer to apply
        :param sku: subject SKU (buying this SKU can save on the target SKU of the offer)
        :return: void
        """
        target_sku = offer.target_sku
        target_quantity = self.basket_contents["single_items"][target_sku].quantity_corrected
        subject_sku = sku
        subject_quantity = self.basket_contents["single_items"][subject_sku].quantity_raw
        subject_quantity_buy = offer.subject_quantity_buy
        self.basket_contents["single_items"][target_sku].quantity_corrected = max(
            0, target_quantity - (subject_quantity // subject_quantity_buy)
        )

    def apply_all_group_offers(self):
        for sku_group, offer_details in self.offer_database["group_offers"].items():
            sub_contents = dict(filter(lambda i: i[0] in sku_group, self.basket_contents["single_items"].items()))
            new_sub_contents, group_price = self.apply_group_offer(sub_contents, offer_details["quantity"], offer_details["price"])
            self.basket_contents["single_items"] = self.basket_contents["single_items"] | new_sub_contents
            try:
                self.basket_contents["group_prices"][sku_group]["price"] = group_price
            except Exception as e:
                pass

    def apply_group_offer(self, input_dict, quan, price):
        input_dict_sorted = sorted(input_dict.items(), key=lambda item: self.offer_database["single_sku_offers"][item[0]].single_unit_price, reverse=True)
        total_quantity = sum([v.quantity_raw for _, v in input_dict_sorted])
        total_price = (total_quantity // quan) * price
        tmp_sku_string = "".join([k*v.quantity_raw for k,v in input_dict_sorted])
        remainder = total_quantity % quan
        sku_remainder = tmp_sku_string[-remainder:]
        sku_remainder_counts = Counter(sku_remainder)
        output_dict = dict(input_dict)
        for k,v in output_dict.items():
            output_dict[k].quantity_corrected = sku_remainder_counts[k]
        return output_dict, total_price

    def calculate_all_prices(self):
        """Calculate all prices for the individual items in the basket contents.

        Also computes final price and sets final_price on Basket.
        :return: void
        """
        for sku, basket_item in self.basket_contents.items():
            offer = self.offer_database["single_sku_offers"][sku]
            basket_item.price = offer.calculate_price(basket_item.quantity_corrected)
        self.final_price = sum(
            [basket_item.price for _, basket_item in self.basket_contents.items()]
        )






