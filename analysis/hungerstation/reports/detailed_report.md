# Hungerstation Restaurants Dataset
## Detailed Exploratory Data Analysis Report

### 1. Objective
This report documents a full exploratory data analysis of the Hungerstation restaurant snapshot stored in `/Users/qq-nux/Downloads/hungerstation_restaurants.json`. The goal is to understand the dataset structure, coverage, data quality, commercial patterns, catalog depth, and the main analytical caveats before any downstream dashboarding, business analysis, or modeling work.

The analysis was run from the reproducible script [hungerstation_eda.py](/Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/scripts/hungerstation_eda.py). A second validation pass and delivery-fee deep dive were run from [hungerstation_delivery_fee_analysis.py](/Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/scripts/hungerstation_delivery_fee_analysis.py). Supporting outputs are organized under the Hungerstation analysis folder, especially [summary_report.md](/Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/reports/summary_report.md), [delivery_fee_report.md](/Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/reports/delivery_fee_report.md), [summary.json](/Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/metadata/summary.json), [delivery_fee_summary.json](/Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/metadata/delivery_fee_summary.json), [restaurants_flattened.csv](/Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/restaurants_flattened.csv), [numeric_summary.csv](/Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/numeric_summary.csv), [categorical_counts.csv](/Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/categorical_counts.csv), [chain_summary.csv](/Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/chain_summary.csv), and [data_quality_checks.csv](/Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/data_quality_checks.csv).

### 2. Dataset Overview

| Metric | Value |
| --- | ---: |
| File size | 461,849,482 bytes |
| Total records | 8,566 |
| Records with menus | 8,548 |
| Records with product cards | 5,757 |
| Menu sections | 72,478 |
| Menu items | 430,811 |
| Product cards | 18,871 |
| Unique chain names | 6,459 |
| Unique chain IDs | 6,850 |
| Unique brand IDs | 91 |
| Unique exact coordinates | 7,647 |

This is a large, nested marketplace snapshot rather than a simple flat store list. At the restaurant level, it combines:

- Merchant metadata
- Ratings and review counts
- Delivery and ETA information
- Geolocation
- Promotional metadata
- Menu catalogs
- Product-card summaries
- Pickup and subscription support

The data is wide enough for merchant profiling and deep enough for menu-level content analysis. One validation nuance matters immediately: `chain_id` and `chain_name` are not interchangeable. The dataset contains `6,850` unique `chain_id` values but only `6,459` unique `chain_name` values, so any "unique chains" claim needs to specify which key it uses.

### 3. Schema And Coverage
The root object is a list of `8,566` restaurant records. Most operational fields are present across all rows, but some fields are highly sparse or behave more like optional UI metadata than stable analytical dimensions.

#### 3.1 Near-complete fields
The following appear on all or nearly all rows:

- `id`, `brand_id`, `chain_id`, `chain_name`, `chain_type`
- `delivery`, `distance`, `time_estimation`, `location`
- `average_rating`, `rate_count`, `minimum_order`
- `status`, `supports_pickup`, `supports_scheduled_order`
- `kitchens`, `promotions`, `incentives`

#### 3.2 Sparse or special-purpose fields

| Field | Non-empty rows | Notes |
| --- | ---: | --- |
| `products` | 5,757 | Present on 67.21% of restaurants |
| `subscription` | 6,252 | Always either `supported=true` or null |
| `badge` | 3,860 | UI-facing merchandising label |
| `tags` | 2,583 | Restaurant discovery tags such as `Top Choice` |
| `price_range` | 8,509 | Missing for 57 rows |
| `restaurant_menu` | 8,548 | Missing for 18 rows |
| `label` | 6 | Rare closed-state marker |
| `external_id` | 6 | Almost entirely null |
| `status_indicator` | 8 | Rare urgency or state banner |

Interpretation:

- The core marketplace coverage is excellent.
- `external_id`, `label`, and `status_indicator` are too sparse to be primary modeling features.
- `products` is not a substitute for the full menu because a third of restaurants have no product cards despite having full menus.

