#!/usr/bin/env python3

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_INPUT = Path("/Users/qq-nux/Downloads/hungerstation_restaurants.json")
DEFAULT_OUTPUT_DIR = Path("analysis/hungerstation")


def parse_args():
    parser = argparse.ArgumentParser(description="Run delivery-fee deep dive on Hungerstation restaurant JSON data.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Path to the input JSON file.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for analysis outputs.")
    return parser.parse_args()


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


def pct(part, whole):
    return (part / whole * 100.0) if whole else 0.0


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


def round_or_none(value, digits=4):
    if value is None:
        return None
    return round(value, digits)


def markdown_table(rows, columns):
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join([header, separator] + body)


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def regression(rows):
    xs = [row["distance_km"] for row in rows if row["distance_km"] is not None and row["delivery_fee"] is not None]
    ys = [row["delivery_fee"] for row in rows if row["distance_km"] is not None and row["delivery_fee"] is not None]
    n = len(xs)
    if not n:
        return {
            "n": 0,
            "pearson_r": None,
            "r_squared": None,
            "slope": None,
            "intercept": None,
            "mae": None,
            "rmse": None,
        }
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    sxx = sum((x - mean_x) ** 2 for x in xs)
    syy = sum((y - mean_y) ** 2 for y in ys)
    pearson_r = sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0
    slope = sxy / sxx if sxx else 0.0
    intercept = mean_y - slope * mean_x
    predictions = [slope * x + intercept for x in xs]
    mae = sum(abs(y - pred) for y, pred in zip(ys, predictions)) / n
    rmse = math.sqrt(sum((y - pred) ** 2 for y, pred in zip(ys, predictions)) / n)
    return {
        "n": n,
        "pearson_r": pearson_r,
        "r_squared": pearson_r * pearson_r,
        "slope": slope,
        "intercept": intercept,
        "mae": mae,
        "rmse": rmse,
    }


