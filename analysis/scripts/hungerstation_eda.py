#!/usr/bin/env python3

import argparse
import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_INPUT = Path("/Users/qq-nux/Downloads/hungerstation_restaurants.json")
DEFAULT_OUTPUT_DIR = Path("analysis/hungerstation")


def parse_args():
    parser = argparse.ArgumentParser(description="Run EDA on Hungerstation restaurant JSON data.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Path to the input JSON file.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for EDA outputs.")
    return parser.parse_args()


def pct(part, whole):
    return (part / whole * 100.0) if whole else 0.0


def round_or_none(value, digits=2):
    if value is None:
        return None
    return round(value, digits)


def parse_number(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return float(int(value))
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip().replace(",", "")
        if not stripped:
            return None
        try:
            return float(stripped)
        except ValueError:
            return None
    return None


def quantile(sorted_values, probability):
    if not sorted_values:
        return None
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = (len(sorted_values) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    fraction = position - lower
    return sorted_values[lower] + (sorted_values[upper] - sorted_values[lower]) * fraction


def numeric_summary(values):
    cleaned = [float(v) for v in values if v is not None and not math.isnan(float(v))]
    if not cleaned:
        return {
            "count": 0,
            "missing": 0,
            "zeros": 0,
            "negatives": 0,
            "min": None,
            "p01": None,
            "p05": None,
            "p25": None,
            "median": None,
            "p75": None,
            "p95": None,
            "p99": None,
            "max": None,
            "mean": None,
            "stddev": None,
        }
    cleaned.sort()
    mean_value = statistics.fmean(cleaned)
    stddev_value = statistics.pstdev(cleaned) if len(cleaned) > 1 else 0.0
    return {
        "count": len(cleaned),
        "missing": 0,
        "zeros": sum(1 for v in cleaned if v == 0),
        "negatives": sum(1 for v in cleaned if v < 0),
        "min": cleaned[0],
        "p01": quantile(cleaned, 0.01),
        "p05": quantile(cleaned, 0.05),
        "p25": quantile(cleaned, 0.25),
        "median": quantile(cleaned, 0.50),
        "p75": quantile(cleaned, 0.75),
        "p95": quantile(cleaned, 0.95),
        "p99": quantile(cleaned, 0.99),
        "max": cleaned[-1],
        "mean": mean_value,
        "stddev": stddev_value,
    }


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows, columns):
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join([header, separator] + body)


def canonical_promotion(promotion):
    if not isinstance(promotion, dict):
        return None
    return (
        promotion.get("name"),
        promotion.get("type"),
        promotion.get("category"),
        promotion.get("minimum_order"),
    )


def counter_to_rows(counter, dimension, total, limit=None):
    rows = []
    items = counter.most_common(limit)
    for value, count in items:
        rows.append(
            {
                "dimension": dimension,
                "value": value,
                "count": count,
                "pct_of_total": round(pct(count, total), 4),
            }
        )
    return rows


def tuple_label(values):
    if not values:
        return "(empty)"
    return " | ".join(str(v) for v in values)


def main():
    args = parse_args()
    input_path = args.input.expanduser().resolve()
    output_dir = args.output if args.output.is_absolute() else (Path.cwd() / args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    reports_dir = output_dir / "reports"
    tables_dir = output_dir / "tables"
    metadata_dir = output_dir / "metadata"
    reports_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)

    with input_path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError("Expected the root JSON object to be a list of restaurant records.")

    total_restaurants = len(data)
    all_top_level_keys = sorted({key for row in data if isinstance(row, dict) for key in row.keys()})

    top_level_presence = Counter()
    top_level_nulls = Counter()
    top_level_empty_strings = Counter()
    top_level_empty_lists = Counter()
    top_level_empty_dicts = Counter()
    top_level_types = defaultdict(Counter)

    restaurant_rows = []
    numeric_values = defaultdict(list)
    categorical_counts = []
    quality_checks = []

    id_counter = Counter()
    chain_id_counter = Counter()
    brand_id_counter = Counter()
    external_id_counter = Counter()
    chain_name_counter = Counter()
    chain_type_counter = Counter()
    vertical_counter = Counter()
    status_counter = Counter()
    delivery_type_counter = Counter()
    delivery_name_counter = Counter()
    delivery_fee_indicator_counter = Counter()
    delivery_fee_style_counter = Counter()
    delivery_fee_style_v2_counter = Counter()
    kitchen_counter = Counter()
    kitchen_combo_counter = Counter()
    expedition_type_counter = Counter()
    expedition_combo_counter = Counter()
    badge_text_counter = Counter()
    label_type_counter = Counter()
    label_value_counter = Counter()
    status_reason_counter = Counter()
    row_tag_label_counter = Counter()
    row_tag_type_counter = Counter()
    price_range_counter = Counter()
    subscription_supported_counter = Counter()

    rating_bucket_counter = Counter()
    rate_count_bucket_counter = Counter()
    fee_bucket_counter = Counter()

    chain_stats = defaultdict(
        lambda: {
            "restaurant_count": 0,
            "open_count": 0,
            "most_loved_count": 0,
            "rated_restaurant_count": 0,
            "rating_sum": 0.0,
            "rate_count_sum": 0,
            "minimum_order_sum": 0.0,
            "delivery_fee_sum": 0.0,
            "menu_item_count_sum": 0,
            "product_count_sum": 0,
        }
    )

    promotion_name_counter = Counter()
    promotion_type_counter = Counter()
    promotion_category_counter = Counter()
    incentives_type_counter = Counter()
    incentives_name_counter = Counter()
    promotion_count_per_restaurant = []
    incentives_count_per_restaurant = []

    product_name_counter = Counter()
    product_source_counter = Counter()
    product_badge_text_counter = Counter()
    product_promotion_name_counter = Counter()
    product_tag_label_counter = Counter()
    product_tag_type_counter = Counter()
    product_id_counter = Counter()
    product_sku_counter = Counter()
    product_price_values = []
    product_discounted_price_values = []
    product_discount_pct_values = []
    product_count_per_restaurant = []
    product_restaurants = 0
    total_products = 0
    products_with_promotion = 0
    products_with_badge = 0
    products_with_tags = 0
    products_missing_image = 0
    products_missing_name = 0
    products_missing_product_id = 0

    section_name_counter = Counter()
    section_layout_counter = Counter()
    section_type_counter = Counter()
    item_name_counter = Counter()
    item_type_counter = Counter()
    item_tag_counter = Counter()
    item_id_counter = Counter()
    menu_section_count_per_restaurant = []
    menu_item_count_per_restaurant = []
    menu_items_per_section = []
    menu_item_price_values = []
    menu_item_discounted_price_values = []
    menu_item_list_price_values = []
    menu_item_discount_pct_values = []
    menu_item_calories_values = []
    menu_restaurants = 0
    total_sections = 0
    total_menu_items = 0
    menu_items_with_quick_add = 0
    menu_items_with_description = 0
    menu_items_with_image = 0
    menu_items_with_allergens = 0
    menu_items_with_dietary_info = 0
    menu_items_with_tags = 0
    menu_items_with_mandatory_choices = 0
    menu_items_with_product_id = 0
    menu_items_with_popularity = 0

    vendor_status_counter = Counter()
    vendor_reason_counter = Counter()
    menu_available_counter = Counter()
    menu_delivery_available_counter = Counter()
    menu_pickup_available_counter = Counter()

    exact_coordinate_counter = Counter()
    rounded_coordinate_counter = Counter()
    latitude_values = []
    longitude_values = []

    mismatched_promotion_incentive_count = 0
    missing_primary_promotion_count = 0
    primary_promotion_not_in_promotions_count = 0
    delivery_fee_gt_original_count = 0
    time_min_gt_max_count = 0
    price_range_invalid_count = 0
    rating_without_reviews_count = 0
    reviews_without_rating_count = 0
    product_discount_gt_price_count = 0
    product_discount_pct_without_promo_count = 0
    menu_item_discount_gt_list_count = 0
    menu_item_discount_pct_without_discount_count = 0
    menu_item_price_gt_list_count = 0
    scheduled_support_mismatch_count = 0
    pickup_support_mismatch_count = 0
    status_open_but_unavailable_count = 0

    file_stats = input_path.stat()

    for row in data:
        if not isinstance(row, dict):
            continue

        for key in all_top_level_keys:
            if key not in row:
                continue
            value = row[key]
            top_level_presence[key] += 1
            top_level_types[key][type(value).__name__] += 1
            if value is None:
                top_level_nulls[key] += 1
            elif value == "":
                top_level_empty_strings[key] += 1
            elif isinstance(value, list) and not value:
                top_level_empty_lists[key] += 1
            elif isinstance(value, dict) and not value:
                top_level_empty_dicts[key] += 1

        restaurant_id = row.get("id")
        brand_id = row.get("brand_id")
        chain_id = row.get("chain_id")
        chain_name = row.get("chain_name")
        chain_type = row.get("chain_type")
        vertical = row.get("vertical")
        status = row.get("status")
        average_rating = parse_number(row.get("average_rating"))
        rate_count = int(parse_number(row.get("rate_count")) or 0)
        minimum_order = parse_number(row.get("minimum_order"))
        filtered_count = parse_number(row.get("filtered_count"))

        delivery = row.get("delivery") if isinstance(row.get("delivery"), dict) else {}
        distance = row.get("distance") if isinstance(row.get("distance"), dict) else {}
        time_estimation = row.get("time_estimation") if isinstance(row.get("time_estimation"), dict) else {}
        location = row.get("location") if isinstance(row.get("location"), dict) else {}
        price_range = row.get("price_range") if isinstance(row.get("price_range"), dict) else {}
        subscription = row.get("subscription") if isinstance(row.get("subscription"), dict) else {}
        badge = row.get("badge") if isinstance(row.get("badge"), dict) else {}
        label = row.get("label") if isinstance(row.get("label"), dict) else {}
        status_indicator = row.get("status_indicator") if isinstance(row.get("status_indicator"), dict) else {}
        meta = row.get("meta") if isinstance(row.get("meta"), dict) else {}
        midas = meta.get("midas") if isinstance(meta.get("midas"), dict) else {}

        delivery_fee = parse_number(delivery.get("fee"))
        delivery_original_fee = parse_number(delivery.get("original_fee"))
        distance_value = parse_number(distance.get("value"))
        time_value = time_estimation.get("value")
        time_min = parse_number(time_estimation.get("min"))
        time_max = parse_number(time_estimation.get("max"))
        time_window = (time_max - time_min) if time_min is not None and time_max is not None else None
        latitude = parse_number(location.get("latitude"))
        longitude = parse_number(location.get("longitude"))
        price_range_rank = parse_number(price_range.get("rank"))
        price_range_total = parse_number(price_range.get("total"))
        subscription_supported = subscription.get("supported")
        badge_text = badge.get("text")
        label_type = label.get("type")
        label_value = label.get("value")
        status_reason = status_indicator.get("reason")
        status_message = status_indicator.get("message")
        status_message_header = status_message.get("header") if isinstance(status_message, dict) else None
        status_message_body = status_message.get("body") if isinstance(status_message, dict) else None
        premium_type = midas.get("premium_type")
        tracking_token = midas.get("tracking_token")

        id_counter[restaurant_id] += 1
        chain_id_counter[chain_id] += 1
        brand_id_counter[brand_id] += 1
        if row.get("external_id") is not None:
            external_id_counter[row.get("external_id")] += 1
        chain_name_counter[chain_name] += 1
        chain_type_counter[chain_type] += 1
        vertical_counter[vertical] += 1
        status_counter[status] += 1
        delivery_type_counter[delivery.get("type")] += 1
        delivery_name_counter[delivery.get("name")] += 1
        delivery_fee_indicator_counter[delivery.get("fee_indicator")] += 1
        delivery_fee_style_counter[delivery.get("fee_style")] += 1
        delivery_fee_style_v2_counter[delivery.get("fee_style_v2")] += 1
        if badge_text:
            badge_text_counter[badge_text] += 1
        if label_type:
            label_type_counter[label_type] += 1
        if label_value:
            label_value_counter[label_value] += 1
        if status_reason:
            status_reason_counter[status_reason] += 1
        subscription_supported_counter[str(subscription_supported)] += 1
        if price_range_rank is not None and price_range_total is not None:
            price_range_counter[f"{int(price_range_rank)}/{int(price_range_total)}"] += 1

        kitchens = row.get("kitchens") if isinstance(row.get("kitchens"), list) else []
        expedition_types = row.get("available_expedition_types") if isinstance(row.get("available_expedition_types"), list) else []
        row_tags = row.get("tags") if isinstance(row.get("tags"), list) else []

        for kitchen in kitchens:
            kitchen_counter[kitchen] += 1
        kitchen_combo_counter[tuple_label(tuple(sorted(set(kitchens))))] += 1

        for expedition_type in expedition_types:
            expedition_type_counter[expedition_type] += 1
        expedition_combo_counter[tuple_label(tuple(sorted(set(expedition_types))))] += 1

        for tag in row_tags:
            if isinstance(tag, dict):
                if tag.get("label"):
                    row_tag_label_counter[tag.get("label")] += 1
                if tag.get("type"):
                    row_tag_type_counter[tag.get("type")] += 1

        if rate_count == 0 or average_rating in (None, 0.0):
            rating_bucket_counter["Unrated / zero reviews"] += 1
        elif average_rating < 3:
            rating_bucket_counter["< 3.0"] += 1
        elif average_rating < 4:
            rating_bucket_counter["3.0 - 3.99"] += 1
        elif average_rating < 4.5:
            rating_bucket_counter["4.0 - 4.49"] += 1
        else:
            rating_bucket_counter["4.5 - 5.0"] += 1

        if rate_count == 0:
            rate_count_bucket_counter["0"] += 1
        elif rate_count < 10:
            rate_count_bucket_counter["1 - 9"] += 1
        elif rate_count < 50:
            rate_count_bucket_counter["10 - 49"] += 1
        elif rate_count < 200:
            rate_count_bucket_counter["50 - 199"] += 1
        elif rate_count < 1000:
            rate_count_bucket_counter["200 - 999"] += 1
        else:
            rate_count_bucket_counter["1000+"] += 1

        if delivery_fee is None:
            fee_bucket_counter["Missing"] += 1
        elif delivery_fee == 0:
            fee_bucket_counter["0"] += 1
        elif delivery_fee <= 5:
            fee_bucket_counter["0.01 - 5"] += 1
        elif delivery_fee <= 10:
            fee_bucket_counter["5.01 - 10"] += 1
        else:
            fee_bucket_counter["> 10"] += 1

        chain_record = chain_stats[chain_name]
        chain_record["restaurant_count"] += 1
        if status == "OPEN":
            chain_record["open_count"] += 1
        if row.get("is_most_loved"):
            chain_record["most_loved_count"] += 1
        if average_rating not in (None, 0.0) and rate_count > 0:
            chain_record["rated_restaurant_count"] += 1
            chain_record["rating_sum"] += average_rating
        chain_record["rate_count_sum"] += rate_count
        if minimum_order is not None:
            chain_record["minimum_order_sum"] += minimum_order
        if delivery_fee is not None:
            chain_record["delivery_fee_sum"] += delivery_fee

        promotions = row.get("promotions") if isinstance(row.get("promotions"), list) else []
        incentives = row.get("incentives") if isinstance(row.get("incentives"), list) else []
        primary_promotion = row.get("promotion")

        promotion_count_per_restaurant.append(len(promotions))
        incentives_count_per_restaurant.append(len(incentives))

        if len(promotions) != len(incentives):
            mismatched_promotion_incentive_count += 1
        if primary_promotion is None and promotions:
            missing_primary_promotion_count += 1
        if primary_promotion is not None:
            if canonical_promotion(primary_promotion) not in {canonical_promotion(p) for p in promotions if isinstance(p, dict)}:
                primary_promotion_not_in_promotions_count += 1

        for promotion in promotions:
            if isinstance(promotion, dict):
                if promotion.get("name"):
                    promotion_name_counter[promotion.get("name")] += 1
                if promotion.get("type"):
                    promotion_type_counter[promotion.get("type")] += 1
                if promotion.get("category"):
                    promotion_category_counter[promotion.get("category")] += 1
        for incentive in incentives:
            if isinstance(incentive, dict):
                if incentive.get("type"):
                    incentives_type_counter[incentive.get("type")] += 1
                if incentive.get("name"):
                    incentives_name_counter[incentive.get("name")] += 1

        products = row.get("products") if isinstance(row.get("products"), list) else []
        if products:
            product_restaurants += 1
        product_count_per_restaurant.append(len(products))

        for product in products:
            if not isinstance(product, dict):
                continue
            total_products += 1
            if product.get("id") is not None:
                product_id_counter[product.get("id")] += 1
            if product.get("sku_id") is not None:
                product_sku_counter[product.get("sku_id")] += 1
            if product.get("name"):
                product_name_counter[product.get("name")] += 1
            if product.get("source"):
                product_source_counter[product.get("source")] += 1
            if not product.get("image_url"):
                products_missing_image += 1
            if not product.get("name"):
                products_missing_name += 1
            if product.get("product_id") is None:
                products_missing_product_id += 1

            product_price = parse_number(product.get("price"))
            if product_price is not None:
                product_price_values.append(product_price)

            badge_payload = product.get("badge") if isinstance(product.get("badge"), dict) else {}
            if badge_payload:
                products_with_badge += 1
                if badge_payload.get("text"):
                    product_badge_text_counter[badge_payload.get("text")] += 1

            promotion_payload = product.get("promotion") if isinstance(product.get("promotion"), dict) else {}
            if promotion_payload:
                products_with_promotion += 1
                if promotion_payload.get("name"):
                    product_promotion_name_counter[promotion_payload.get("name")] += 1
                discounted_price = parse_number(promotion_payload.get("discounted_price"))
                discounted_percentage = parse_number(promotion_payload.get("discounted_percentage"))
                if discounted_price is not None:
                    product_discounted_price_values.append(discounted_price)
                if discounted_percentage is not None:
                    product_discount_pct_values.append(discounted_percentage)
                    if discounted_percentage > 0 and discounted_price is None:
                        product_discount_pct_without_promo_count += 1
                if discounted_price is not None and product_price is not None and discounted_price > product_price:
                    product_discount_gt_price_count += 1

            product_tags = product.get("tags") if isinstance(product.get("tags"), list) else []
            if product_tags:
                products_with_tags += 1
            for product_tag in product_tags:
                if isinstance(product_tag, dict):
                    if product_tag.get("label"):
                        product_tag_label_counter[product_tag.get("label")] += 1
                    if product_tag.get("type"):
                        product_tag_type_counter[product_tag.get("type")] += 1

        restaurant_menu = row.get("restaurant_menu") if isinstance(row.get("restaurant_menu"), dict) else {}
        has_menu = bool(restaurant_menu)
        if has_menu:
            menu_restaurants += 1

        vendor_coverage = restaurant_menu.get("vendor_coverage") if isinstance(restaurant_menu.get("vendor_coverage"), dict) else {}
        availability = restaurant_menu.get("availability") if isinstance(restaurant_menu.get("availability"), dict) else {}
        availability_delivery = availability.get("delivery") if isinstance(availability.get("delivery"), dict) else {}
        availability_pickup = availability.get("pickup") if isinstance(availability.get("pickup"), dict) else {}
        sections = restaurant_menu.get("sections") if isinstance(restaurant_menu.get("sections"), list) else []

        menu_section_count = len(sections)
        menu_item_count = 0
        menu_section_count_per_restaurant.append(menu_section_count)

        if availability:
            menu_available_counter[str(availability.get("available"))] += 1
        if availability_delivery:
            menu_delivery_available_counter[str(availability_delivery.get("available"))] += 1
        if availability_pickup:
            menu_pickup_available_counter[str(availability_pickup.get("available"))] += 1
        if vendor_coverage.get("status"):
            vendor_status_counter[vendor_coverage.get("status")] += 1
        if vendor_coverage.get("reason"):
            vendor_reason_counter[vendor_coverage.get("reason")] += 1

        for section in sections:
            if not isinstance(section, dict):
                continue
            total_sections += 1
            if section.get("name"):
                section_name_counter[section.get("name")] += 1
            if section.get("layout"):
                section_layout_counter[section.get("layout")] += 1
            if section.get("type") is not None:
                section_type_counter[section.get("type") or "(empty)"] += 1

            items = section.get("items") if isinstance(section.get("items"), list) else []
            menu_items_per_section.append(len(items))
            menu_item_count += len(items)

            for item in items:
                if not isinstance(item, dict):
                    continue
                total_menu_items += 1
                if item.get("id") is not None:
                    item_id_counter[item.get("id")] += 1
                if item.get("name"):
                    item_name_counter[item.get("name")] += 1
                if item.get("type"):
                    item_type_counter[item.get("type")] += 1

                price = parse_number(item.get("price"))
                discounted_price = parse_number(item.get("discounted_price"))
                list_price = parse_number(item.get("list_price"))
                discount_pct = parse_number(item.get("discount_percentage"))
                calories = parse_number(item.get("calories"))

                if price is not None:
                    menu_item_price_values.append(price)
                if discounted_price is not None:
                    menu_item_discounted_price_values.append(discounted_price)
                if list_price is not None:
                    menu_item_list_price_values.append(list_price)
                if discount_pct is not None:
                    menu_item_discount_pct_values.append(discount_pct)
                if calories is not None:
                    menu_item_calories_values.append(calories)

                if item.get("quick_add_available"):
                    menu_items_with_quick_add += 1
                if item.get("description"):
                    menu_items_with_description += 1
                if item.get("image"):
                    menu_items_with_image += 1
                if item.get("allergens"):
                    menu_items_with_allergens += 1
                if item.get("dietary_info"):
                    menu_items_with_dietary_info += 1
                if item.get("mandatory_choices"):
                    menu_items_with_mandatory_choices += 1
                if item.get("product_id") is not None:
                    menu_items_with_product_id += 1
                if item.get("popularity") is not None:
                    menu_items_with_popularity += 1

                item_tags = item.get("tags") if isinstance(item.get("tags"), list) else []
                if item_tags:
                    menu_items_with_tags += 1
                for item_tag in item_tags:
                    if isinstance(item_tag, dict):
                        label = item_tag.get("label") or item_tag.get("type") or str(item_tag)
                        item_tag_counter[label] += 1
                    else:
                        item_tag_counter[str(item_tag)] += 1

                if discount_pct is not None and discount_pct > 0 and discounted_price is not None and list_price is not None and discounted_price > list_price:
                    menu_item_discount_gt_list_count += 1
                if discount_pct is not None and discount_pct > 0 and (discounted_price is None or discounted_price == list_price):
                    menu_item_discount_pct_without_discount_count += 1
                if price is not None and list_price is not None and price > list_price:
                    menu_item_price_gt_list_count += 1

        menu_item_count_per_restaurant.append(menu_item_count)
        chain_record["menu_item_count_sum"] += menu_item_count
        chain_record["product_count_sum"] += len(products)

        vendor_delivering = vendor_coverage.get("delivering")
        vendor_status = vendor_coverage.get("status")
        vendor_reason = vendor_coverage.get("reason")
        vendor_immediate_supported = vendor_coverage.get("immediate_order_supported")
        vendor_scheduled_supported = vendor_coverage.get("scheduled_order_supported")
        menu_available = availability.get("available") if availability else None
        menu_delivery_available = availability_delivery.get("available") if availability_delivery else None
        menu_pickup_available = availability_pickup.get("available") if availability_pickup else None

        if delivery_fee is not None and delivery_original_fee is not None and delivery_fee > delivery_original_fee:
            delivery_fee_gt_original_count += 1
        if time_min is not None and time_max is not None and time_min > time_max:
            time_min_gt_max_count += 1
        if price_range_rank is not None and price_range_total is not None and (price_range_rank <= 0 or price_range_total <= 0 or price_range_rank > price_range_total):
            price_range_invalid_count += 1
        if average_rating not in (None, 0.0) and rate_count == 0:
            rating_without_reviews_count += 1
        if average_rating in (None, 0.0) and rate_count > 0:
            reviews_without_rating_count += 1
        if bool(row.get("supports_scheduled_order")) != bool(vendor_scheduled_supported) and vendor_scheduled_supported is not None:
            scheduled_support_mismatch_count += 1
        if bool(row.get("supports_pickup")) != bool(menu_pickup_available) and menu_pickup_available is not None:
            pickup_support_mismatch_count += 1
        if status == "OPEN" and menu_available is False:
            status_open_but_unavailable_count += 1

        exact_coordinate = f"{latitude:.6f},{longitude:.6f}" if latitude is not None and longitude is not None else None
        rounded_coordinate = f"{latitude:.3f},{longitude:.3f}" if latitude is not None and longitude is not None else None
        if exact_coordinate:
            exact_coordinate_counter[exact_coordinate] += 1
        if rounded_coordinate:
            rounded_coordinate_counter[rounded_coordinate] += 1
        if latitude is not None:
            latitude_values.append(latitude)
        if longitude is not None:
            longitude_values.append(longitude)

        flattened_row = {
            "id": restaurant_id,
            "brand_id": brand_id,
            "chain_id": chain_id,
            "chain_name": chain_name,
            "chain_type": chain_type,
            "vertical": vertical,
            "status": status,
            "average_rating": average_rating,
            "rate_count": rate_count,
            "minimum_order": minimum_order,
            "filtered_count": filtered_count,
            "delivery_type": delivery.get("type"),
            "delivery_name": delivery.get("name"),
            "delivery_fee": delivery_fee,
            "delivery_original_fee": delivery_original_fee,
            "delivery_fee_indicator": delivery.get("fee_indicator"),
            "delivery_fee_style": delivery.get("fee_style"),
            "delivery_fee_style_v2": delivery.get("fee_style_v2"),
            "delivery_is_default": delivery.get("is_default"),
            "distance_value": distance_value,
            "distance_unit": distance.get("unit"),
            "time_value": time_value,
            "time_min": time_min,
            "time_max": time_max,
            "time_window": time_window,
            "supports_pickup": row.get("supports_pickup"),
            "supports_scheduled_order": row.get("supports_scheduled_order"),
            "subscription_supported": subscription_supported,
            "is_favorable": row.get("is_favorable"),
            "is_favorite": row.get("is_favorite"),
            "is_most_loved": row.get("is_most_loved"),
            "kitchens_count": len(kitchens),
            "available_expedition_types_count": len(expedition_types),
            "promotions_count": len(promotions),
            "incentives_count": len(incentives),
            "products_count": len(products),
            "tags_count": len(row_tags),
            "badge_text": badge_text,
            "label_type": label_type,
            "label_value": label_value,
            "status_indicator_reason": status_reason,
            "status_indicator_header": status_message_header,
            "status_indicator_body": status_message_body,
            "price_range_rank": price_range_rank,
            "price_range_total": price_range_total,
            "external_id": row.get("external_id"),
            "meta_context": meta.get("context"),
            "midas_premium_type": premium_type,
            "midas_tracking_token": tracking_token,
            "has_menu": has_menu,
            "menu_section_count": menu_section_count,
            "menu_item_count": menu_item_count,
            "menu_available": menu_available,
            "menu_delivery_available": menu_delivery_available,
            "menu_pickup_available": menu_pickup_available,
            "vendor_delivering": vendor_delivering,
            "vendor_status": vendor_status,
            "vendor_reason": vendor_reason,
            "vendor_immediate_supported": vendor_immediate_supported,
            "vendor_scheduled_supported": vendor_scheduled_supported,
            "latitude": latitude,
            "longitude": longitude,
            "exact_coordinate": exact_coordinate,
            "rounded_coordinate_3dp": rounded_coordinate,
        }
        restaurant_rows.append(flattened_row)

        numeric_values["average_rating"].append(average_rating)
        numeric_values["rate_count"].append(rate_count)
        numeric_values["minimum_order"].append(minimum_order)
        numeric_values["filtered_count"].append(filtered_count)
        numeric_values["delivery_fee"].append(delivery_fee)
        numeric_values["delivery_original_fee"].append(delivery_original_fee)
        numeric_values["distance_value"].append(distance_value)
        numeric_values["time_min"].append(time_min)
        numeric_values["time_max"].append(time_max)
        numeric_values["time_window"].append(time_window)
        numeric_values["price_range_rank"].append(price_range_rank)
        numeric_values["price_range_total"].append(price_range_total)
        numeric_values["kitchens_count"].append(len(kitchens))
        numeric_values["available_expedition_types_count"].append(len(expedition_types))
        numeric_values["promotions_count"].append(len(promotions))
        numeric_values["incentives_count"].append(len(incentives))
        numeric_values["products_count"].append(len(products))
        numeric_values["tags_count"].append(len(row_tags))
        numeric_values["menu_section_count"].append(menu_section_count)
        numeric_values["menu_item_count"].append(menu_item_count)
        numeric_values["latitude"].append(latitude)
        numeric_values["longitude"].append(longitude)

    top_level_completeness_rows = []
    for key in all_top_level_keys:
        present = top_level_presence[key]
        nulls = top_level_nulls[key]
        empty_strings = top_level_empty_strings[key]
        empty_lists = top_level_empty_lists[key]
        empty_dicts = top_level_empty_dicts[key]
        non_empty = present - nulls - empty_strings - empty_lists - empty_dicts
        top_level_completeness_rows.append(
            {
                "field": key,
                "present_count": present,
                "present_pct": round(pct(present, total_restaurants), 4),
                "null_count": nulls,
                "empty_string_count": empty_strings,
                "empty_list_count": empty_lists,
                "empty_dict_count": empty_dicts,
                "non_empty_count": non_empty,
                "observed_types": json.dumps(dict(top_level_types[key]), ensure_ascii=False, sort_keys=True),
            }
        )

    numeric_summary_rows = []
    for field, values in sorted(numeric_values.items()):
        summary = numeric_summary(values)
        summary["missing"] = total_restaurants - summary["count"]
        summary["field"] = field
        numeric_summary_rows.append(
            {
                "field": field,
                "count": summary["count"],
                "missing": summary["missing"],
                "zeros": summary["zeros"],
                "negatives": summary["negatives"],
                "min": round_or_none(summary["min"], 4),
                "p01": round_or_none(summary["p01"], 4),
                "p05": round_or_none(summary["p05"], 4),
                "p25": round_or_none(summary["p25"], 4),
                "median": round_or_none(summary["median"], 4),
                "p75": round_or_none(summary["p75"], 4),
                "p95": round_or_none(summary["p95"], 4),
                "p99": round_or_none(summary["p99"], 4),
                "max": round_or_none(summary["max"], 4),
                "mean": round_or_none(summary["mean"], 4),
                "stddev": round_or_none(summary["stddev"], 4),
            }
        )

    categorical_counts.extend(counter_to_rows(vertical_counter, "vertical", total_restaurants))
    categorical_counts.extend(counter_to_rows(chain_type_counter, "chain_type", total_restaurants))
    categorical_counts.extend(counter_to_rows(status_counter, "status", total_restaurants))
    categorical_counts.extend(counter_to_rows(delivery_type_counter, "delivery_type", total_restaurants))
    categorical_counts.extend(counter_to_rows(delivery_name_counter, "delivery_name", total_restaurants))
    categorical_counts.extend(counter_to_rows(delivery_fee_indicator_counter, "delivery_fee_indicator", total_restaurants))
    categorical_counts.extend(counter_to_rows(delivery_fee_style_counter, "delivery_fee_style", total_restaurants))
    categorical_counts.extend(counter_to_rows(delivery_fee_style_v2_counter, "delivery_fee_style_v2", total_restaurants))
    categorical_counts.extend(counter_to_rows(kitchen_counter, "kitchen", total_restaurants))
    categorical_counts.extend(counter_to_rows(kitchen_combo_counter, "kitchen_combo", total_restaurants))
    categorical_counts.extend(counter_to_rows(expedition_type_counter, "expedition_type", total_restaurants))
    categorical_counts.extend(counter_to_rows(expedition_combo_counter, "expedition_combo", total_restaurants))
    categorical_counts.extend(counter_to_rows(badge_text_counter, "badge_text", total_restaurants))
    categorical_counts.extend(counter_to_rows(label_type_counter, "label_type", total_restaurants))
    categorical_counts.extend(counter_to_rows(label_value_counter, "label_value", total_restaurants))
    categorical_counts.extend(counter_to_rows(status_reason_counter, "status_indicator_reason", total_restaurants))
    categorical_counts.extend(counter_to_rows(price_range_counter, "price_range_rank_total", total_restaurants))
    categorical_counts.extend(counter_to_rows(subscription_supported_counter, "subscription_supported", total_restaurants))
    categorical_counts.extend(counter_to_rows(row_tag_label_counter, "row_tag_label", total_restaurants))
    categorical_counts.extend(counter_to_rows(row_tag_type_counter, "row_tag_type", total_restaurants))
    categorical_counts.extend(counter_to_rows(rating_bucket_counter, "rating_bucket", total_restaurants))
    categorical_counts.extend(counter_to_rows(rate_count_bucket_counter, "rate_count_bucket", total_restaurants))
    categorical_counts.extend(counter_to_rows(fee_bucket_counter, "delivery_fee_bucket", total_restaurants))
    categorical_counts.extend(counter_to_rows(promotion_name_counter, "promotion_name", total_restaurants))
    categorical_counts.extend(counter_to_rows(promotion_type_counter, "promotion_type", total_restaurants))
    categorical_counts.extend(counter_to_rows(promotion_category_counter, "promotion_category", total_restaurants))
    categorical_counts.extend(counter_to_rows(incentives_type_counter, "incentive_type", total_restaurants))
    categorical_counts.extend(counter_to_rows(incentives_name_counter, "incentive_name", total_restaurants))
    categorical_counts.extend(counter_to_rows(product_source_counter, "product_source", total_products))
    categorical_counts.extend(counter_to_rows(product_badge_text_counter, "product_badge_text", total_products))
    categorical_counts.extend(counter_to_rows(product_promotion_name_counter, "product_promotion_name", total_products))
    categorical_counts.extend(counter_to_rows(product_tag_label_counter, "product_tag_label", total_products))
    categorical_counts.extend(counter_to_rows(product_tag_type_counter, "product_tag_type", total_products))
    categorical_counts.extend(counter_to_rows(section_name_counter, "menu_section_name", total_sections))
    categorical_counts.extend(counter_to_rows(section_layout_counter, "menu_section_layout", total_sections))
    categorical_counts.extend(counter_to_rows(section_type_counter, "menu_section_type", total_sections))
    categorical_counts.extend(counter_to_rows(item_type_counter, "menu_item_type", total_menu_items))
    categorical_counts.extend(counter_to_rows(item_tag_counter, "menu_item_tag", total_menu_items))
    categorical_counts.extend(counter_to_rows(vendor_status_counter, "vendor_status", menu_restaurants))
    categorical_counts.extend(counter_to_rows(vendor_reason_counter, "vendor_reason", menu_restaurants))
    categorical_counts.extend(counter_to_rows(menu_available_counter, "menu_available", menu_restaurants))
    categorical_counts.extend(counter_to_rows(menu_delivery_available_counter, "menu_delivery_available", menu_restaurants))
    categorical_counts.extend(counter_to_rows(menu_pickup_available_counter, "menu_pickup_available", menu_restaurants))

    duplicate_restaurant_ids = sum(count - 1 for count in id_counter.values() if count > 1)
    duplicate_external_ids = sum(count - 1 for count in external_id_counter.values() if count > 1)
    duplicate_product_ids = sum(count - 1 for count in product_id_counter.values() if count > 1)
    duplicate_product_skus = sum(count - 1 for count in product_sku_counter.values() if count > 1)
    duplicate_menu_item_ids = sum(count - 1 for count in item_id_counter.values() if count > 1)
    duplicate_exact_coordinates = sum(count - 1 for count in exact_coordinate_counter.values() if count > 1)

    quality_checks = [
        {"check": "duplicate_restaurant_ids", "count": duplicate_restaurant_ids, "pct_of_base": round(pct(duplicate_restaurant_ids, total_restaurants), 4)},
        {"check": "duplicate_external_ids", "count": duplicate_external_ids, "pct_of_base": round(pct(duplicate_external_ids, total_restaurants), 4)},
        {"check": "delivery_fee_gt_original_fee", "count": delivery_fee_gt_original_count, "pct_of_base": round(pct(delivery_fee_gt_original_count, total_restaurants), 4)},
        {"check": "time_min_gt_time_max", "count": time_min_gt_max_count, "pct_of_base": round(pct(time_min_gt_max_count, total_restaurants), 4)},
        {"check": "invalid_price_range_rank_total", "count": price_range_invalid_count, "pct_of_base": round(pct(price_range_invalid_count, total_restaurants), 4)},
        {"check": "rating_without_reviews", "count": rating_without_reviews_count, "pct_of_base": round(pct(rating_without_reviews_count, total_restaurants), 4)},
        {"check": "reviews_without_rating", "count": reviews_without_rating_count, "pct_of_base": round(pct(reviews_without_rating_count, total_restaurants), 4)},
        {"check": "promotion_count_mismatch_vs_incentives", "count": mismatched_promotion_incentive_count, "pct_of_base": round(pct(mismatched_promotion_incentive_count, total_restaurants), 4)},
        {"check": "missing_primary_promotion_despite_promotions", "count": missing_primary_promotion_count, "pct_of_base": round(pct(missing_primary_promotion_count, total_restaurants), 4)},
        {"check": "primary_promotion_not_found_in_promotions", "count": primary_promotion_not_in_promotions_count, "pct_of_base": round(pct(primary_promotion_not_in_promotions_count, total_restaurants), 4)},
        {"check": "scheduled_support_mismatch_top_vs_menu", "count": scheduled_support_mismatch_count, "pct_of_base": round(pct(scheduled_support_mismatch_count, total_restaurants), 4)},
        {"check": "pickup_support_mismatch_top_vs_menu", "count": pickup_support_mismatch_count, "pct_of_base": round(pct(pickup_support_mismatch_count, total_restaurants), 4)},
        {"check": "status_open_but_menu_unavailable", "count": status_open_but_unavailable_count, "pct_of_base": round(pct(status_open_but_unavailable_count, total_restaurants), 4)},
        {"check": "duplicate_exact_coordinates", "count": duplicate_exact_coordinates, "pct_of_base": round(pct(duplicate_exact_coordinates, total_restaurants), 4)},
        {"check": "duplicate_product_ids", "count": duplicate_product_ids, "pct_of_base": round(pct(duplicate_product_ids, total_products), 4)},
        {"check": "duplicate_product_skus", "count": duplicate_product_skus, "pct_of_base": round(pct(duplicate_product_skus, total_products), 4)},
        {"check": "product_discounted_price_gt_price", "count": product_discount_gt_price_count, "pct_of_base": round(pct(product_discount_gt_price_count, total_products), 4)},
        {"check": "product_discount_pct_without_discounted_price", "count": product_discount_pct_without_promo_count, "pct_of_base": round(pct(product_discount_pct_without_promo_count, total_products), 4)},
        {"check": "duplicate_menu_item_ids", "count": duplicate_menu_item_ids, "pct_of_base": round(pct(duplicate_menu_item_ids, total_menu_items), 4)},
        {"check": "menu_item_discounted_price_gt_list_price", "count": menu_item_discount_gt_list_count, "pct_of_base": round(pct(menu_item_discount_gt_list_count, total_menu_items), 4)},
        {"check": "menu_item_discount_pct_without_actual_discount", "count": menu_item_discount_pct_without_discount_count, "pct_of_base": round(pct(menu_item_discount_pct_without_discount_count, total_menu_items), 4)},
        {"check": "menu_item_price_gt_list_price", "count": menu_item_price_gt_list_count, "pct_of_base": round(pct(menu_item_price_gt_list_count, total_menu_items), 4)},
    ]

    chain_summary_rows = []
    for chain_name, stats in chain_stats.items():
        restaurant_count = stats["restaurant_count"]
        rated_restaurant_count = stats["rated_restaurant_count"]
        chain_summary_rows.append(
            {
                "chain_name": chain_name,
                "restaurant_count": restaurant_count,
                "open_count": stats["open_count"],
                "most_loved_count": stats["most_loved_count"],
                "rated_restaurant_count": rated_restaurant_count,
                "mean_rating_rated_only": round_or_none(stats["rating_sum"] / rated_restaurant_count if rated_restaurant_count else None, 4),
                "total_rate_count": stats["rate_count_sum"],
                "avg_minimum_order": round_or_none(stats["minimum_order_sum"] / restaurant_count if restaurant_count else None, 4),
                "avg_delivery_fee": round_or_none(stats["delivery_fee_sum"] / restaurant_count if restaurant_count else None, 4),
                "avg_menu_item_count": round_or_none(stats["menu_item_count_sum"] / restaurant_count if restaurant_count else None, 4),
                "avg_product_count": round_or_none(stats["product_count_sum"] / restaurant_count if restaurant_count else None, 4),
            }
        )
    chain_summary_rows.sort(key=lambda row: (-row["restaurant_count"], row["chain_name"] or ""))

    top_coordinate_cluster_rows = []
    for coordinate, count in rounded_coordinate_counter.most_common(100):
        top_coordinate_cluster_rows.append(
            {
                "rounded_coordinate_3dp": coordinate,
                "restaurant_count": count,
                "pct_of_restaurants": round(pct(count, total_restaurants), 4),
            }
        )

    top_restaurants_by_menu_items = sorted(restaurant_rows, key=lambda row: (-row["menu_item_count"], row["chain_name"] or ""))[:100]
    top_restaurants_by_products = sorted(restaurant_rows, key=lambda row: (-row["products_count"], row["chain_name"] or ""))[:100]
    top_restaurants_by_rate_count = sorted(restaurant_rows, key=lambda row: (-row["rate_count"], row["chain_name"] or ""))[:100]
    top_menu_section_names = [{"section_name": name, "count": count} for name, count in section_name_counter.most_common(100)]
    top_menu_item_names = [{"item_name": name, "count": count} for name, count in item_name_counter.most_common(100)]
    top_product_names = [{"product_name": name, "count": count} for name, count in product_name_counter.most_common(100)]

    restaurant_fieldnames = list(restaurant_rows[0].keys()) if restaurant_rows else []
    write_csv(tables_dir / "restaurants_flattened.csv", restaurant_rows, restaurant_fieldnames)
    write_csv(tables_dir / "top_level_completeness.csv", top_level_completeness_rows, list(top_level_completeness_rows[0].keys()))
    write_csv(tables_dir / "numeric_summary.csv", numeric_summary_rows, list(numeric_summary_rows[0].keys()))
    write_csv(tables_dir / "categorical_counts.csv", categorical_counts, ["dimension", "value", "count", "pct_of_total"])
    write_csv(tables_dir / "data_quality_checks.csv", quality_checks, ["check", "count", "pct_of_base"])
    write_csv(tables_dir / "chain_summary.csv", chain_summary_rows, list(chain_summary_rows[0].keys()))
    write_csv(tables_dir / "top_coordinate_clusters.csv", top_coordinate_cluster_rows, list(top_coordinate_cluster_rows[0].keys()))
    write_csv(tables_dir / "top_restaurants_by_menu_items.csv", top_restaurants_by_menu_items, restaurant_fieldnames)
    write_csv(tables_dir / "top_restaurants_by_products.csv", top_restaurants_by_products, restaurant_fieldnames)
    write_csv(tables_dir / "top_restaurants_by_rate_count.csv", top_restaurants_by_rate_count, restaurant_fieldnames)
    write_csv(tables_dir / "top_menu_section_names.csv", top_menu_section_names, ["section_name", "count"])
    write_csv(tables_dir / "top_menu_item_names.csv", top_menu_item_names, ["item_name", "count"])
    write_csv(tables_dir / "top_product_names.csv", top_product_names, ["product_name", "count"])

    rated_restaurants = [row for row in restaurant_rows if row["average_rating"] not in (None, 0.0) and row["rate_count"] > 0]
    mean_rating_rated_only = round_or_none(
        statistics.fmean(row["average_rating"] for row in rated_restaurants) if rated_restaurants else None, 4
    )
    weighted_rating = round_or_none(
        (
            sum(row["average_rating"] * row["rate_count"] for row in rated_restaurants)
            / sum(row["rate_count"] for row in rated_restaurants)
        )
        if rated_restaurants and sum(row["rate_count"] for row in rated_restaurants)
        else None,
        4,
    )

    summary_payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_path": str(input_path),
        "file_size_bytes": file_stats.st_size,
        "restaurant_count": total_restaurants,
        "restaurant_with_menu_count": menu_restaurants,
        "restaurant_with_products_count": product_restaurants,
        "menu_section_count": total_sections,
        "menu_item_count": total_menu_items,
        "product_count": total_products,
        "unique_chain_names": len(chain_name_counter),
        "unique_chain_ids": len(chain_id_counter),
        "unique_brand_ids": len(brand_id_counter),
        "unique_exact_coordinates": len(exact_coordinate_counter),
        "duplicate_restaurant_ids": duplicate_restaurant_ids,
        "mean_rating_rated_only": mean_rating_rated_only,
        "weighted_rating_by_review_count": weighted_rating,
        "top_outputs": {
            "summary_report": str(reports_dir / "summary_report.md"),
            "restaurants_flattened": str(tables_dir / "restaurants_flattened.csv"),
            "numeric_summary": str(tables_dir / "numeric_summary.csv"),
            "categorical_counts": str(tables_dir / "categorical_counts.csv"),
            "chain_summary": str(tables_dir / "chain_summary.csv"),
            "quality_checks": str(tables_dir / "data_quality_checks.csv"),
        },
    }
    with (metadata_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary_payload, handle, ensure_ascii=False, indent=2)

    overview_rows = [
        {"metric": "Total records", "value": total_restaurants},
        {"metric": "Unique chain names", "value": len(chain_name_counter)},
        {"metric": "Unique chain IDs", "value": len(chain_id_counter)},
        {"metric": "Unique brand IDs", "value": len(brand_id_counter)},
        {"metric": "Records with menus", "value": f"{menu_restaurants} ({pct(menu_restaurants, total_restaurants):.2f}%)"},
        {"metric": "Records with products", "value": f"{product_restaurants} ({pct(product_restaurants, total_restaurants):.2f}%)"},
        {"metric": "Menu sections", "value": total_sections},
        {"metric": "Menu items", "value": total_menu_items},
        {"metric": "Products", "value": total_products},
        {"metric": "Mean rating (rated only)", "value": mean_rating_rated_only},
        {"metric": "Weighted rating (by rate count)", "value": weighted_rating},
    ]

    top_chain_rows = [
        {
            "chain_name": row["chain_name"],
            "restaurant_count": row["restaurant_count"],
            "mean_rating_rated_only": row["mean_rating_rated_only"],
            "total_rate_count": row["total_rate_count"],
        }
        for row in chain_summary_rows[:20]
    ]

    top_reviewed_chain_rows = [
        {
            "chain_name": row["chain_name"],
            "restaurant_count": row["restaurant_count"],
            "mean_rating_rated_only": row["mean_rating_rated_only"],
            "total_rate_count": row["total_rate_count"],
        }
        for row in sorted(chain_summary_rows, key=lambda row: (-row["total_rate_count"], row["chain_name"] or ""))[:20]
    ]

    top_rated_chains_rows = [
        {
            "chain_name": row["chain_name"],
            "restaurant_count": row["restaurant_count"],
            "mean_rating_rated_only": row["mean_rating_rated_only"],
            "total_rate_count": row["total_rate_count"],
        }
        for row in sorted(
            [row for row in chain_summary_rows if row["restaurant_count"] >= 5 and row["mean_rating_rated_only"] is not None],
            key=lambda row: (-row["mean_rating_rated_only"], -row["restaurant_count"], row["chain_name"] or ""),
        )[:20]
    ]

    report_lines = [
        "# Hungerstation Restaurants EDA",
        "",
        f"- Generated at (UTC): {summary_payload['generated_at_utc']}",
        f"- Source file: `{input_path}`",
        f"- File size: {file_stats.st_size:,} bytes",
        "",
        "## Overview",
        "",
        markdown_table(overview_rows, ["metric", "value"]),
        "",
        "## Top-Level Schema Completeness",
        "",
        markdown_table(top_level_completeness_rows, ["field", "present_count", "null_count", "empty_list_count", "non_empty_count", "observed_types"]),
        "",
        "## Restaurant-Level Numeric Summary",
        "",
        markdown_table(numeric_summary_rows, ["field", "count", "missing", "min", "p25", "median", "p75", "p95", "max", "mean", "stddev"]),
        "",
        "## Core Categorical Distributions",
        "",
        "### Vertical",
        "",
        markdown_table(counter_to_rows(vertical_counter, "vertical", total_restaurants), ["value", "count", "pct_of_total"]),
        "",
        "### Chain Type",
        "",
        markdown_table(counter_to_rows(chain_type_counter, "chain_type", total_restaurants), ["value", "count", "pct_of_total"]),
        "",
        "### Status",
        "",
        markdown_table(counter_to_rows(status_counter, "status", total_restaurants), ["value", "count", "pct_of_total"]),
        "",
        "### Delivery Type",
        "",
        markdown_table(counter_to_rows(delivery_type_counter, "delivery_type", total_restaurants), ["value", "count", "pct_of_total"]),
        "",
        "### Delivery Fee Buckets",
        "",
        markdown_table(counter_to_rows(fee_bucket_counter, "delivery_fee_bucket", total_restaurants), ["value", "count", "pct_of_total"]),
        "",
        "### Rating Buckets",
        "",
        markdown_table(counter_to_rows(rating_bucket_counter, "rating_bucket", total_restaurants), ["value", "count", "pct_of_total"]),
        "",
        "### Top Kitchens",
        "",
        markdown_table(counter_to_rows(kitchen_counter, "kitchen", total_restaurants, limit=20), ["value", "count", "pct_of_total"]),
        "",
        "### Expedition Type Combinations",
        "",
        markdown_table(counter_to_rows(expedition_combo_counter, "expedition_combo", total_restaurants, limit=20), ["value", "count", "pct_of_total"]),
        "",
        "## Promotions And Incentives",
        "",
        markdown_table(
            [
                {"metric": "Restaurants with promotions", "value": sum(1 for value in promotion_count_per_restaurant if value > 0)},
                {"metric": "Total promotion records", "value": sum(promotion_count_per_restaurant)},
                {"metric": "Restaurants with incentives", "value": sum(1 for value in incentives_count_per_restaurant if value > 0)},
                {"metric": "Total incentive records", "value": sum(incentives_count_per_restaurant)},
                {"metric": "Top-level primary promotion missing despite promotions list", "value": missing_primary_promotion_count},
                {"metric": "Primary promotion not found inside promotions list", "value": primary_promotion_not_in_promotions_count},
            ],
            ["metric", "value"],
        ),
        "",
        "### Top Promotion Names",
        "",
        markdown_table(counter_to_rows(promotion_name_counter, "promotion_name", total_restaurants, limit=20), ["value", "count", "pct_of_total"]),
        "",
        "### Top Promotion Types",
        "",
        markdown_table(counter_to_rows(promotion_type_counter, "promotion_type", total_restaurants, limit=20), ["value", "count", "pct_of_total"]),
        "",
        "## Products",
        "",
        markdown_table(
            [
                {"metric": "Restaurants with products", "value": f"{product_restaurants} ({pct(product_restaurants, total_restaurants):.2f}%)"},
                {"metric": "Total products", "value": total_products},
                {"metric": "Products with promotions", "value": f"{products_with_promotion} ({pct(products_with_promotion, total_products):.2f}%)"},
                {"metric": "Products with badges", "value": f"{products_with_badge} ({pct(products_with_badge, total_products):.2f}%)"},
                {"metric": "Products with tags", "value": f"{products_with_tags} ({pct(products_with_tags, total_products):.2f}%)"},
                {"metric": "Products missing image", "value": f"{products_missing_image} ({pct(products_missing_image, total_products):.2f}%)"},
                {"metric": "Products missing name", "value": f"{products_missing_name} ({pct(products_missing_name, total_products):.2f}%)"},
                {"metric": "Products missing product_id", "value": f"{products_missing_product_id} ({pct(products_missing_product_id, total_products):.2f}%)"},
            ],
            ["metric", "value"],
        ),
        "",
        markdown_table(
            [
                {
                    "field": "product_price",
                    **{k: round_or_none(v, 4) if isinstance(v, float) else v for k, v in numeric_summary(product_price_values).items()},
                },
                {
                    "field": "product_discounted_price",
                    **{k: round_or_none(v, 4) if isinstance(v, float) else v for k, v in numeric_summary(product_discounted_price_values).items()},
                },
                {
                    "field": "product_discount_pct",
                    **{k: round_or_none(v, 4) if isinstance(v, float) else v for k, v in numeric_summary(product_discount_pct_values).items()},
                },
            ],
            ["field", "count", "zeros", "min", "p25", "median", "p75", "p95", "max", "mean", "stddev"],
        ),
        "",
        "### Top Product Sources",
        "",
        markdown_table(counter_to_rows(product_source_counter, "product_source", total_products), ["value", "count", "pct_of_total"]),
        "",
        "### Top Product Names",
        "",
        markdown_table([{"product_name": row["product_name"], "count": row["count"]} for row in top_product_names[:20]], ["product_name", "count"]),
        "",
        "## Restaurant Menus",
        "",
        markdown_table(
            [
                {"metric": "Restaurants with menus", "value": f"{menu_restaurants} ({pct(menu_restaurants, total_restaurants):.2f}%)"},
                {"metric": "Total menu sections", "value": total_sections},
                {"metric": "Total menu items", "value": total_menu_items},
                {"metric": "Menu items with quick add", "value": f"{menu_items_with_quick_add} ({pct(menu_items_with_quick_add, total_menu_items):.2f}%)"},
                {"metric": "Menu items with descriptions", "value": f"{menu_items_with_description} ({pct(menu_items_with_description, total_menu_items):.2f}%)"},
                {"metric": "Menu items with images", "value": f"{menu_items_with_image} ({pct(menu_items_with_image, total_menu_items):.2f}%)"},
                {"metric": "Menu items with allergens", "value": f"{menu_items_with_allergens} ({pct(menu_items_with_allergens, total_menu_items):.2f}%)"},
                {"metric": "Menu items with dietary_info", "value": f"{menu_items_with_dietary_info} ({pct(menu_items_with_dietary_info, total_menu_items):.2f}%)"},
                {"metric": "Menu items with tags", "value": f"{menu_items_with_tags} ({pct(menu_items_with_tags, total_menu_items):.2f}%)"},
                {"metric": "Menu items with mandatory choices", "value": f"{menu_items_with_mandatory_choices} ({pct(menu_items_with_mandatory_choices, total_menu_items):.2f}%)"},
            ],
            ["metric", "value"],
        ),
        "",
        markdown_table(
            [
                {
                    "field": "menu_section_count_per_restaurant",
                    **{k: round_or_none(v, 4) if isinstance(v, float) else v for k, v in numeric_summary(menu_section_count_per_restaurant).items()},
                },
                {
                    "field": "menu_item_count_per_restaurant",
                    **{k: round_or_none(v, 4) if isinstance(v, float) else v for k, v in numeric_summary(menu_item_count_per_restaurant).items()},
                },
                {
                    "field": "menu_items_per_section",
                    **{k: round_or_none(v, 4) if isinstance(v, float) else v for k, v in numeric_summary(menu_items_per_section).items()},
                },
                {
                    "field": "menu_item_price",
                    **{k: round_or_none(v, 4) if isinstance(v, float) else v for k, v in numeric_summary(menu_item_price_values).items()},
                },
                {
                    "field": "menu_item_discounted_price",
                    **{k: round_or_none(v, 4) if isinstance(v, float) else v for k, v in numeric_summary(menu_item_discounted_price_values).items()},
                },
                {
                    "field": "menu_item_list_price",
                    **{k: round_or_none(v, 4) if isinstance(v, float) else v for k, v in numeric_summary(menu_item_list_price_values).items()},
                },
                {
                    "field": "menu_item_discount_pct",
                    **{k: round_or_none(v, 4) if isinstance(v, float) else v for k, v in numeric_summary(menu_item_discount_pct_values).items()},
                },
                {
                    "field": "menu_item_calories",
                    **{k: round_or_none(v, 4) if isinstance(v, float) else v for k, v in numeric_summary(menu_item_calories_values).items()},
                },
            ],
            ["field", "count", "zeros", "min", "p25", "median", "p75", "p95", "max", "mean", "stddev"],
        ),
        "",
        "### Top Section Names",
        "",
        markdown_table(top_menu_section_names[:20], ["section_name", "count"]),
        "",
        "### Top Menu Item Names",
        "",
        markdown_table(top_menu_item_names[:20], ["item_name", "count"]),
        "",
        "### Menu Item Types",
        "",
        markdown_table(counter_to_rows(item_type_counter, "menu_item_type", total_menu_items), ["value", "count", "pct_of_total"]),
        "",
        "## Geography",
        "",
        markdown_table(
            [
                {"metric": "Latitude min", "value": round_or_none(min(latitude_values) if latitude_values else None, 6)},
                {"metric": "Latitude max", "value": round_or_none(max(latitude_values) if latitude_values else None, 6)},
                {"metric": "Longitude min", "value": round_or_none(min(longitude_values) if longitude_values else None, 6)},
                {"metric": "Longitude max", "value": round_or_none(max(longitude_values) if longitude_values else None, 6)},
                {"metric": "Unique exact coordinates", "value": len(exact_coordinate_counter)},
                {"metric": "Duplicate exact-coordinate rows", "value": duplicate_exact_coordinates},
            ],
            ["metric", "value"],
        ),
        "",
        "### Top Rounded Coordinate Clusters (3 dp)",
        "",
        markdown_table(top_coordinate_cluster_rows[:20], ["rounded_coordinate_3dp", "restaurant_count", "pct_of_restaurants"]),
        "",
        "## Chain Highlights",
        "",
        "### Top Chains By Location Count",
        "",
        markdown_table(top_chain_rows, ["chain_name", "restaurant_count", "mean_rating_rated_only", "total_rate_count"]),
        "",
        "### Most Reviewed Chains",
        "",
        markdown_table(top_reviewed_chain_rows, ["chain_name", "restaurant_count", "mean_rating_rated_only", "total_rate_count"]),
        "",
        "### Highest Rated Chains With At Least 5 Locations",
        "",
        markdown_table(top_rated_chains_rows, ["chain_name", "restaurant_count", "mean_rating_rated_only", "total_rate_count"]),
        "",
        "## Data Quality Checks",
        "",
        markdown_table(quality_checks, ["check", "count", "pct_of_base"]),
        "",
        "## Output Files",
        "",
        markdown_table(
            [
                {"file": str(reports_dir / "summary_report.md"), "description": "Compact autogenerated EDA summary report."},
                {"file": str(metadata_dir / "summary.json"), "description": "Compact machine-readable summary."},
                {"file": str(tables_dir / "restaurants_flattened.csv"), "description": "One row per restaurant with flattened restaurant and menu metadata."},
                {"file": str(tables_dir / "top_level_completeness.csv"), "description": "Presence, null, and empty counts for every top-level field."},
                {"file": str(tables_dir / "numeric_summary.csv"), "description": "Distribution summary for derived numeric restaurant features."},
                {"file": str(tables_dir / "categorical_counts.csv"), "description": "Exhaustive categorical value counts for restaurant, promotion, product, and menu dimensions."},
                {"file": str(tables_dir / "data_quality_checks.csv"), "description": "Duplicate and consistency checks."},
                {"file": str(tables_dir / "chain_summary.csv"), "description": "Chain-level rollup metrics."},
                {"file": str(tables_dir / "top_coordinate_clusters.csv"), "description": "Top rounded geographic clusters."},
                {"file": str(tables_dir / "top_restaurants_by_menu_items.csv"), "description": "Restaurants with the largest menus."},
                {"file": str(tables_dir / "top_restaurants_by_products.csv"), "description": "Restaurants with the most product cards."},
                {"file": str(tables_dir / "top_restaurants_by_rate_count.csv"), "description": "Most-reviewed restaurants."},
                {"file": str(tables_dir / "top_menu_section_names.csv"), "description": "Most common menu section names."},
                {"file": str(tables_dir / "top_menu_item_names.csv"), "description": "Most repeated menu item names."},
                {"file": str(tables_dir / "top_product_names.csv"), "description": "Most repeated product names."},
            ],
            ["file", "description"],
        ),
        "",
    ]

    with (reports_dir / "summary_report.md").open("w", encoding="utf-8") as handle:
        handle.write("\n".join(report_lines))

    print(f"Wrote EDA outputs to {output_dir}")


if __name__ == "__main__":
    main()