#### 3.3 Fields absent from the raw payload
The validation rerun confirmed that several fields discussed in downstream scraper notes are not present in the raw Hungerstation response at all:

- `name_ar` is absent from the payload keys.
- `chain_name_ar` is absent from the payload keys.
- `title_ar` is absent from the payload keys.
- `query_lat` and `query_lng` are absent from the top-level payload keys.
- `external_id` is not universally null, but it is almost empty: only `6` rows have a value and `8,560` are null.

Important nuance:

- There are no dedicated Arabic-localized name fields.
- Arabic script does still appear sporadically inside free-text values: `6` chain names, `11` section names, `21` item names, `446` item descriptions, and `1` product name contain Arabic characters.
- In practice this means the dataset has limited mixed-language content, but not a structured Arabic naming layer.

Implication:

- Arabic naming, city attribution, and the original query point cannot be validated from the raw response alone. Those require either scraper-side enrichment, injected query metadata, or external geocoding.

### 4. Executive Findings
Several patterns dominate the snapshot:

1. The dataset is overwhelmingly composed of open restaurant listings rather than mixed commerce verticals.
2. Promotions are almost universal and are led by a standardized free-delivery mechanic.
3. Ratings are strong overall, but review volume is heavily right-skewed.
4. Menus are rich and nearly universal; product cards are much more selective and merchandising-oriented.
5. Operational pricing fields are unusually standardized, especially `minimum_order`.
6. Delivery fees are best modeled as a stepped tier system driven by distance for `vertical='restaurants'`, not for the mixed dataset as a whole.
7. The data is mostly clean on basic consistency checks, but some identifiers and coordinates are reused.

### 5. Restaurant-Level Marketplace Profile

#### 5.1 Restaurant status and platform availability

| Measure | Count | Share |
| --- | ---: | ---: |
| Open restaurants | 8,560 | 99.93% |
| Closed restaurants | 6 | 0.07% |
| Restaurants with menus | 8,548 | 99.79% |
| Restaurants with product cards | 5,757 | 67.21% |
| Rated restaurants | 8,279 | 96.65% |
| Unrated / zero-review restaurants | 287 | 3.35% |
| Most loved restaurants | 792 | 9.25% |
| Restaurants with restaurant tags | 2,583 | 30.15% |
| Restaurants with badges | 3,860 | 45.06% |

The marketplace snapshot is very mature operationally:

- Almost every listing is active.
- Almost every listing has a menu.
- Only a small minority are unrated.
- Roughly one in ten merchants is flagged as `is_most_loved`.

#### 5.2 Ratings and review counts

| Metric | Value |
| --- | ---: |
| Mean rating across all rows | 4.0137 |
| Mean rating among rated restaurants only | 4.1529 |
| Review-weighted rating | 4.2024 |
| Median rating | 4.2 |
| Median review count | 60 |
| 95th percentile review count | 658.5 |
| Max review count | 5,531 |

Rating distribution:

- `50.49%` of restaurants are between `4.0` and `4.49`
- `24.04%` are between `4.5` and `5.0`
- `19.30%` are between `3.0` and `3.99`
- `2.83%` are below `3.0`
- `3.35%` are unrated or have zero reviews

Interpretation:

- The merchant base is broadly well-reviewed.
- The review-weighted mean exceeds the simple rated-only mean, which suggests that the more heavily reviewed merchants are slightly better rated than the long tail.
- Review count is highly concentrated, so comparisons between chains or stores should always be volume-aware.

### 6. Commercial Structure

#### 6.1 Vertical mix

| Vertical | Count | Share |
| --- | ---: | ---: |
| `restaurants` | 8,496 | 99.18% |
| `specialty_and_ethnic` | 20 | 0.23% |
| `nuts_and_dried_fruits` | 17 | 0.20% |
| `charity` | 15 | 0.18% |
| `coffee_grinders` | 10 | 0.12% |
| `bakery` | 7 | 0.08% |
| `snacks_and_sweets` | 1 | 0.01% |

