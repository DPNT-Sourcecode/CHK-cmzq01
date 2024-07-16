import re

from CHK.offers import SingleProductOffer, CrossProductOffer, LadderOffer, LadderDiscount, BgfOffer

single_price_pattern = r"\|\s*([A-Z])\s*\|\s*(\d+)\s*\|\s*\|"
single_ladder_pattern = r"\|\s*([A-Z])\s*\|\s*(\d+)\s*\|\s*(\d+)[A-Z]\s+for\s+(\d+)\s*\|"
double_ladder_pattern = r"\|\s*([A-Z])\s*\|\s*(\d+)\s*\|\s*(\d+)[A-Z]\s+for\s+(\d+),\s*(\d+)[A-Z]\s+for\s+(\d+)\s*\|"
cross_product_and_bgf_pattern = r"\|\s*([A-Z])\s*\|\s*(\d+)\s*\|\s*(\d+)[A-Z]\s+get\s+one\s+([A-Z])\s+free\s*\|"

offer_database_second_line_patter = r"\|\s.*Item\s.*\|\s.*Price\s.*\|\s.*Special offers\s.*\|"

def parse_line(line) -> tuple[str, [SingleProductOffer, CrossProductOffer]]:
    global single_ladder_pattern, double_ladder_pattern, cross_product_and_bgf_pattern
    return_sku = None
    return_offer = None

    if re.match(single_price_pattern, line):
        sku, single_unit_price = re.findall(single_price_pattern, line)[0]
        return_sku = sku
        return_offer = SingleProductOffer(int(single_unit_price))
    elif re.match(single_ladder_pattern, line):
        sku, single_unit_price, discount_quantity, discount_price = re.findall(single_ladder_pattern, line)[0]
        return_sku = sku
        return_offer = LadderOffer(int(single_unit_price), [LadderDiscount(int(discount_quantity), int(discount_price))])
    elif re.match(double_ladder_pattern, line):
        sku, single_unit_price, discount_1_quantity, discount_1_price, discount_2_quantity, discount_2_price = re.findall(double_ladder_pattern, line)[0]
        return_sku = sku
        return_offer = LadderOffer(
            int(single_unit_price), [
                LadderDiscount(int(discount_1_quantity), int(discount_1_price)),
                LadderDiscount(int(discount_2_quantity), int(discount_2_price)),
            ]
        )
    elif re.match(cross_product_and_bgf_pattern, line):
        subject_sku, single_unit_price, buy_quantity, target_sku = re.findall(cross_product_and_bgf_pattern, line)[0]
        if subject_sku == target_sku:
            return_sku = subject_sku
            return_offer = BgfOffer(int(single_unit_price), int(buy_quantity))
        else:
            return_sku = subject_sku
            return_offer = CrossProductOffer(int(single_unit_price), subject_sku, int(buy_quantity), target_sku)

    return return_sku, return_offer

class InvalidOfferDatabaseFile(Exception):
    pass


def parse_offer_database_file(filename):
    offer_database = {}
    with open(filename) as f:
        try:
            # Check second line for column signature
            l1 = f.readline().rstrip("\n")
            l2 = f.readline().rstrip("\n")
            if not re.match(offer_database_second_line_patter, l2):
                raise InvalidOfferDatabaseFile
            while line := f.readline():
                sku, offer = parse_line(line)
                if sku is not None and offer is not None:
                    offer_database[sku] = offer
            return offer_database
        except:
            raise InvalidOfferDatabaseFile