def dominant(counter):
    if not counter:
        return (None, 0, 0.0)
    value, count = counter.most_common(1)[0]
    total = sum(counter.values())
    return (value, count, pct(count, total))


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
        raise ValueError("Expected the root JSON object to be a list.")

    rows = []
    all_keys = set()
    for record in data:
        if not isinstance(record, dict):
            continue
        all_keys.update(record.keys())
        delivery = record.get("delivery") if isinstance(record.get("delivery"), dict) else {}
        distance = record.get("distance") if isinstance(record.get("distance"), dict) else {}
        location = record.get("location") if isinstance(record.get("location"), dict) else {}
        rows.append(
            {
                "id": record.get("id"),
                "chain_id": record.get("chain_id"),
                "chain_name": record.get("chain_name"),
                "vertical": record.get("vertical"),
                "distance_km": parse_number(distance.get("value")),
                "distance_unit": distance.get("unit"),
                "delivery_fee": parse_number(delivery.get("fee")),
                "delivery_original_fee": parse_number(delivery.get("original_fee")),
                "minimum_order": parse_number(record.get("minimum_order")),
                "delivery_type": delivery.get("type"),
                "delivery_name": delivery.get("name"),
                "status": record.get("status"),
                "latitude": parse_number(location.get("latitude")),
                "longitude": parse_number(location.get("longitude")),
                "external_id": record.get("external_id"),
            }
        )

    restaurants_only = [row for row in rows if row["vertical"] == "restaurants"]
    non_restaurants = [row for row in rows if row["vertical"] != "restaurants"]

    regression_rows = []
    for scope, subset in [
        ("all_rows", rows),
        ("restaurants_only", restaurants_only),
        ("non_restaurants", non_restaurants),
    ]:
        stats = regression(subset)
        regression_rows.append(
            {
                "scope": scope,
                "n": stats["n"],
                "pearson_r": round_or_none(stats["pearson_r"], 6),
                "r_squared": round_or_none(stats["r_squared"], 6),
                "slope": round_or_none(stats["slope"], 6),
                "intercept": round_or_none(stats["intercept"], 6),
                "mae": round_or_none(stats["mae"], 6),
                "rmse": round_or_none(stats["rmse"], 6),
            }
        )

    restaurant_regression = next(row for row in regression_rows if row["scope"] == "restaurants_only")
    fee_tiers = sorted({row["delivery_fee"] for row in restaurants_only if row["delivery_fee"] is not None})
    fee_counter = Counter(row["delivery_fee"] for row in restaurants_only if row["delivery_fee"] is not None)

    fee_tier_rows = []
    for fee in fee_tiers:
        distances = sorted(row["distance_km"] for row in restaurants_only if row["delivery_fee"] == fee and row["distance_km"] is not None)
        if not distances:
            continue
        fee_tier_rows.append(
            {
                "fee_sar": round_or_none(fee, 2),
                "restaurant_count": len(distances),
                "pct_of_restaurants": round(pct(len(distances), len(restaurants_only)), 4),
                "distance_min_km": round_or_none(distances[0], 4),
                "distance_p25_km": round_or_none(quantile(distances, 0.25), 4),
                "distance_median_km": round_or_none(quantile(distances, 0.50), 4),
                "distance_p75_km": round_or_none(quantile(distances, 0.75), 4),
                "distance_p95_km": round_or_none(quantile(distances, 0.95), 4),
                "distance_max_km": round_or_none(distances[-1], 4),
                "distance_mean_km": round_or_none(sum(distances) / len(distances), 4),
            }
        )

    distance_bands = [(0, 2), (2, 5), (5, 10), (10, 15), (15, 20), (20, 50)]
    distance_band_rows = []
    for lower, upper in distance_bands:
        subset = [row for row in restaurants_only if row["distance_km"] is not None and lower <= row["distance_km"] < upper]
        fees = sorted(row["delivery_fee"] for row in subset if row["delivery_fee"] is not None)
        fee_counts = Counter(fees)
        dominant_fee, dominant_count, dominant_share = dominant(fee_counts)
        top_fees = ", ".join(f"{int(fee) if fee.is_integer() else fee}:{count}" for fee, count in fee_counts.most_common(5))
        distance_band_rows.append(
            {
                "distance_band_km": f"{lower}-{upper}",
                "restaurant_count": len(subset),
                "pct_of_restaurants": round(pct(len(subset), len(restaurants_only)), 4),
                "fee_mean_sar": round_or_none(sum(fees) / len(fees) if fees else None, 4),
                "fee_median_sar": round_or_none(quantile(fees, 0.50) if fees else None, 4),
                "dominant_fee_sar": round_or_none(dominant_fee, 2),
                "dominant_fee_count": dominant_count,
                "dominant_fee_share_pct": round_or_none(dominant_share, 4),
                "top_fee_mix": top_fees,
            }
        )

    slope = float(restaurant_regression["slope"])
    intercept = float(restaurant_regression["intercept"])
    within_2 = 0
    nearest_match = 0
    for row in restaurants_only:
        if row["distance_km"] is None or row["delivery_fee"] is None:
            continue
        predicted = slope * row["distance_km"] + intercept
        if abs(row["delivery_fee"] - predicted) <= 2:
            within_2 += 1
        nearest_tier = min(fee_tiers, key=lambda tier: abs(tier - predicted))
        if row["delivery_fee"] == nearest_tier:
            nearest_match += 1

    formula_quality_rows = [
        {
            "scope": "restaurants_only",
            "within_2_sar_of_linear_prediction_pct": round(pct(within_2, len(restaurants_only)), 4),
            "exact_match_to_nearest_fee_tier_pct": round(pct(nearest_match, len(restaurants_only)), 4),
            "top_4_fee_tiers_share_pct": round(pct(sum(count for _, count in fee_counter.most_common(4)), len(restaurants_only)), 4),
        }
    ]

    validation_rows = [
        {"metric": "total_rows", "value": len(rows)},
        {"metric": "restaurants_only_rows", "value": len(restaurants_only)},
        {"metric": "non_restaurant_rows", "value": len(non_restaurants)},
        {"metric": "missing_location_rows", "value": sum(1 for row in rows if row["latitude"] is None or row["longitude"] is None)},
        {"metric": "external_id_non_null_rows", "value": sum(1 for row in rows if row["external_id"] is not None)},
        {"metric": "external_id_null_rows", "value": sum(1 for row in rows if row["external_id"] is None)},
        {"metric": "has_name_ar_key_anywhere_top_level", "value": "name_ar" in all_keys},
        {"metric": "has_query_lat_key_anywhere_top_level", "value": "query_lat" in all_keys},
        {"metric": "has_query_lng_key_anywhere_top_level", "value": "query_lng" in all_keys},
        {"metric": "unique_chain_ids", "value": len({row["chain_id"] for row in rows})},
        {"metric": "unique_chain_names", "value": len({row["chain_name"] for row in rows})},
        {"metric": "multi_branch_chain_ids", "value": sum(1 for _, count in Counter(row["chain_id"] for row in rows).items() if count > 1)},
        {"metric": "multi_branch_chain_names", "value": sum(1 for _, count in Counter(row["chain_name"] for row in rows).items() if count > 1)},
    ]

    write_csv(tables_dir / "delivery_fee_regression.csv", regression_rows, list(regression_rows[0].keys()))
    write_csv(tables_dir / "delivery_fee_tiers.csv", fee_tier_rows, list(fee_tier_rows[0].keys()))
    write_csv(tables_dir / "delivery_fee_distance_bands.csv", distance_band_rows, list(distance_band_rows[0].keys()))
    write_csv(tables_dir / "delivery_fee_formula_quality.csv", formula_quality_rows, list(formula_quality_rows[0].keys()))
    write_csv(tables_dir / "eda_validation_checks.csv", validation_rows, ["metric", "value"])

    summary_payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_path": str(input_path),
        "restaurants_only_regression": restaurant_regression,
        "all_rows_regression": next(row for row in regression_rows if row["scope"] == "all_rows"),
        "fee_tiers": [row["fee_sar"] for row in fee_tier_rows],
        "top_fee_tiers": fee_counter.most_common(10),
        "validation": {row["metric"]: row["value"] for row in validation_rows},
    }
    with (metadata_dir / "delivery_fee_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary_payload, handle, ensure_ascii=False, indent=2)

    report_lines = [
        "# Delivery Fee Deep Dive",
        "",
        f"- Generated at (UTC): {summary_payload['generated_at_utc']}",
        f"- Source file: `{input_path}`",
        "",
        "## Validation Notes",
        "",
        markdown_table(validation_rows, ["metric", "value"]),
        "",
        "Key validation points:",
        "",
        "- The raw payload does not contain `query_lat`, `query_lng`, or `name_ar` as top-level fields.",
        "- `external_id` is mostly null, but not completely null: only 6 rows have a value.",
        "- Delivery-fee modeling must distinguish `restaurants` from the small non-restaurant tail.",
        "",
        "## Regression Summary",
        "",
        markdown_table(regression_rows, ["scope", "n", "pearson_r", "r_squared", "slope", "intercept", "mae", "rmse"]),
        "",
        "Interpretation:",
        "",
        "- On the full mixed dataset, distance and fee are not meaningfully related because non-restaurant rows introduce extreme long-distance, low-fee cases.",
        f"- On `restaurants_only`, the relationship is strong: `fee ≈ {restaurant_regression['slope']} × distance_km + {restaurant_regression['intercept']}`.",
        "- The restaurant-only model is still an average relationship. Actual fees snap to discrete tiers rather than following a smooth continuous curve.",
        "",
        "## Fee Tier Distribution",
        "",
        markdown_table(fee_tier_rows, ["fee_sar", "restaurant_count", "pct_of_restaurants", "distance_median_km", "distance_p75_km", "distance_max_km"]),
        "",
        "## Distance Bands",
        "",
        markdown_table(distance_band_rows, ["distance_band_km", "restaurant_count", "fee_mean_sar", "fee_median_sar", "dominant_fee_sar", "dominant_fee_share_pct", "top_fee_mix"]),
        "",
        "## Formula Quality",
        "",
        markdown_table(formula_quality_rows, list(formula_quality_rows[0].keys())),
        "",
        "## Conclusions",
        "",
        "- Delivery fees behave like a stepped pricing ladder with strong distance dependence for real restaurant rows.",
        "- The most important operating tiers are 20, 24, 30, 35, and 40 SAR, with 24 and 30 SAR dominating the middle-distance range.",
        "- Short-range merchants cluster around 17 to 20 SAR, mid-range around 24 to 30 SAR, and long-range around 35 to 40 SAR.",
        "- Any fee model should be built on `vertical='restaurants'` and ideally treated as a tiered classifier or step function, not just a linear regressor.",
        "",
    ]

    with (reports_dir / "delivery_fee_report.md").open("w", encoding="utf-8") as handle:
        handle.write("\n".join(report_lines))

    print(f"Wrote delivery-fee outputs to {output_dir}")


if __name__ == "__main__":
    main()