This is effectively a restaurants dataset with a very small specialty tail. The `charity` rows are analytically important because they behave differently from standard merchants and are likely responsible for several extreme values.

#### 6.2 Chain type and delivery model

| Dimension | Leading value | Count | Share |
| --- | --- | ---: | ---: |
| Chain type | `RESTAURANT` | 8,560 | 99.93% |
| Delivery type | `OWN_DELIVERY` | 8,551 | 99.82% |
| Delivery name | `Fast Delivery` | 8,551 | 99.82% |

Only `15` rows use `VENDOR_DELIVERY` / `Store Delivery`, and these align closely with the small charity segment.

#### 6.3 Pickup, scheduling, and subscription

| Feature | Count | Share |
| --- | ---: | ---: |
| Supports pickup | 6,486 | 75.72% |
| Supports scheduled order | 5,181 | 60.48% |
| Subscription supported | 6,252 | 72.99% |

Interpretation:

- Pickup is a standard capability for roughly three out of four merchants.
- Scheduled ordering is also common, but materially less universal than pickup.
- Subscription appears binary in practice: present support is encoded as `true`, and non-support is null rather than explicit `false`.

### 7. Pricing, Delivery, And ETA

#### 7.1 Minimum order
`minimum_order` is unusually standardized:

- `15 SAR` for `8,509` restaurants
- `20 SAR` for `42` restaurants
- `0 SAR` for `15` restaurants

This is not a normal continuous pricing field. It behaves more like a platform policy with a few exceptions.

#### 7.2 Delivery fee

| Metric | Value |
| --- | ---: |
| Median delivery fee | 25 |
| Mean delivery fee | 27.48 |
| 95th percentile | 40 |
| Max | 40 |

Most common fees:

- `24 SAR`: `2,153`
- `30 SAR`: `2,038`
- `40 SAR`: `1,277`
- `20 SAR`: `935`
- `22 SAR`: `473`

The fee summary in this section refers to `vertical='restaurants'`, because that is the only slice where fee behavior is stable enough to model. The structure is highly discretized rather than continuous, and it looks like a set of predefined pricing tiers. The validation rerun sharpened this point substantially.

Regression summary from the delivery-fee deep dive:

| Scope | Pearson r | R² | Slope | Intercept | MAE | RMSE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| All rows | -0.0614 | 0.0038 | -0.0100 | 27.5107 | 5.9031 | 7.0573 |
| Restaurants only | 0.9108 | 0.8296 | 1.3113 | 13.7534 | 2.0906 | 2.8748 |
| Non-restaurants only | -0.8166 | 0.6669 | -0.0195 | 20.6098 | 3.5126 | 5.8703 |

Interpretation:

- The strong fee-distance relationship exists only when the analysis is restricted to real restaurant rows.
- On the full mixed dataset, the relationship effectively disappears because the `charity` and specialty tail contains long-distance, low-fee exceptions.
- For restaurant rows, the average pricing rule is:

`delivery_fee ≈ 1.311 × distance_km + 13.753`

- Even that formula should be interpreted as an average trend, not the literal pricing engine, because actual fees snap to fixed tiers.

Validated fee tiers for `vertical='restaurants'` are:

`9, 10, 11, 12, 13, 15, 16, 17, 19, 20, 21, 22, 24, 25, 28, 30, 35, 40 SAR`

The most important tiers are still `24`, `30`, `40`, and `20 SAR`, which together cover `75.36%` of restaurant rows.

Distance-band view:

| Distance band | Restaurants | Mean fee | Median fee | Dominant fee | Dominant share |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0-2 km | 257 | 15.36 | 17 | 17 | 72.76% |
| 2-5 km | 787 | 19.13 | 20 | 20 | 51.08% |
| 5-10 km | 3,039 | 23.24 | 24 | 24 | 54.16% |
| 10-15 km | 2,954 | 29.37 | 30 | 30 | 65.23% |
| 15-20 km | 1,188 | 39.05 | 40 | 40 | 82.66% |
| 20-50 km | 271 | 39.48 | 40 | 40 | 89.67% |

