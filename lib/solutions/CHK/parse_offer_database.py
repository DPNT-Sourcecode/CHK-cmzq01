import re

from CHK.offers import SingleProductOffer, CrossProductOffer, LadderOffer, LadderDiscount, BgfOffer

single_ladder_pattern = r"\|\s*([A-Z])\s*\|\s*(\d+)\s*\|\s*(\d+)[A-Z]\s+for\s+(\d+)\s*\|"
double_ladder_pattern = r"\|\s*([A-Z])\s*\|\s*(\d+)\s*\|\s*(\d+)[A-Z]\s+for\s+(\d+),\s*(\d+)[A-Z]\s+for\s+(\d+)\s*\|"
cross_product_and_bgf_pattern = r"\|\s*([A-Z])\s*\|\s*(\d+)\s*\|\s*(\d+)[A-Z]\s+get\s+one\s+([A-Z])\s+free\s*\|"


def parse_line(line) -> tuple[str, [SingleProductOffer, CrossProductOffer]]:
    global single_ladder_pattern, double_ladder_pattern, cross_product_and_bgf_pattern
    return_sku = None
    return_offer = None

    if re.match(single_ladder_pattern, line):
        sku, single_unit_price, discount_quantity, discount_price = re.findall(single_ladder_pattern, line)[0]
        return_sku = sku
        return_offer = LadderOffer(int(single_unit_price), [LadderDiscount(int(discount_quantity), int(discount_price))])
    elif re.match(double_ladder_pattern, line):
        sku, single_unit_price, discount_1_quantity, discount_1_price, discount_2_quantity, discount_2_price = re.findall(double_ladder_pattern, line)[0]
        return_sku = sku
        return_offer = LadderOffer(
            single_unit_price, [
                LadderDiscount(discount_1_quantity, discount_1_price),
                LadderDiscount(discount_2_quantity, discount_2_price),
            ]
        )
    elif re.match(cross_product_and_bgf_pattern, line):
        subject_sku, single_unit_price, buy_quantity, target_sku = re.findall(cross_product_and_bgf_pattern, line)[0]
        if subject_sku == target_sku:
            return_sku = subject_sku
            return_offer = BgfOffer(single_unit_price, buy_quantity)
        else:
            return_sku = subject_sku
            return_offer = CrossProductOffer(single_unit_price, subject_sku, buy_quantity, target_sku)

    return return_sku, return_offer