This shows that delivery fee behaves more like a step ladder than a continuous line:

- short distance: mostly `17` to `20 SAR`
- lower mid distance: mostly `24 SAR`
- upper mid distance: mostly `30 SAR`
- long distance: mostly `35` to `40 SAR`

Modeling implication:

- A tiered classifier or step-function approximation is a better production interpretation than a plain linear model.
- The linear model is still useful as a summary and rough fee estimator, but only for restaurant rows.
- The nearest-tier match to the linear prediction is only `41.48%`, while `60.75%` of restaurant rows fall within `±2 SAR` of the linear prediction. That is consistent with a stepped pricing system built around a roughly linear backbone.

#### 7.3 ETA

| Metric | Value |
| --- | ---: |
| Median ETA minimum | 35 |
| Median ETA maximum | 50 |
| Median ETA window | 15 |
| Mean ETA minimum | 34.33 |
| Mean ETA maximum | 49.60 |

Most common ETA bands are:

- `30-45`
- `35-50`
- `40-55`
- `25-40`
- `45-60`

The ETA structure is also templated, with repeated 15-minute windows.

#### 7.4 Distance

| Metric | Value |
| --- | ---: |
| Median distance | 10.2 |
| Mean distance | 12.28 |
| 95th percentile | 18.6 |
| Max | 1328.8 |

The distance distribution is heavily affected by outliers. The maximum values belong to atypical rows such as `Tarmeem`, `Saudi Society for Public Taste`, `Children with Disability Association`, `Sanad`, and `Etaam`, all of which have:

- `0` delivery fee
- `0` ratings / reviews
- very large apparent distances

These rows should be segmented out of standard merchant delivery analysis.

### 8. Price Range Positioning
The `price_range` field is available for `8,509` restaurants and always uses a total scale of `3`.

| Price range | Count | Share of all restaurants |
| --- | ---: | ---: |
| `1/3` | 3,554 | 41.49% |
| `2/3` | 4,587 | 53.55% |
| `3/3` | 368 | 4.30% |
| Missing | 57 | 0.67% |

Interpretation:

- Mid-priced merchants dominate.
- Premium listings are present but small.
- The field is useful as a coarse affordability signal, but not as a precise price measure.

### 9. Merchant Discovery And Merchandising Signals

#### 9.1 Badges
`3,860` restaurants carry a badge. The most common badge texts are:

| Badge text | Count |
| --- | ---: |
| `20% off` | 1,843 |
| `Offers` | 1,668 |
| `30% off` | 168 |
| `25% off` | 104 |

Badge coverage is high enough to matter in discovery, but badge text is largely promotion-driven.

#### 9.2 Restaurant tags
`2,583` rows include restaurant-level tags. Top labels:

| Tag | Count |
| --- | ---: |
| `Top Choice` | 2,143 |
| `NEW` | 262 |
| `Best Price` | 216 |

Interpretation:

- Restaurant tags appear curated and limited.
- `Top Choice` is by far the dominant discoverability label.

### 10. Promotions And Incentives
Promotions are one of the strongest signals in the dataset.

| Measure | Value |
| --- | ---: |
| Restaurants with at least one promotion | 8,551 |
| Restaurants without promotions | 15 |
| Total promotion rows | 12,503 |
| Total incentive rows | 12,503 |
| Promotion / incentive mismatches | 0 |

Top promotion names:

| Promotion | Count |
| --- | ---: |
| `Free delivery (Spend 15 SAR)` | 8,509 |
| `20% off on selected items` | 2,421 |
| `30% off on selected items` | 647 |
| `25% off on selected items` | 241 |
| `50% off on selected items` | 171 |

Top promotion types:

| Type | Count |
| --- | ---: |
| `FREE_DELIVERY` | 8,551 |
| `MENU_ITEM_DISCOUNT` | 3,860 |
| `ORDER_PERCENTAGE_CUTBACK` | 87 |
| `FIXED_ORDER_CUTBACK` | 5 |

Interpretation:

- Promotions are standardized and platform-managed.
- Free delivery is almost universal and should be treated as a baseline commercial mechanic rather than a rare event.
- Menu item discounting is common, but order-level discounting is rare.

### 11. Cuisine Mix
The most common kitchens are:

| Kitchen | Count |
| --- | ---: |
| Desserts | 3,385 |
| Fast Food | 2,511 |
| Arabic | 1,899 |
| Coffee | 1,647 |
| Sandwich | 1,570 |
| Pastries | 1,506 |
| Grill | 1,412 |
| Saudi | 1,275 |
| Burgers | 1,210 |
| Breakfast | 1,046 |

Interpretation:

- The marketplace is strongly skewed toward dessert, fast food, coffee, pastries, and casual dining formats.
- Kitchen labels are multi-valued, so counts represent presence, not exclusive category assignment.

### 12. Product Cards
Product cards are a curated subset of catalog items used for discovery.

| Measure | Value |
| --- | ---: |
| Restaurants with products | 5,757 |
| Restaurants without products | 2,809 |
| Total product cards | 18,871 |
| Products with promotions | 9,873 |
| Products with badges | 18,871 |
| Products with tags | 7,444 |
| Products missing image | 54 |
| Products missing name | 0 |
| Products with null `product_id` | 15,271 |

Product pricing summary:

| Metric | Product price | Discounted price | Discount % |
| --- | ---: | ---: | ---: |
| Median | 30.0 | 25.6 | 20.0 |
| Mean | 44.75 | 36.93 | 22.75 |
| 95th percentile | 140.0 | 112.8 | 35.0 |
| Max | 619.0 | 495.2 | 65.0 |

Source mix:

| Source | Count | Share |
| --- | ---: | ---: |
| `best_seller` | 11,427 | 60.55% |
| `promotion` | 7,444 | 39.45% |

Interpretation:

- Product cards are explicitly merchandising-oriented.
- They are not complete catalog coverage.
- The null `product_id` rate is very high, so `id` or `sku_id` is more reliable for product-card tracking.

### 13. Menus
Menus are the richest part of the dataset.

#### 13.1 Coverage and structure

| Measure | Value |
| --- | ---: |
| Restaurants with menus | 8,548 |
| Restaurants without menus | 18 |
| Total sections | 72,478 |
| Total menu items | 430,811 |
| Median sections per restaurant | 8 |
| Median items per restaurant | 42 |
| Median items per section | 4 |

#### 13.2 Menu content coverage

| Feature | Count | Share of menu items |
| --- | ---: | ---: |
| Quick add available | 276,304 | 64.14% |
| Description present | 411,934 | 95.62% |
| Image present | 426,983 | 99.11% |
| Allergens present | 116,806 | 27.11% |
| Dietary info present | 276,392 | 64.16% |
| Tags present | 61,180 | 14.20% |
| Mandatory choices present | 1,334 | 0.31% |

Interpretation:

- The marketplace has very strong content completeness for descriptions and images.
- Allergen data is still sparse relative to general descriptive content.
- The low count of `mandatory_choices` suggests the dataset may not fully expose modifier complexity, or that many items are represented at the variation level already.

#### 13.3 Menu prices and calories

| Metric | Menu price | Discounted price | List price | Calories |
| --- | ---: | ---: | ---: | ---: |
| Median | 20.0 | 20.0 | 20.91 | 128 |
| Mean | 32.73 | 31.60 | 32.95 | 332.59 |
| 95th percentile | 105.0 | 99.0 | 105.0 | 1,250 |
| Max | 7,350.0 | 7,350.0 | 7,350.0 | 45,698 |

These extremes are not random corruption. The largest prices come from large-party or feast items such as:

- `Twina Meal Especially 20 Persons` at `7,350`
- `Twina Meal 20 Persons` at `6,510`
- `Family International Food Offer` at `2,760`
- `Feast` at `1,880`

The largest calorie values also belong to very large meals or suspiciously inflated entries, including:

- `Morning Feast Box` at `45,698`
- `Mandi Carcass` at `40,700`
- `Klopp Shawerma Sandwich` at `29,959`

Interpretation:

- Menu-level outliers are real observations, but they should be winsorized or segmented when modeling typical basket size or consumer nutrition.
- Calories especially need QA before health-related analysis.

#### 13.4 Common section and item naming
Top section names:

| Section | Count |
| --- | ---: |
| `Bestsellers` | 7,874 |
| `Beverages` | 2,786 |
| `Special discounts` | 1,985 |
| `Desserts` | 1,821 |
| `Top 3 Discounts 🔥` | 1,611 |

Top item names:

| Item | Count |
| --- | ---: |
| `Water` | 3,396 |
| `Pepsi` | 2,840 |
| `7 Up` | 1,614 |
| `French Fries` | 1,368 |
| `Cappuccino` | 1,026 |

This indicates strong menu standardization around drinks, fries, and common cafe / quick-service products.

### 14. Chain Analysis

#### 14.1 Largest chains by location count

| Chain | Locations | Mean rating | Total reviews |
| --- | ---: | ---: | ---: |
| Dunkin | 25 | 4.0320 | 4,821 |
| Al Tazaj | 24 | 4.0625 | 33,143 |
| Al Baik | 22 | 4.1864 | 26,082 |
| Kudu | 22 | 3.9682 | 15,655 |
| Herfy | 21 | 3.9000 | 10,118 |
| KFC | 21 | 3.6000 | 20,083 |

#### 14.2 Most reviewed chains

| Chain | Total reviews | Locations | Mean rating |
| --- | ---: | ---: | ---: |
| Al Tazaj | 33,143 | 24 | 4.0625 |
| Al Baik | 26,082 | 22 | 4.1864 |
| McDonald's KSA | 20,792 | 13 | 3.9154 |
| KFC | 20,083 | 21 | 3.6000 |
| Deep Fries | 19,825 | 6 | 4.2333 |

#### 14.3 Highest rated chains with at least 5 locations

| Chain | Mean rating | Locations | Total reviews |
| --- | ---: | ---: | ---: |
| TOZEEN | 4.7000 | 5 | 12 |
| Labkah | 4.6667 | 9 | 1,965 |
| Kyok | 4.6571 | 7 | 891 |
| Ladorf | 4.6333 | 6 | 17 |
| Aseel Nabulsieh Kunafa | 4.6286 | 7 | 1,366 |

Interpretation:

- Chain reach and review scale are highly concentrated.
- Some highly rated multi-location chains still have very low review bases, so ranking by mean alone can overstate quality.
- Large, well-reviewed chains such as `Al Tazaj`, `Al Baik`, and `Deep Fries` are more analytically robust than chains with fewer than 20 total reviews.

### 15. Geography
The dataset spans a wide geographic footprint:

| Metric | Value |
| --- | ---: |
| Latitude range | 17.5619 to 31.6808 |
| Longitude range | 36.4643 to 50.1312 |
| Unique exact coordinates | 7,647 |
| Duplicate-coordinate rows | 919 |

Largest rounded coordinate clusters at 3 decimal places include:

- `27.524, 41.671` with `79` restaurants
- `21.592, 39.167` with `71`
- `21.592, 39.152` with `56`

Interpretation:

- Merchant coordinates span many cities and regions.
- Repeated coordinates likely represent malls, shared kitchens, dense commercial corridors, or default pins.
- Exact lat/long should not be assumed to uniquely identify a branch.
- The raw payload does not include city labels or the original query coordinates, so any city-level market-share table or "single query point" conclusion must come from external geocoding or scraper-side metadata rather than this JSON alone.

### 16. Data Quality Assessment
The dataset is strong on structural consistency.

#### 16.1 Clean checks
The following checks returned zero issues:

- Duplicate restaurant IDs
- Duplicate external IDs
- Delivery fee greater than original fee
- ETA minimum greater than ETA maximum
- Invalid `price_range.rank > price_range.total`
- Ratings without reviews
- Reviews without ratings
- Promotion count mismatches with incentives
- Missing primary promotion despite promotion list
- Primary promotion missing from promotion list
- Product discounted price greater than product price
- Menu discounted price greater than list price

#### 16.2 Non-zero issues

| Issue | Count | Interpretation |
| --- | ---: | --- |
| Duplicate exact coordinates | 919 | Shared or reused store locations |
| Duplicate product IDs | 664 | Product identifiers are not globally unique |
| Duplicate product SKUs | 664 | Same issue as product IDs |
| Duplicate menu item IDs | 55,932 | Menu item IDs are reused across restaurants or sections |
| Menu price greater than list price | 1 | Single anomaly |
| Pickup support mismatch | 22 | Top-level and menu-level pickup fields disagree |
| Open status but menu unavailable | 22 | Operational inconsistency |

The `22` menu-availability inconsistencies are concentrated in a small set of records where:

- top-level `status` is `OPEN`
- `menu_available=False`
- `vendor_status` may be `BUSY`, `CLOSED`, or still `OPEN`

This is a small problem operationally, but it matters if availability is used as a target label.

### 17. Caveats And Analytical Risks

#### 17.1 Charity and special-purpose listings
The charity-related records behave differently from normal restaurants:

- zero minimum order or zero delivery fee
- zero reviews
- very large distances
- unusual menu structures

These should be filtered or tagged for most restaurant performance analyses.

#### 17.2 Identifier reuse
Neither menu item IDs nor product IDs are globally unique. Any entity resolution should use composite keys such as:

- `restaurant_id + menu_item_id`
- `restaurant_id + sku_id`
- `restaurant_id + product_name + section_name`

depending on the use case.

#### 17.3 Highly templated fields
Several fields are platform-standard rather than merchant-specific:

- `minimum_order`
- delivery fee tiers
- ETA window widths
- promotion mechanics

These still carry signal, but they may reflect platform rules more than merchant behavior.

#### 17.4 Sparse UI fields
`label`, `status_indicator`, and `external_id` are too sparse for general-purpose analysis.

#### 17.5 Outlier sensitivity
Menu price, calories, and distance all contain extreme but plausible records. Robust statistics should be preferred over raw means.

### 18. Recommended Cleaning Rules
Before building dashboards or models, the following cleaning strategy is appropriate:

1. Exclude or separately flag non-standard verticals, especially `charity`.
2. Build branch-level keys from `restaurant_id`; do not rely on coordinates as unique keys.
3. Build menu-level keys using a composite identifier rather than raw menu item ID.
4. Winsorize or segment distance, calories, and menu price outliers.
5. Treat `products` as a merchandising layer, not a complete product master.
6. Encode `subscription` null as `not observed / likely unsupported`, not as a clean boolean without review.
7. Treat `minimum_order` as quasi-categorical because it has almost no continuous variation.
8. Use review-weighted methods when comparing merchant quality.

### 19. Analytical Opportunities
This snapshot is strong enough to support:

- Merchant segmentation by cuisine, price tier, and service options
- Promotion penetration analysis
- Menu depth and complexity analysis
- Chain benchmarking by coverage, reviews, and ratings
- Pickup / scheduling support comparisons
- Menu content completeness scoring
- Geo-cluster analysis by coordinates

Potential next deliverables:

1. A cleaned restaurant-level modeling table
2. A menu-item fact table with composite keys
3. A visual dashboard with chain, cuisine, and geography slices
4. A merchant quality score combining ratings, review count, menu richness, and service coverage

### 20. Final Assessment
This is a high-value marketplace dataset with strong restaurant coverage, rich menu detail, and mostly solid structural quality. The most important practical conclusions are:

- The data is highly usable after moderate cleaning.
- Promotions and delivery mechanics are central platform features.
- Menus are the richest and most reliable granular source.
- Product cards are curated summaries, not the full catalog.
- Outlier handling and special-vertical filtering are necessary.
- Review-weighted chain analysis is more reliable than raw rating averages.

For business analysis, the dataset is already strong. For predictive or causal work, the main challenge is not missingness, but careful treatment of templated fields, reused identifiers, and operational outliers.
